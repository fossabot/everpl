# Include standard modules
import asyncio
import os
import logging

# Include 3rd-party modules
from sqlalchemy import create_engine

# Include DPL modules
from dpl import DPL_INSTALL_PATH
from dpl import api
from dpl import auth
from dpl.core import LegacyConfiguration
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


LOGGER = logging.getLogger(__name__)


class Controller(object):
    def __init__(self):
        self._conf = LegacyConfiguration(path=os.path.join(DPL_INSTALL_PATH, "../samples/config"))

        # FIXME: Make path configurable
        db_path = os.path.expanduser("~/everpl_db.sqlite")
        self._engine = create_engine("sqlite:///%s" % db_path, echo=True)
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
        self._conf.load_config()

        core_settings = self._conf.get_by_subsystem("core")
        is_safe_mode = core_settings.get('safe_mode_enabled', False)

        if is_safe_mode:
            LOGGER.warning("\n\n\nSafe mode is enabled, the most of everpl capabilities will be disabled\n\n")
        else:
            await self._bootstrap_integrations()

        # FIXME: Only for testing purposes
        self._auth_manager.create_root_user("admin", "admin")

        asyncio.ensure_future(
            self._rest_api.create_server(host="0.0.0.0", port=10800)
        )

    async def _bootstrap_integrations(self):
        core_settings = self._conf.get_by_subsystem("core")
        connection_settings = self._con_settings_repo.load_all()
        thing_settings = self._thing_settings_repo.load_all()

        enabled_integrations = core_settings["enabled_integrations"]

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
