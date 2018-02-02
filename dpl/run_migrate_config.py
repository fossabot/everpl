"""
This module contains instructions for migration of
some settings from config files into the database
"""

# Include standard modules
import os
from typing import Mapping, Any

# Include 3rd-party modules
from sqlalchemy import create_engine

# Include DPL modules
from dpl import DPL_INSTALL_PATH
from dpl.core import Configuration
from dpl.placements.placement_bootstrapper import PlacementBootstrapper

from dpl.settings.thing_settings import ThingSettings
from dpl.settings.connection_settings import ConnectionSettings

from dpl.repo_impls.sql_alchemy.session_manager import SessionManager
from dpl.repo_impls.sql_alchemy.db_mapper import DbMapper
from dpl.repo_impls.sql_alchemy.placement_repository import PlacementRepository
from dpl.repo_impls.sql_alchemy.connection_settings_repo import ConnectionSettingsRepository
from dpl.repo_impls.sql_alchemy.thing_settings_repo import ThingSettingsRepository


def con_settings_deserialize(mapping_settings: Mapping[str, Any]) -> ConnectionSettings:
    """
    Converts connection settings from a legacy dict-based
    format to an instance of ConnectionSettings class

    :param mapping_settings: connection settings stored
           as a mapping (dict)
    :return: a corresponding instance of ConnectionSettings
    """
    return ConnectionSettings(
        domain_id=mapping_settings['id'],
        integration=mapping_settings['integration'],
        con_type=mapping_settings['con_type'],
        con_params=mapping_settings['con_params']
    )


def thing_settings_deserialize(mapping_settings: Mapping[str, Any]) -> ThingSettings:
    """
    Converts thing settings from a legacy dict-based
    format to an instance of ThingSettings class

    :param mapping_settings: connection settings stored
           as a mapping (dict)
    :return: a corresponding instance of ConnectionSettings
    """
    return ThingSettings(
        # Mandatory parameters:
        domain_id=mapping_settings['id'],
        integration=mapping_settings['integration'],
        thing_type=mapping_settings['type'],
        con_id=mapping_settings['con_id'],
        con_params=mapping_settings['con_params'],
        # Optional parameters
        friendly_name=mapping_settings.get('friendly_name'),
        placement_id=mapping_settings.get('placement')
    )


def main():
    warning_header = """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                           WARNING                            !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

    warning_text = "You will LOST all data that is currently stored in %s " \
                   "database file. At the same time your legacy text file " \
                   "configuration will remain untouched.\n"

    print(warning_header)
    print(warning_text)

    answer = input(
        "\nContinue migration? (yes/no)\n"
    )

    while answer not in ('yes', 'no'):
        print("Please, answer yes or no")

    if answer == 'no':
        print("Migration aborted")
        exit(1)

    print("\nStarting migration...")

    os.path.abspath(__file__)

    conf = Configuration(path=os.path.join(DPL_INSTALL_PATH, "../samples/config"))

    # FIXME: Make path configurable
    db_path = os.path.expanduser("~/everpl_db.sqlite")
    engine = create_engine("sqlite:///%s" % db_path, echo=True)
    db_mapper = DbMapper()
    db_mapper.init_tables()
    db_mapper.init_mappers()
    db_mapper.drop_all_tables(bind=engine)
    db_mapper.create_all_tables(bind=engine)
    db_session_manager = SessionManager(engine=engine)

    placement_repo = PlacementRepository(db_session_manager)
    con_settings_repo = ConnectionSettingsRepository(db_session_manager)
    thing_settings_repo = ThingSettingsRepository(db_session_manager)

    conf.load_config()

    # FIXME: Migrate Connection and Thing settings too!
    placement_settings = conf.get_by_subsystem("placements")
    connection_settings = conf.get_by_subsystem("connections")
    thing_settings = conf.get_by_subsystem("things")

    PlacementBootstrapper.init_placements(
        placement_repo=placement_repo,
        config=placement_settings
    )

    db_session_manager.get_session().commit()

    for i in connection_settings:
        con_settings_repo.add(
            con_settings_deserialize(i)
        )

    db_session_manager.get_session().commit()

    for i in thing_settings:
        thing_settings_repo.add(
            thing_settings_deserialize(i)
        )

    db_session_manager.get_session().commit()

    print("\nMigration finished! Your instance of everpl is ready to rock")


if __name__ == '__main__':
    main()
