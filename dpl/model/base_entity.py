from .domain_id import TDomainId


class BaseEntity(object):
    """
    A declaration of Entity - base class for all Entities of Object
    Model (like Things, Placements and Users)
    """
    def __init__(self, domain_id: TDomainId):
        """
        Constructor. Just saves domain_id to the internal variable

        :param domain_id: an unique identifier of this Entity
        """
        self._domain_id = domain_id

    @property
    def domain_id(self) -> TDomainId:
        """
        Returns an unique identifier of this Entity

        :return: an unique identifier of this Entity
        """
        return self._domain_id
