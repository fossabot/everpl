REST API
========

General information
-------------------

REST API is the base external API that is provided by platform.
It is recommended to use with unstable network connections, for
getting of access tokens and for occasional updates of resource
statuses. For receiving of instant notifications on resource
updates please take a look in :doc:`./streaming_api` section of
documentation.

In this documentation you will also find such value as ``BASE_URL``.
The ``BASE_URL`` is a value that points to the base URL of REST API.
It consists of protocol specification (http or https), hostname or
an IP address of platform instance, port and the rest of REST API
path. Keep in mind that the hostname and port of platform instance
can be changed in various circumstances (like ip address renewal,
moving between different networks and so on).

The ``BASE_URL`` always look like:
``protocol://domain:port/api/rest/v1``

Where:

- ``protocol`` is either ``http`` or ``https`` for unsecured and
  secured (TLS) HTTP connection;
- ``domain`` is a fully-qualified domain name or IP address of evepl
  instance you are connecting to;
- ``port`` is a port used for HTTP connection;
- ``api/rest/`` is a constant part of an address;
- ``v1`` indicates the currently used version of the REST API.

.. _protected_resources:

Protected resources
-------------------

There are two types of API resources in the platform:

- protected;
- and unprotected.

Protected resources are resources that can be viewed or modified only
by an authorized user. Unprotected resources are resources that can be
accessed by any user, including anonymous users.

To access protected resources you will need to authenticate and obtain
a special access token [#f1]_. Then this token must to be passed in
``Authorization`` HTTP header on each request to protected resource.

The process of obtaining of access token is described in
`Authentication`_ section. Related error responses are described in
:doc:`./handling_errors` section of documentation.
Possible errors: 2100, 2101, 2110.

Authentication
--------------

As was mentioned in the previous section, you need to obtain an access
token to read or modify protected resources (which are the majority of
resources). An access token itself is a unique secret alphanumeric
string that is specific exactly to one user on exactly one client
application instance. As a usual username-password combination it
allows to uniquely identify the user and to perform all operations on
his or her behalf. So threat it with care and store securely.

To retrieve an access token you need to send user credentials on
``/auth`` endpoint in POST request.

:URL structure:
    ``BASE_URL/auth``

:Method:
    ``POST``

:Headers:
    :Content-Type: ``application/json``

:Request Body:
    .. code-block:: json

        {
            "username": "your_username_here",
            "password": "your_password_here"
        }

In a case of success you will get the similar response:

:Status Code:
    200

:Headers:
    :Content-Type: ``application/json``

:Response Body:
    .. code-block:: json

        {
            "message": "authorized",
            "token": "90ff4ba085545c1735ab6c29a916f9cb8c0b7222"
        }

In a case of authentication error you will receive one of the responses
listed in :doc:`./handling_errors` section of documentation.
Possible errors: 1000, 1001, 1003, 2000, 2001, 2002.

Things
------

Thing is a sort of basic concept in platform. Thing represent some item
of the system, i.e. some physical device or software application.

Thing object
^^^^^^^^^^^^

General thing object has the following structure:

:capabilities:
    A list of Capabilities, supported by this Thing. For more
    information see :doc:`/developer/capabilities` section of
    documentation.

:is_available:
    A boolean field that indicates if this Thing is available for
    communication (like fetching data, updating Things state and
    sending commands).

:last_updated:
    A floating-point value, UNIX time that indicates the
    time of latest update (of state field or any other field)

:friendly_name:
    Some user-friendly name of this particular thing that can be
    modified and directly displayed to user.

:type:
    Some type-related information. Its format is still unstable.

:id:
    A string (for now), some machine-friendly unique identifier of
    specific thing.

:placement:
    A string (for now), an identifier of placement where this Thing
    is currently placed (positioned). See `Placements`_ section for
    detailed information about placements.


Meanwhile, Actuator Things usually (but not always [#f2]_) provide some
additional fields:

:commands:
    A list of commands that can be sent to this Thing

:is_active:
    A boolean field that indicates if this Thing is in one of the
    'active' states (like 'playing' for player or 'on' for lighting).

:state:
    A string, indicates the current state of Thing (type-specific).
    For example, for lighting it can take on the following values:
    'on', 'off' and 'unknown'.


The exact set of fields and their values may vary for different types
of things. For detailed information, please refer to the
:doc:`/developer/capability_list` and :doc:`/developer/generic_thing_types`
sections of documentation.

Example of an Actuator Thing object:

.. code-block:: json

    {
        "commands": [
            "activate",
            "deactivate",
            "toggle",
            "on",
            "off"
        ],
        "is_active": false,
        "is_available": true,
        "last_updated": 1505768807.4725718,
        "state": "unknown",
        "friendly_name": "Kitchen cooker hood",
        "type": "switch",
        "id": "F1",
        "placement": "R2"
    }


Fetching all Things
^^^^^^^^^^^^^^^^^^^

To fetch all Things, you need to perform the following request:

:URL structure:
    ``BASE_URL/things/``

:Parameters:
    :placement:
        Enables filtering of things by placement. Use it like
        ``?placement=R1`` to get a list of things positioned in
        ``R1`` placement.

    :type:
        Enables filtering of things by their type. Use it like
        ``?type=lighting`` to get a list of things that have a
        type of ``lighting``.

:Method:
    ``GET``

:Headers:
    :Authorization: ``your_auth_token_here``

An example of response body is placed here: https://git.io/v5xz3.

Fetching specific Thing
^^^^^^^^^^^^^^^^^^^^^^^

To fetch a specific Thing, you need to perform the following request:

:URL structure:
    ``BASE_URL/things/{id}``

:Method:
    ``GET``

:Headers:
    :Authorization: ``your_auth_token_here``

:Notes:
    Replace ``{id}`` part of the URL with an identifier of requested
    Thing object.


.. _things_executing_commands:

Sending commands to a Thing
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Starting from the v0.3 of everpl it's possible to send commands to
the Actuators - to the Things that are able to execute some commands.

Each command can have its own set of arguments, the list of the allowed
commands is specified in the ``commands`` field for each Actuator Thing.
The list of available commands and their set of possible arguments is
determined by the list of capabilities implemented by the specified Thing.

To send a command to an Actuator Thing you need to send a POST request
using an ``/execute`` sub-resource of a Thing in question:

:URL structure:
    ``BASE_URL/things/{id}/execute``

:Method:
    ``POST``

:Headers:
    :Authorization: ``your_auth_token_here``
    :Content-Type: ``application/json``

:Request Body:
    .. code-block:: json

        {
	        "command": "the_name_of_the_command",
	        "command_args": {}
        }

:Notes:
    Replace ``{id}`` part of the URL with an identifier of requested
    Thing object.

The presence of the both ``command`` and ``command_args`` fields is mandatory.

The value of the ``command`` field must to be a string - the name of the
command to be executed; this value is must to be an element from the
``commands`` field of the specified Thing.

The value of the ``command_args`` field must to be a dictionary of keyword-
arguments for the command with keys as strings and values as specified in
the Thing's documentation. It's allowed to pass an empty dictionary as the
value of the ``command_args`` field if there is no additional arguments needed
for an execution of the specified command.

In a case of success your command will be send on execution and you will get
a similar response:

:Status Code:
    202

:Headers:
    :Content-Type: ``application/json``

:Response Body:
    .. code-block:: json

        {
	        "message": "accepted"
        }

In a case of an pre-execution (validation) error you will receive
one of the responses listed in :doc:`./handling_errors` section of
documentation. Possible errors: 1000, 1001, 1003, 1005, 2100, 2101,
2110, 3100, 3101, 3102, 3103, 3110.


Placements
----------

Placement is a some static position in a building / city / other area.
In homes it usually corresponds to one room.

Placement object
^^^^^^^^^^^^^^^^

Placement object has the following structure:

:id:
    A string (for now), some machine-friendly unique identifier of
    specific thing.

:friendly_name:
    Some user-friendly name of this particular placement that can be
    modified and directly displayed to user.

:image_url:
    A URL to related picture of this placement (room).

Example of Placement object:

.. code-block:: json

    {
        "id": "R1",
        "friendly_name": "Corridor",
        "image_url": "http://www.gesundheittipps.net/wp-content/uploads/2016/02/Flur_547-1024x610.jpg"
    }

Fetching all Placements
^^^^^^^^^^^^^^^^^^^^^^^

To fetch all Placements, you need to perform the following request:

:URL structure:
    ``BASE_URL/placements/``

:Method:
    ``GET``

:Headers:
    :Authorization: ``your_auth_token_here``

An example of response body is placed here: https://git.io/v5x6S.

Fetching specific Placement
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To fetch a specific Placement, you need to perform the following
request:

:URL structure:
    ``BASE_URL/placements/{id}``

:Method:
    ``GET``

:Headers:
    :Authorization: ``your_auth_token_here``

:Notes:
    Replace ``{id}`` part of the URL with an identifier of requested
    Placement object.


.. rubric:: Footnotes

.. [#f1] See also: `Access token definition in OAuth specs
         <https://tools.ietf.org/html/rfc6749#section-1.4>`_

.. [#f2] Only the presence of ``commands`` field is granted for
   Actuators. For more information about available fields please
   refer to the :doc:`/developer/capabilities` section of documentation.
