import unittest

import sqlalchemy as sa

from dpl.repo_impls.sql_alchemy.db_mapper import DbMapper


class TestDbMapper(unittest.TestCase):
    def test_init(self):
        mapper = DbMapper()

        engine = sa.create_engine("sqlite:///test_db.sqlite")

        mapper.init_tables()
        mapper.init_mappers()

        mapper.drop_all_tables(engine)
        mapper.create_all_tables(engine)
