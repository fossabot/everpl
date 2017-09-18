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

.. _error_1000:

Error 1000: Unsupported content-type
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

.. _error_1001:

Error 1001: Failed to decode request body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests. It may indicate that:

- a passed request body is not a valid JSON, XML or other file format 
  that was declared in``Content-Type`` header;
- the value of ``Content-Type`` header doesn't correspond to the
  content of request body.

This error indicates some issue with the client-side code and should
be fixed by client's developer.

.. _error_1003:

Error 1003: Server-side issue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on any request. It may indicate that:

- a request was completely valid but server catched some internal
  error.

In this situation there is nothing to do from the client-side. Please,
contact an administrator of the platform and platform's developers
if needed to resolve this issue.

.. _error_1004:

Error 1004: Method not allowed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests. It may indicate that:

- a request method like GET, POST, PUT and so own is not supported
  for this resource (URL, endpoint).

This error indicates some issue with the client-side code and should
be fixed by client's developer. For the full list of available resources
and corresponding HTTP methods, please take a look in :doc:`./rest_api`
page of documentation.

.. _error_1005:

Error 1005: Resource not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests. It may indicate that:

- the specified resource was deleted, moved or was not existing
  at all.

In case of this error please double-check the specified URL. For
example, you can have a spelling error, an extra slash symbol
or a missing one. If you are sure that the specified URL is valid,
than it means that the corresponding resource or object was
deleted. This is fine. Just be ready to that.

Authorization and authentication
-------

This section is related to the errors in authorization and 
authentification processes.

.. _error_2000:

Error 2000: Missing username
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests on ``/auth`` endpoint. 
It may indicate that:

- a client application forgot to pass 'username' field in request body;
- a client application passed a username that is equal to null.

This error indicates some issue with the client-side code and should
be fixed by client's developer. Do not allow to user to send an empty
username field.

.. WARNING::
   This behaviour may be changed if 'insecure' mode will be introduced.
   Please, take a look in this pull request to get more information:
   `pull#15 <https://github.com/s-kostyuk/adpl/pull/15>`_.

.. _error_2001:

Error 2001: Missing username
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests on ``/auth`` endpoint. 
It may indicate that:

- a client application forgot to pass 'password' field in request body;
- a client application passed a password that is equal to null.

This error indicates some issue with the client-side code and should
be fixed by client's developer. Do not allow to user to send an empty
password field.

.. WARNING::
   This behaviour may be changed if 'insecure' mode will be introduced.
   Please, take a look in this pull request to get more information:
   `pull#15 <https://github.com/s-kostyuk/adpl/pull/15>`_.

.. _error_2002:

Error 2002: Invalid username and password combination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests on ``/auth`` endpoint. 
It may indicate that:

- the user specified a non-existing username;
- the user specified an invalid password value.

This error indicates some issue from the user-side. In this case please,
help to user to log into system and provide some related suggestions.

.. _error_2100:

Error 2100: Missing Authorization header
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests on protected resources. 
It may indicate that:

- the client application forgot to pass an ``Authorization`` header in
  HTTP request;
- the value of this header is null.

This error indicates some issue with the client-side code and should
be fixed by client's developer. You must to pass a non-empty
authorization header while accessing to protected resources. To get
more information about the authorization process, please take a look
into FIXME section of documentation.

.. WARNING::
   This behaviour may be changed if 'insecure' mode will be introduced.
   Please, take a look in this pull request to get more information:
   `pull#15 <https://github.com/s-kostyuk/adpl/pull/15>`_.

.. _error_2101:

Error 2101: Invalid access token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests on protected resources. 
It may indicate that:

- the access token was revoked;
- the access token was invalid from the start.

This error indicates that the access token must to be renewed. In this
case it is recommended to redirect user to authorization page. To get
more information about the authorization process, plese take a look
into FIXME section of documentation.

.. WARNING::
   This behaviour may be changed if 'insecure' mode will be introduced.
   Please, take a look in this pull request to get more information:
   `pull#15 <https://github.com/s-kostyuk/adpl/pull/15>`_.

Error 2110: Permission Denied
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests on protected resources. 
It may indicate that:

- the user doesn't have an access to this resource;
- the user doesn't have a permission to modify this resource;
- the specified access token doesn't permit to process this 
  request for some other reason.

This error indicates that the user doesn't have an access to this
resource for some reason. There is nothing to do from the client-
side. In this situation please describe what was happened to user
and help him/her to contact an administrator of platform's instance
and to get a corresponding rights.

.. WARNING::
   This behaviour may be changed if 'insecure' mode will be introduced.
   Please, take a look in this pull request to get more information:
   `pull#15 <https://github.com/s-kostyuk/adpl/pull/15>`_.

Things
-------

FIXME

Placements
-------

FIXME