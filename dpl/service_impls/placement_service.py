import uuid
from typing import Optional

from dpl.model.domain_id import TDomainId
from dpl.placements.placement import Placement
from dpl.dtos.placement_dto import PlacementDto
from dpl.dtos.dto_builder import build_dto
from dpl.services.abs_placement_service import AbsPlacementService, \
    ServiceEntityResolutionError, ServiceEntityLinkError

from dpl.repos.abs_placement_repository import AbsPlacementRepository
from .base_service import BaseService


class PlacementService(AbsPlacementService, BaseService[PlacementDto]):
    """
    This is an implementation of a PlacementService -
    a class that manages all Placements in the system
    """

    def __init__(self, placement_repo: AbsPlacementRepository):
        """
        Constructor. Receives an instance of PlacementRepository
        which will be used to store all Placements and fetch them

        :param placement_repo: an instance of a PlacementRepository
        """
        self._placements = placement_repo

    def view_all(self):  # -> Collection[PlacementDto]:
        """
        Fetch a full list of DTOs of all stored objects

        :return: a collection of DTOs
        """
        return [
            build_dto(i) for i in self._placements.load_all()
        ]

    def view(self, domain_id: TDomainId) -> PlacementDto:
        """
        Fetch a DTO of stored object by the ID specified

        :param domain_id: id of object to be fetched
        :return: a DTO of stored object
        :raises ServiceResolutionError: if the entity with
                the specified ID can't be found
        """
        placement = self._placements.load(domain_id)

        if placement is None:
            raise ServiceEntityResolutionError(
                "A Placement with the specified ID can't "
                "be found: %s" % domain_id
            )

        return build_dto(placement)

    def remove(self, domain_id: TDomainId) -> None:
        """
        REMOVES an Entity with the specified ID altogether
        from the system

        :param domain_id: an identifier of Entity to be deleted
        :return: None
        :raises ServiceResolutionError: if the entity with
                the specified ID can't be found
        :raises ServiceEntityLinkError: if the specified can't
                be removed because some other entity is linked
                (uses or refers) to it
        """
        # FIXME: Handle exceptions caused by resolution errors
        # FIXME: Handle exceptions caused by link breakages
        self._placements.delete(domain_id)

    def create_placement(self, friendly_name: Optional[str], image_url: Optional[str]) -> TDomainId:
        """
        Create a new placement with the specified name
        and an attached image

        :param friendly_name: a human-friendly name or title
               for the new Placement
        :param image_url: a URL for an image associated with
               this Placement
        :return: a unique identifier of the created Placement
        """
        new_id = uuid.uuid4()
        domain_id = new_id.hex

        assert isinstance(domain_id, TDomainId)

        new_placement = Placement(domain_id, friendly_name, image_url)
        self._placements.add(new_placement)

        return domain_id

    def change_name(self, placement_id: TDomainId, new_name: Optional[str]) -> None:
        """
        Sets a new friendly_name value for a Placement with
        the specified identifier

        :param placement_id: an identifier of the Placement to
               be altered
        :param new_name: the new value of friendly_name field
               to be set
        :return: None
        :raises ServiceEntityResolutionError: if a Placement
                with the specified ID wasn't found
        """
        placement = self._resolve_entity(
            repository=self._placements,
            domain_id=placement_id
        )

        # FIXME: Handle validation errors
        placement.friendly_name = new_name

    def change_image_url(self, placement_id: TDomainId, new_image_url: Optional[str]) -> None:
        """
        Sets a new image_url value for a Placement with
        the specified identifier

        :param placement_id: an identifier of the Placement to
               be altered
        :param new_image_url: the new value of image_url field
               to be set; an address of a new image to be
               associated with this Placement
        :return: None
        :raises ServiceEntityResolutionError: if a Placement
                with the specified ID wasn't found
        """
        placement = self._resolve_entity(
            repository=self._placements,
            domain_id=placement_id
        )

        # FIXME: Handle validation errors
        placement.image_url = new_image_url
