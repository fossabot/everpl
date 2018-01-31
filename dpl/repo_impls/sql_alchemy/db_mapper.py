"""
This module contains definition of DB tables and
mappings of classes onto the corresponding DB tables.
It also contains methods used to initialize actual
mapping and set up ORM.
"""

import json
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.mutable

from dpl.placements.placement import Placement
from dpl.settings.connection_settings import ConnectionSettings
from dpl.settings.thing_settings import ThingSettings


class JSONEncodedDict(sa.types.TypeDecorator):
    """
    Represents an immutable structure as a json-encoded string.

    More info:
    http://docs.sqlalchemy.org/en/latest/orm/extensions/mutable.html
    """
    impl = sa.VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


# FIXME: CC26: Move a definition of tables out of a DB Mapper
# FIXME: CC27: Move a class mapping logic  out of a DB Mapper
class DbMapper(object):
    """
    DbMapper is a utility class that is responsible for
    building of MetaData object, definition of Tables
    and their structure and mapping of them to the
    classes via ORM
    """
    def __init__(self, metadata: Optional[sa.MetaData] = None):
        """
        Initializes an internal MetaData object with
        the specified one or creates a new one by if
        None value was specified

        :param metadata: an instance of MetaData to be
               used for construction of tables
        """
        if metadata is None:
            metadata = sa.MetaData()

        self.metadata = metadata

        self.table_placements = None  # type: sa.Table
        self.table_con_settings = None  # type: sa.Table
        self.table_thing_settings = None  # type: sa.Table

    def init_tables(self) -> None:
        """
        Creates instances of Table with a predefined schema.
        Initializes values of table_placements, table_con_settings
        and table_thing_settings

        :return: None
        """
        self.table_placements = sa.Table(
            'placements', self.metadata,
            sa.Column('_domain_id', sa.String(32), primary_key=True),
            sa.Column('_friendly_name', sa.String(50), nullable=True),
            sa.Column('_image_url', sa.String(120), nullable=True)
        )

        self.table_con_settings = sa.Table(
            'connection_settings', self.metadata,
            sa.Column('_domain_id', sa.String(32), primary_key=True),
            sa.Column('_integration', sa.String(32), index=True),
            sa.Column('_con_type', sa.String(32)),
            sa.Column('_con_params', sa.ext.mutable.MutableDict.as_mutable(JSONEncodedDict)),
        )

        self.table_thing_settings = sa.Table(
            'thing_settings', self.metadata,
            sa.Column('_domain_id', sa.String(32), primary_key=True),
            sa.Column('_integration', sa.String(32), index=True),
            sa.Column('_thing_type', sa.String(32)),
            sa.Column('_con_id', sa.String(32), sa.ForeignKey("connection_settings._domain_id"), nullable=False),
            sa.Column('_con_params', sa.ext.mutable.MutableDict.as_mutable(JSONEncodedDict)),
            sa.Column('_friendly_name', sa.String(50), nullable=True),
            sa.Column('_placement_id', sa.String(32), sa.ForeignKey("placements._domain_id"), nullable=True)
        )

    def init_mappers(self) -> None:
        """
        Creates mappers between the object model classes and the
        corresponding tables

        :return: None
        """
        sa.orm.mapper(Placement, self.table_placements)
        sa.orm.mapper(ConnectionSettings, self.table_con_settings)
        sa.orm.mapper(ThingSettings, self.table_thing_settings)

    def create_all_tables(self, bind: sa.engine.Connectable):
        """
        Calls create_all on the stored metadata. Creates all
        tables in DB if they are not created yet

        :param bind: an instance of connectable for which
               the tables must be created
        :return: None
        """
        self.metadata.create_all(bind=bind)

    def drop_all_tables(self, bind: sa.engine.Connectable) -> None:
        """
        Calls drop_all on the stored metadata. Drops all
        tables in DB if they was created yet

        :param bind: an instance of connectable for which
               the tables must be dropped
        :return: None
        """
        self.metadata.drop_all(bind=bind)
