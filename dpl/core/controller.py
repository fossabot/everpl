# Include standard modules
import asyncio
import os
import logging

# Include 3rd-party modules
from sqlalchemy import create_engine
import appdirs

# Include DPL modules
from dpl import api
from dpl import auth
from dpl.core.configuration import Configuration
from dpl.integrations.binding_bootstrapper import BindingBootstrapper

from dpl.repo_impls.sql_alchemy.session_manager import SessionManager
from dpl.repo_impls.sql_alchemy.db_mapper import DbMapper
from dpl.repo_impls.sql_alchemy.placement_repository import PlacementRepository

from dpl.repo_impls.sql_alchemy.connection_settings_repo import ConnectionSettingsRepository
from dpl.repo_impls.sql_alchemy.thing_settings_repo import ThingSettingsRepository

from dpl.repo_impls.in_memory.connection_repository import ConnectionRepository
from dpl.repo_impls.in_memory.thing_repository import ThingRepository

from dpl.service_impls.placement_service import PlacementService
from dpl.service_impls.thing_service import ThingService


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
        self._conf = Configuration()
        self._conf.load_or_create_config(DEFAULT_CONFIG_PATH)

        self._core_config = self._conf.get_by_subsystem('core')
        self._apis_config = self._conf.get_by_subsystem('apis')
        self._integrations_config = self._conf.get_by_subsystem('integrations')

        logging_level_str = self._core_config['logging_level']  # type: str
        dpl_root_logger.setLevel(level=logging_level_str.upper())

        if self._core_config.get('main_db_path') is None:
            self._core_config['main_db_path'] = DEFAULT_MAIN_DB_PATH

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
        self._db_session_manager = SessionManager(engine=self._engine)

        self._con_settings_repo = ConnectionSettingsRepository(self._db_session_manager)
        self._thing_settings_repo = ThingSettingsRepository(self._db_session_manager)

        self._placement_repo = PlacementRepository(self._db_session_manager)
        self._connection_repo = ConnectionRepository()
        self._thing_repo = ThingRepository()

        self._placement_service = PlacementService(self._placement_repo)
        self._thing_service = ThingService(self._thing_repo)

        self._auth_manager = auth.AuthManager()

        self._api_gateway = api.ApiGateway(self._auth_manager, self._thing_service, self._placement_service)
        self._rest_api = api.RestApi(self._api_gateway)

    async def start(self):
        is_safe_mode = self._core_config['is_safe_mode']

        if is_safe_mode:
            module_logger.warning("\n\n\nSafe mode is enabled, the most of everpl capabilities will be disabled\n\n")
            module_logger.warning("\n!!! REST API access will be enabled in the safe mode !!!\n")

            # Only REST API will be enabled in the safe mode
            self._apis_config['enabled_apis'] = ('rest_api', )

            # Force enable API access
            self._core_config['is_api_enabled'] = True
        else:
            await self._bootstrap_integrations()

        # FIXME: Only for testing purposes
        self._auth_manager.create_root_user("admin", "admin")

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
            await self._start_rest_api()

    async def _start_rest_api(self):
        """
        Starts REST API server

        :return: None
        """
        rest_api_config = self._apis_config['rest_api']
        rest_api_host = rest_api_config['host']
        rest_api_port = rest_api_config['port']

        asyncio.ensure_future(
            self._rest_api.create_server(host=rest_api_host, port=rest_api_port)
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

        self._thing_service.enable_all()

    async def shutdown(self):
        await self._rest_api.shutdown_server()
        self._thing_service.disable_all()
