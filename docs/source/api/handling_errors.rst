Handling Errors
===============

Unfortunately, always there is something that could go wrong while
processing of API requests. Connection can be lost, token can be
expired, some exception can be unhandled and so on. Stuff happens.
And you must be ready to that.

Here is the complete list of responses for different types of API
errors. Errors are grouped by main platform's subsystems and each
error type has its own identifier.

Error Response Format
---------------------

If some request resulted in an error, than platform instance returns
a response with HTTP status code not less than 400 and JSON-encoded
body with an additional information about an error.

A format of request body is the following:

.. code-block:: json

   {
     "error_id": "int, an identifier of an error",
     "devel_message": "Some message for developers",
     "user_message": "Some message that can be directly displayed to the user",
     "docs_url": "A link to the related section in platform's documentation"
   }

Regarding HTTP status codes:

- codes starting from 400 are error codes;
- codes >= 400 and < 500 indicate client-side errors;
- codes >= 500 indicate server-side errors.

General
-------

.. _error_1000:

Error 1000: Unsupported content-type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

HTTP status code: 400.

.. _error_1001:

Error 1001: Failed to decode request body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests. It may indicate that:

- a passed request body is not a valid JSON, XML or other file format 
  that was declared in ``Content-Type`` header;
- the value of ``Content-Type`` header doesn't correspond to the
  content of request body.

This error indicates some issue with the client-side code and should
be fixed by client's developer.

HTTP status code: 400.

.. _error_1003:

Error 1003: Server-side issue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on any request. It may indicate that:

- a request was completely valid but server caught some internal
  error.

In this situation there is nothing to do from the client-side. Please,
contact an administrator of the platform and platform's developers
if needed to resolve this issue.

HTTP status code: 500.

.. _error_1004:

Error 1004: Method not allowed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests. It may indicate that:

- a request method like GET, POST, PUT and so own is not supported
  for this resource (URL, endpoint).

This error indicates some issue with the client-side code and should
be fixed by client's developer. For the full list of available resources
and corresponding HTTP methods, please take a look in :doc:`./rest_api`
page of documentation.

HTTP status code: 405.

.. _error_1005:

Error 1005: Resource not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests. It may indicate that:

- the specified resource was deleted, moved or was not existing
  at all.

In case of this error please double-check the specified URL. For
example, you can have a spelling error, an extra slash symbol
or a missing one. If you are sure that the specified URL is valid,
than it means that the corresponding resource or object was
deleted. This is fine. Just be ready to that.

HTTP status code: 404.

Authorization and authentication
--------------------------------

This section is related to the errors in authorization and 
authentication processes.

.. _error_2000:

Error 2000: Missing username
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

HTTP status code: 400.

.. _error_2001:

Error 2001: Missing password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

HTTP status code: 400.

.. _error_2002:

Error 2002: Invalid username and password combination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on POST requests on ``/auth`` endpoint. 
It may indicate that:

- the user specified a non-existing username;
- the user specified an invalid password value.

This error indicates some issue from the user-side. In this case please,
help to user to log into system and provide some related suggestions.

HTTP status code: 401.

.. _error_2100:

Error 2100: Missing Authorization header
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests on protected resources. 
It may indicate that:

- the client application forgot to pass an ``Authorization`` header in
  HTTP request;
- the value of this header is null.

This error indicates some issue with the client-side code and should
be fixed by client's developer. You must to pass a non-empty
authorization header while accessing to protected resources. To get
more information about the authorization process, please take a look
into :ref:`protected_resources` section of documentation.

.. WARNING::
   This behaviour may be changed if 'insecure' mode will be introduced.
   Please, take a look in this pull request to get more information:
   `pull#15 <https://github.com/s-kostyuk/adpl/pull/15>`_.

HTTP status code: 400.

.. _error_2101:

Error 2101: Invalid access token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on all requests on protected resources. 
It may indicate that:

- the access token was revoked;
- the access token was invalid from the start.

This error indicates that the access token must to be renewed. In this
case it is recommended to redirect user to authorization page. To get
more information about the authorization process, plese take a look
into :ref:`protected_resources` section of documentation.

.. WARNING::
   This behaviour may be changed if 'insecure' mode will be introduced.
   Please, take a look in this pull request to get more information:
   `pull#15 <https://github.com/s-kostyuk/adpl/pull/15>`_.

HTTP status code: 400.

.. _error_2110:

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

HTTP status code: 403.

Things
------

.. _error_3100:

Error 3100: Not an Actuator
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to send a command on execution
to the Thing. It may indicate that:

- the ``/execute`` sub-resource is not available for this instance;
- this instance isn't capable of command execution.

This error indicates some issue with the client-side code and should
be fixed by client's developer. Do not allow to user to send any
commands to the non-actuator objects.

HTTP status code: 404.

.. _error_3101:

Error 3101: Missing 'command' value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to send a command on execution
to the Thing. It may indicate that:

- the client application forgot to pass a ``command`` value in a
  body of HTTP request;
- the value of this header is not a string (i.e. is a number, null
  or a value of some other type).

This error indicates some issue with the client-side code and should
be fixed by client's developer. You must to pass a valid ``command``
value while sending of commands on execution to Actuators. To get
more information about the ``/execute`` request and its format,
please take a look into :ref:`things_executing_commands` section of
documentation.

HTTP status code: 400.

.. _error_3102:

Error 3102: Missing 'command_args' value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to send a command on execution
to the Thing. It may indicate that:

- the client application forgot to pass a ``command_args`` value in a
  body of HTTP request;
- the value of the ``command_args`` key is not a mapping (dictionary).

This error indicates some issue with the client-side code and should
be fixed by client's developer. You must to pass a valid ``command_args``
value while sending of commands on execution to Actuators. To get
more information about the ``/execute`` request and its format,
please take a look into :ref:`things_executing_commands` section of
documentation.

HTTP status code: 400.

.. _error_3103:

Error 3103: Unacceptable command arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to send a command on execution
to the Thing. It may indicate that:

- the client application forgot to pass some non-optional argument in
  the ``command_args`` field of a body of HTTP request;
- the client application passed an unexpected extra (additional)
  command argument in the ``command_args`` field of a body of HTTP request;
- one of the command arguments haves an invalid type;
- one of the command arguments haves an invalid value.

This error indicates some issue with the client-side code and should
be fixed by client's developer. You must to pass a valid ``command_args``
value while sending of commands on execution to Actuators. To get
more information about the ``/execute`` request and its format,
please take a look into :ref:`things_executing_commands` section of
documentation.

HTTP status code: 400.


Error 3110: Unsupported command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to send a command on execution
to the Thing. It may indicate that:

- the specified instance of Actuator doesn't support the requested
  command.

This error indicates some issue with the client-side code and should
be fixed by client's developer. You must to pass the name of a command
which is supported by the specified Thing instance in ``command``
field in request body. To get more information about the ``/execute``
request and its format, please take a look into
:ref:`things_executing_commands` section of documentation.

HTTP status code: 400.


Placements
----------

There is no Placement-specific exceptions for now.


Streaming API
-------------

Streaming API has its own subset of errors in addition to the errors
defined above. All errors with identifiers starting from ``5000``
and to ``5999`` including are considered as Streaming API-specific
errors.


Error 5000: Timeout
^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to use a Streaming API.
It may indicate that:

- the server was expected to receive a message from a client in the
  specified time window but such message wasn't sent.

This error indicates some issue with the client-side code and should
be fixed by client's developer. In some situations server may wait a
message from a client application in the specified time window (not later
than X time units after some point of time). For example, the client
must to send Authentication message not later than 20 seconds from
the connection establishment (as defined in :doc:`./streaming_api`
section of documentation). You must to send messages in the specified
time windows, otherwise you will receive this (5000) error.


Error 5001: Invalid frame type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to send a frame using a Streaming API.
It may indicate that:

- the frame sent has type that is different from expected.

This error indicates some issue with the client-side code and should
be fixed by client's developer. For now the only supported type of
WebSocket frame is TEXT frame. TEXT frames are then parsed as JSON
objects and interpreted as Streaming API Messages. You must not to use
binary frames or any other frames for transferring Streaming API Messages.


Error 5002: Invalid frame content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to send a frame using a Streaming API.
It may indicate that:

- the content of the specified TEXT frame is not a JSON object.

This error indicates some issue with the client-side code and should
be fixed by client's developer. For now all the messages passed via
Streaming API must to be encoded as JSON objects according to the rules
defined in :doc:`./streaming_api` section of documentation. You must to
encode Messages as JSON objects and transfer them in TEXT WebSocket frames.
Otherwise the mentioned (5002) error will be thrown.


Error 5003: Message format violation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to send a message using a Streaming API.
It may indicate that:

- the received message is a valid JSON object is not a valid Message object;
- some fields of Message are missing or have an appropriate type.

This error indicates some issue with the client-side code and should
be fixed by client's developer. For now all the messages passed via
Streaming API must to be encoded as JSON objects according to the rules
defined in :doc:`./streaming_api` section of documentation. You must to
encode Messages as JSON objects and transfer them in TEXT WebSocket frames.
Otherwise the mentioned (5003) error will be thrown.

The name of erroneous field is specified in ``devel_message`` field of Error
message.


Error 5010: Invalid message type (not Control)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to use a Streaming API.
It may indicate that:

- the server was expected to receive a Control Message from a
  client but the message received is not a Control Message.

This error indicates some issue with the client-side code and should
be fixed by client's developer. In some situations server may wait a
message from a client application with the specified type: either
Control Message or Data Message. To define either the received Message
is Control or Data Message, the ``type`` field is used according
to the :doc:`./streaming_api` section of documentation. You must
to send messages with a type, appropriate to the current situation,
otherwise you will receive this (5010) error.


Error 5011: Invalid message type (not Data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to use a Streaming API.
It may indicate that:

- the server was expected to receive a Data Message from a
  client but the message received is not a Data Message.

This error indicates some issue with the client-side code and should
be fixed by client's developer. In some situations server may wait a
message from a client application with the specified type: either
Control Message or Data Message. To define either the received Message
is Control or Data Message, the ``type`` field is used according
to the :doc:`./streaming_api` section of documentation. You must
to send messages with a type, appropriate to the current situation,
otherwise you will receive this (5011) error.


Error 5020: Invalid message topic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to use a Streaming API.
It may indicate that:

- the server was expected to receive a Message with the specified
  topic from a client but the topic of the received message is
  different from expected.

This error indicates some issue with the client-side code and should
be fixed by client's developer. In some situations server may wait a
message from a client application with the specified topic. You must
to send messages with a topic, appropriate to the current situation,
otherwise you will receive this (5020) error. To define what message
topic is expected in the current situation, please refer to the
:doc:`./streaming_api` section of documentation. The expected topic
of a message is defined in ``devel_message`` field of Error message.


Error 5030: Invalid message body content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can be thrown on attempts to use a Streaming API.
It may indicate that:

- the server expected to find some information in a body content
  of received message but such information is missing or is invalid
  (by type or value).

This error indicates some issue with the client-side code and should
be fixed by client's developer. In some situations client must to send
messages with the specified type, topic and the message body content.
You must to send messages with bodies as defined in the
:doc:`./streaming_api` section of documentation, otherwise
you will receive this (5030) error. The name of the missing or
erroneous field is defined in ``devel_message`` field of Error message.
