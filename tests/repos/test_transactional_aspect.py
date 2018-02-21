import unittest

from sqlalchemy import create_engine
from dpl.utils.simple_interceptor import SimpleInterceptor

from dpl.repo_impls.sql_alchemy.db_mapper import DbMapper
from dpl.repo_impls.sql_alchemy.db_session_manager import DbSessionManager
from dpl.repo_impls.sql_alchemy.transactional_aspect import TransactionalAspect
from dpl.repo_impls.sql_alchemy.placement_repository import PlacementRepository
from dpl.service_impls.placement_service import PlacementService


class TestTransactionalAspect(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._test_db_path = "sqlite://"  # use an in-memory DB
        cls._engine = create_engine(cls._test_db_path)

        cls._mapper = DbMapper()
        cls._mapper.init_tables()
        cls._mapper.init_mappers()

    def setUp(self):
        self._mapper.drop_all_tables(self._engine)
        self._mapper.create_all_tables(self._engine)
        self._session_manager = DbSessionManager(engine=self._engine)
        self._placement_repo = PlacementRepository(
            session_manager=self._session_manager
        )
        self._placement_service = PlacementService(
            placement_repo=self._placement_repo
        )

    def test_without_aspect(self):
        # FIXME: REWRITE and split to the several other tests

        # just to be sure
        placements = self._placement_service.view_all()
        assert(
            len(placements) == 0  # just to be sure
        )

        # create a new Placement
        self._placement_service.create_placement(
            friendly_name="Some Placement",
            image_url=None
        )

        # and forcefully remove a current session
        self._session_manager.remove_session()

        # expected result: changes wasn't saved
        placements = self._placement_service.view_all()
        self.assertTrue(
            len(placements) == 0
        )

    def test_all_magic(self):
        # FIXME: REWRITE and split to the several other tests
        aspect = TransactionalAspect(self._session_manager)
        interceptor = SimpleInterceptor(
            wrapped=self._placement_service,
            aspect=aspect
        )  # type: PlacementService

        # create a new Placement
        interceptor.create_placement(
            friendly_name="Some Placement",
            image_url=None
        )

        # and forcefully remove a current session
        self._session_manager.remove_session()

        # expected result: changes was saved
        placements = interceptor.view_all()
        self.assertTrue(
            len(placements) == 1
        )
