from dpl.model.domain_id import TDomainId
from dpl.dtos.connection_dto import ConnectionDto
from .abs_entity_service import AbsEntityService


class AbsConnectionService(AbsEntityService[ConnectionDto]):
    """
    A base class for all ConnectionService implementations
    """
    def create_connection(self, *args, **kwargs) -> TDomainId:
        """
        FIXME: METHOD SIGNATURE IS NOT YET DEFINED
        FIXME: !!! DEFINE METHOD SIGNATURE AND PREPARE A RELATED DOCUMENTATION !!!

        :param args: !!! NOT YET DEFINED !!!!
        :param kwargs: !!! NOT YET DEFINED !!!!
        :return:
        """
        raise NotImplementedError()
