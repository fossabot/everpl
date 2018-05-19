"""
This module contains definition of Track Info capability
"""


class TrackInfo(object):
    """
    Track Info devices are devices that can display information about the
    current playing media. The type of this information can be arbitrary
    and is not specified by this document. It's not even supposed to be
    parsed by other devices. The only thing that must to be granted is that
    the track_info field value must to be human-readable without any additional
    processing.

    For support of information about the song name, movie name, artists,
    current playing TV program and so on please refer to the corresponding
    Capabilities and Thing types.
    """
    _capability_name = 'track_info'

    @property
    def track_info(self) -> str:
        """
        Returns an information about a current playing song, movie,
        stream or another media in a form of a single human-readable
        string.

        :return: an information about a current playing song, movie, stream
                 or another media
        """
        raise NotImplementedError()
