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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests. It may indicate that:

- a client application forgot to set ``Content-Type`` request
  header;
- or ``Content-Type`` header value points to unsupported type of
  content.

This error indicates some issue with the client-side code and should
be fixed by client's developer.

For now only one type of request content is supported and can be
read: ``application/json``. In future additional
content-types may be supported like ``application/xml``. Extra
information about content-types in general can be found on
`Wikipedia <https://en.wikipedia.org/wiki/Media_type>`_ and
`MDN <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type>`_.

.. _error_2:

Error 2: Failed to decode request body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests. It may indicate that:

- a passed request body is not a valid JSON, XML or other file format 
  that was declared in``Content-Type`` header;
- the value of ``Content-Type`` header doesn't correspond to the
  content of request body.

This error indicates some issue with the client-side code and should
be fixed by client's developer.

.. _error_3:

Error 3: Server-side issue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on any request. It may indicate that:

- a request was completely valid but server catched some internal
  error.

In this situation there is nothing to do from the client-side. Please,
contact an administrator of the platform and platform's developers
if needed to resolve this issue.

.. _error_4:

Error 4: Method not allowed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests. It may indicate that:

- a request method like GET, POST, PUT and so own is not supported
  for this resouse (URL, endpoint).

This error indicates some issue with the client-side code and should
be fixed by client's developer. For the full list of available resourses
and corresponding HTTP methods, please take a look in :doc:`./rest_api`
page of documentation.

.. _error_5:

Error 5: Resourse not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests. It may indicate that:

- the specified resourse was deleted, moved or was not existing
  at all.

In case of this error please double-check the specified URL. For
example, you can have a spelling error, an extra slash symbol
or a missing one. If you are sure that the specified URL is valid,
than it means that the corresponding resourse or object was
deleted. This is fine. Just be ready to that.

