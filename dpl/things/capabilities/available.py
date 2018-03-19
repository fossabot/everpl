class Available(object):
    """
    Instances which provide Available capability provides
    their availability status: is they are available for
    communication or not - i.e. they are explicitly disabled
    (see Enabled capability), lost, faulted, have a
    discharged battery and so on).
    """
    @property
    def is_available(self) -> bool:
        """
        Availability of thing for usage and communication

        :return: True if Thing is available, False otherwise
        """
        raise NotImplementedError()
