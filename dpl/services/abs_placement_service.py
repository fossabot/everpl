from typing import Optional

from dpl.model.domain_id import TDomainId
from dpl.dtos.placement_dto import PlacementDto
from .abs_entity_service import AbsEntityService
from .service_exceptions import ServiceEntityResolutionError, ServiceEntityLinkError


class AbsPlacementService(AbsEntityService[PlacementDto]):
    """
    A base class for all PlacementService implementations
    """
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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()
