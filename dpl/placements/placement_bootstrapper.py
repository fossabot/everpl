from typing import Iterable, Mapping

from dpl.placements.placement_builder import PlacementBuilder
from dpl.repos.abs_placement_repository import AbsPlacementRepository


class PlacementBootstrapper(object):
    """
    PlacementBootstrapper is a class which is responsible
    for instantiation of all Placements based on a config
    file information
    """
    @staticmethod
    def init_placements(placement_repo: AbsPlacementRepository, config: Iterable[Mapping]):
        """
        Fills the specified PlacementRepository with Placements
        initialized from a config file

        :param placement_repo: an instance of PlacementRepository
               to be filled with instantiated Placements
        :param config: a configuration data to be used for
               instantiation of Placements
        :return: None
        """
        for conf_item in config:
            new_placement = PlacementBuilder.build(conf_item)
            placement_repo.add(new_placement)
