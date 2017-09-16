Handling Errors
===============

Unfortunately, always there is something that could go wrong while
processing of API requests. Connection can be lost, token can be
expired, some exception can be unhandled and so on. Stuff happens.
And you must be ready to that.

Here is the complete list of responses for different types of API
errors. Errors are grouped by main platform's subsystems and each
error type has its own identifier.

General
-------

.. _error_1:

Error 1: Unsupported content-type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests. It may indicate that:

- a client application forgot to set ``Content-Type`` request
  header;
- or ``Content-Type`` header value points to unsupported type of
  content.

For now only one type of request content is supported and can be
read: ``application/json``. In future additional
content-types may be supported like ``application/xml``. Extra
information about content-types in general can be found on
`Wikipedia <https://en.wikipedia.org/wiki/Media_type>`_ and
`MDN <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type>`_.

.. _error_2:

Error 1: Unsupported content-type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests. It may indicate that:

- a client application forgot to set ``Content-Type`` request
  header;
- or ``Content-Type`` header value points to unsupported type of
  content.

For now only one type of request content is supported and can be
read: ``application/json``. In future additional
content-types may be supported like ``application/xml``. Extra
information about content-types in general can be found on
`Wikipedia <https://en.wikipedia.org/wiki/Media_type>`_ and
`MDN <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type>`_.

.. _error_3:

Error 1: Unsupported content-type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests. It may indicate that:

- a client application forgot to set ``Content-Type`` request
  header;
- or ``Content-Type`` header value points to unsupported type of
  content.

For now only one type of request content is supported and can be
read: ``application/json``. In future additional
content-types may be supported like ``application/xml``. Extra
information about content-types in general can be found on
`Wikipedia <https://en.wikipedia.org/wiki/Media_type>`_ and
`MDN <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type>`_.
