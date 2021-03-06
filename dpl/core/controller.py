# Include standard modules
import asyncio
import os
import logging
import argparse
import functools

# Include 3rd-party modules
from sqlalchemy import create_engine
import appdirs

# Include DPL modules
from dpl.core.configuration import Configuration
from dpl.integrations.binding_bootstrapper import BindingBootstrapper

from dpl.repo_impls.sql_alchemy.db_session_manager import DbSessionManager
from dpl.repo_impls.sql_alchemy.db_mapper import DbMapper
from dpl.repo_impls.sql_alchemy.user_repository import UserRepository
from dpl.repo_impls.sql_alchemy.placement_repository import PlacementRepository

from dpl.repo_impls.sql_alchemy.connection_settings_repo import ConnectionSettingsRepository
from dpl.repo_impls.sql_alchemy.thing_settings_repo import ThingSettingsRepository

from dpl.repo_impls.in_memory.session_repository import SessionRepository
from dpl.repo_impls.in_memory.connection_repository import ConnectionRepository
from dpl.repo_impls.in_memory.thing_repository import ThingRepository

from dpl.service_impls.user_service import UserService
from dpl.service_impls.session_service import SessionService
from dpl.service_impls.placement_service import PlacementService
from dpl.service_impls.thing_service import ThingService

from dpl.auth.auth_service import AuthService, ServiceEntityResolutionError
from dpl.auth.auth_context import AuthContext
from dpl.auth.auth_aspect import AuthAspect

from dpl.utils.simple_interceptor import SimpleInterceptor

from dpl.events.event_hub import EventHub
from dpl.events.build_object_related_event import build_object_related_event

from dpl.api.rest_api.things_subapp import build_things_subapp
from dpl.api.rest_api.placements_subapp import build_placements_subapp
from dpl.api.http_api_provider import HttpApiProvider
from dpl.api.rest_api.rest_api_provider import RestApiProvider

from dpl.api.streaming_api.streaming_api_provider import StreamingApiProvider


module_logger = logging.getLogger(__name__)
dpl_root_logger = logging.getLogger(name='dpl')

# Path to the folder with everpl configuration used by default
DEFAULT_CONFIG_DIR = appdirs.user_config_dir(
    appname='everpl'
)

CONFIG_NAME = 'everpl_config.yaml'
MAIN_DB_NAME = 'everpl_db.sqlite'

# Path to the configuration file to be used by default
# like ~/.config/everpl/everpl_config.yaml)
DEFAULT_CONFIG_PATH = os.path.join(DEFAULT_CONFIG_DIR, CONFIG_NAME)

# Path to the main database file to be used by default
DEFAULT_MAIN_DB_PATH = os.path.join(DEFAULT_CONFIG_DIR, MAIN_DB_NAME)


class Controller(object):
    def __init__(self):
        # FIXME: Initialize configuration externally
        self._conf = Configuration()

        args = self.parse_arguments()

        if args.config_dir is None:
            self._config_dir = DEFAULT_CONFIG_DIR
        else:
            self._config_dir = args.config_dir

        if args.config_path is None:
            self._config_path = os.path.join(self._config_dir, CONFIG_NAME)
        else:
            self._config_path = args.config_path

        self._conf.load_or_create_config(self._config_path)
        self.apply_arguments(args)

        self._core_config = self._conf.get_by_subsystem('core')
        self._apis_config = self._conf.get_by_subsystem('apis')
        self._integrations_config = self._conf.get_by_subsystem('integrations')

        logging_level_str = self._core_config['logging_level']  # type: str
        dpl_root_logger.setLevel(level=logging_level_str.upper())

        if self._core_config.get('main_db_path') is None:
            self._core_config['main_db_path'] = os.path.join(self._config_dir, MAIN_DB_NAME)

        main_db_path = self._core_config.get('main_db_path')
        echo_db_requests = (logging_level_str == 'debug')

        if not os.path.exists(main_db_path):
            logging.warning("There is no DB file present by the specified path. "
                            "A new one will be created: %s" % main_db_path)

        self._engine = create_engine("sqlite:///%s" % main_db_path, echo=echo_db_requests)
        self._db_mapper = DbMapper()
        self._db_mapper.init_tables()
        self._db_mapper.init_mappers()
        self._db_mapper.create_all_tables(bind=self._engine)
        self._db_session_manager = DbSessionManager(engine=self._engine)

        self._con_settings_repo = ConnectionSettingsRepository(self._db_session_manager)
        self._thing_settings_repo = ThingSettingsRepository(self._db_session_manager)

        self._user_repo = UserRepository(self._db_session_manager)
        self._placement_repo = PlacementRepository(self._db_session_manager)

        self._session_repo = SessionRepository()
        self._connection_repo = ConnectionRepository()
        self._thing_repo = ThingRepository()

        is_safe_mode = self._core_config['is_safe_mode']

        if is_safe_mode:
            module_logger.warning(
                "\n\n\nSafe mode is enabled, the most of everpl capabilities will be disabled\n\n")
            module_logger.warning(
                "\n!!! REST API access will be enabled in the safe mode !!!\n")

            # Only REST API will be enabled in the safe mode
            self._apis_config['enabled_apis'] = ('rest_api',)

            # Force enable API access
            self._core_config['is_api_enabled'] = True
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                self._bootstrap_integrations()
            )

        self._user_service_raw = UserService(self._user_repo)
        self._session_service_raw = SessionService(self._session_repo)
        self._auth_service = AuthService(self._user_service_raw, self._session_service_raw)

        self._auth_context = AuthContext()
        self._auth_aspect = AuthAspect(
            auth_service=self._auth_service,
            auth_context=self._auth_context
        )

        self._placement_service_raw = PlacementService(self._placement_repo)
        self._placement_service = SimpleInterceptor(
            wrapped=self._placement_service_raw,
            aspect=self._auth_aspect
        )  # type: PlacementService

        self._thing_service_raw = ThingService(self._thing_repo)
        self._thing_service = SimpleInterceptor(
            wrapped=self._thing_service_raw,
            aspect=self._auth_aspect
        )  # type: ThingService

        api_context_data = {'auth_context': self._auth_context}

        self._event_hub = EventHub()
        self._setup_event_hub(self._event_hub)

        self._user_service_raw.subscribe(self._event_hub)
        self._placement_service_raw.subscribe(self._event_hub)
        self._thing_service_raw.subscribe(self._event_hub)

        self._rest_api_things = build_things_subapp(
            thing_service=self._thing_service,
            additional_data=api_context_data
        )

        self._rest_api_placements = build_placements_subapp(
            placement_service=self._placement_service,
            additional_data=api_context_data
        )

        self._http_api = HttpApiProvider()

        self._rest_api = RestApiProvider(
            things=self._rest_api_things,
            placements=self._rest_api_placements,
            auth_context=self._auth_context,
            auth_service=self._auth_service
        )

        self._http_api.add_child_provider(
            provider=self._rest_api,
            provider_root='/api/rest/v1/'
        )

        self._separate_streaming = False
        self._streaming_api_provider = None

        if 'streaming_api' in self._apis_config['enabled_apis']:
            self._init_streaming_api()

        # None will indicate that this module was disabled
        self._local_announce = None

        # if module ws enabled...
        if 'local_announce' in self._apis_config['enabled_apis']:
            self._initialize_local_announcement()

    def _init_streaming_api(self) -> None:
        """
        Initializes and sets up an Streaming API instance

        :return: None
        """
        streaming_api_config = self._apis_config.get('streaming_api', dict())

        self._separate_streaming = (
                streaming_api_config.get('host') is not None or
                streaming_api_config.get('port') is not None or
                streaming_api_config.get('is_strict_tls') is not None
        )

        if self._separate_streaming:
            api_root = '/api/streaming/v1/'
        else:
            api_root = '/'

        self._streaming_api_provider = StreamingApiProvider(
            auth_context=self._auth_context,
            auth_service=self._auth_service,
            api_root=api_root
        )

        if not self._separate_streaming:
            self._http_api.add_child_provider(
                provider=self._streaming_api_provider,
                provider_root='/api/streaming/v1/'
            )

        self._event_hub.subscribe(self._streaming_api_provider)

    @staticmethod
    def _setup_event_hub(event_hub: EventHub) -> None:
        """
        Sets up EventHub to handle notifications from ObservableServices

        :param event_hub: an instance of EventHub to be set up
        :return: None
        """
        handler_users = functools.partial(
            build_object_related_event, target_root_topic='users'
        )

        handler_placements = functools.partial(
            build_object_related_event, target_root_topic='placements'
        )

        handler_things = functools.partial(
            build_object_related_event, target_root_topic='things'
        )

        event_hub.register_handler(
            source_type=UserService, handler=handler_users
        )

        event_hub.register_handler(
            source_type=PlacementService, handler=handler_placements
        )

        event_hub.register_handler(
            source_type=ThingService, handler=handler_things
        )

    def _initialize_local_announcement(self):
        """
        Performs an import of local_announce module an initializes the
        self._local_announce field with LocalAnnounce constructor

        :return: None
        """
        try:  # ...try to import a module and initialize its instance
            from dpl.api.local_announce import LocalAnnounce
            self._local_announce = LocalAnnounce()
        except ImportError as e:  # if something gone wrong...
            # ... print an error ...
            logging.error(
                "Failed to enable local_announce module: %s. Install all "
                "missing dependencies or disable local_announce module in "
                "everpl config file" % e
            )
            raise  # ...and terminate

    def parse_arguments(self):
        """
        Parses command-line arguments and alters everpl configuration
        correspondingly. Returns values of cmdline arguments

        :return: Any
        """
        # FIXME: Move argument parsing to the run.py script
        arg_parser = argparse.ArgumentParser(
            description="everpl runner script"
        )

        arg_parser.add_argument(
            '--is-safe', help='if everpl must to be started in the safe mode',
            type=bool, dest='is_safe', default=None
        )

        arg_parser.add_argument(
            '--log-level', help='minimum level of logging messages to be displayed',
            type=bool, dest='log_level', default=None
        )

        arg_parser.add_argument(
            '--is-api-enabled', help='if any API access must to be enabled',
            type=bool, dest='is_api_enabled', default=None
        )

        arg_parser.add_argument(
            '--config-dir', help='a path to the configuration directory',
            type=str, dest='config_dir', default=None
        )

        arg_parser.add_argument(
            '--config-path', help='a path to the everpl config file',
            type=str, dest='config_path', default=None
        )

        arg_parser.add_argument(
            '--db-path', help='a path to the main DB file to be used',
            type=str, dest='db_path', default=None
        )

        arg_parser.add_argument(
            '--rest-api-host', help='a hostname used for REST API listening',
            type=str, dest='rest_api_host', default=None
        )

        arg_parser.add_argument(
            '--rest-api-port', help='a listening port for REST API',
            type=int, dest='rest_api_port', default=None
        )

        return arg_parser.parse_args()

    def apply_arguments(self, args) -> None:
        """
        Applies cmdline arguments to the configuration

        :param args: arguments to be applied
        :return: None
        """
        if args.is_safe is not None:
            self._core_config['is_safe'] = args.is_safe

        if args.log_level is not None:
            self._core_config['logging_level'] = args.log_level

        if args.is_api_enabled is not None:
            self._core_config['is_api_enabled'] = args.is_api_enabled

        if args.db_path is not None:
            self._core_config['main_db_path'] = args.db_path

        if args.rest_api_host is not None:
            self._apis_config['rest_api']['host'] = args.rest_api_host

        if args.rest_api_port is not None:
            self._apis_config['rest_api']['port'] = args.rest_api_port

    async def start(self):
        # FIXME: Only for testing purposes
        try:
            self._user_service_raw.view_by_username('admin')

        except ServiceEntityResolutionError:
            self._user_service_raw.create_user("admin", "admin")
            self._db_session_manager.get_session().commit()

        self._thing_service_raw.enable_all()

        is_api_enabled = self._core_config['is_api_enabled']

        if is_api_enabled:
            await self._start_apis()
        else:
            module_logger.warning("All APIs was disabled by everpl configuration. "
                                  "Connections from client devices will be blocked")

    async def _start_apis(self):
        """
        Starts all APIs enabled in everpl configuration

        :return: None
        """
        enabled_apis = self._apis_config['enabled_apis']

        if 'rest_api' in enabled_apis:
            await self._start_http_api()

        if 'streaming_api' in enabled_apis and self._separate_streaming:
            await self._start_streaming_api()

        if 'local_announce' in enabled_apis:
            self._start_local_announce()

    async def _start_streaming_api(self) -> None:
        """
        Starts a Streaming API on host and port different from the main API

        :return: None
        """
        rest_api_config = self._apis_config.get('rest_api', dict())
        streaming_api_config = self._apis_config.get('streaming_api', dict())

        host = streaming_api_config.get('host', rest_api_config['host'])
        port = streaming_api_config.get('port', rest_api_config['port'])

        assert isinstance(self._streaming_api_provider, StreamingApiProvider)

        await self._streaming_api_provider.create_server(host=host, port=port)

    def _start_local_announce(self):
        local_announce_config = self._apis_config['local_announce']
        rest_api_config = self._apis_config.get('rest_api', dict())

        if local_announce_config['use_rest_host']:
            assert 'rest_api' in self._apis_config
            host = rest_api_config['host']
        else:
            host = local_announce_config['host']

        if local_announce_config['use_rest_port']:
            assert 'rest_api' in self._apis_config
            port = rest_api_config['port']
        else:
            port = local_announce_config['port']

        self._local_announce.create_server(
            instance_name=None,  # use default
            # address=,  # use default
            port=port,  # use default REST API listening port
            server_host=host  # use REST API listening hostname
        )

    async def _start_http_api(self):
        """
        Starts HTTP API server with parameters defined for REST API

        :return: None
        """
        rest_api_config = self._apis_config['rest_api']
        rest_api_host = rest_api_config['host']
        rest_api_port = rest_api_config['port']

        asyncio.ensure_future(
            self._http_api.create_server(
                host=rest_api_host, port=rest_api_port
            )
        )

    async def _bootstrap_integrations(self):
        enabled_integrations = self._integrations_config['enabled_integrations']

        connection_settings = self._con_settings_repo.load_all()
        thing_settings = self._thing_settings_repo.load_all()

        binding_bootstrapper = BindingBootstrapper(
            connection_repo=self._connection_repo,
            thing_repo=self._thing_repo
        )

        binding_bootstrapper.init_integrations(enabled_integrations)
        binding_bootstrapper.init_connections(connection_settings)
        binding_bootstrapper.init_things(thing_settings)

        self._db_session_manager.remove_session()

    async def shutdown(self):
        if self._local_announce is not None:
            self._local_announce.shutdown_server()

        if self._separate_streaming:
            await self._streaming_api_provider.shutdown_server()

        await self._http_api.shutdown_server()
        self._thing_service_raw.disable_all()
