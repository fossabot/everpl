class LastUpdated(object):
    """
    LastUpdated capability allows to determine a moment
    in time when the properties of a Thing was altered
    for the last time.
    """
    @property
    def last_updated(self) -> float:
        """
        Returns a timestamp of the last thing state update

        :return: float, UNIX time
        """
        raise NotImplementedError()
