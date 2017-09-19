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

The ``BASE_URL`` may look like this: ``http://localhost:10800/api/v1/``

or like this: ``https://hostname.local/api/v1/``

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
a special access token. Then this token must to be passed in
``Authorization`` HTTP header on each request to protected resource.

The process of obtaining of access token is described in
`Authentication`_ section. Related error responses are described in
:doc:`./handling_errors` section of documentation.

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

Things
------

Thing is a sort of basic concept in platform. Thing represent some item
of the system, i.e. some physical device or software application.

Thing object
^^^^^^^^^^^^

General thing object has the following structure:

:commands:
    A list of commands that can be sent to this Thing

:is_active:
    A boolean field that indicates if this Thing is in one of the
    'active' states (like 'playing' for player or 'on' for lighting).

:is_available:
    A boolean field that indicates if this Thing is available for
    communication (like fetching data, updating Things state and
    sending commands).

:last_updated:
    A floating-point value, UNIX time that indicates the
    time of latest update (of state field or any other field)

:state:
    A string, indicates the current state of Thing (type-specific).
    For example, for lighting it can take on the following values:
    'on', 'off' and 'unknown'.

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

:description:
    .. WARNING::
        Deprecation pending

    Some description of a thing.

The exact set of fields and their values may vary for different types
of things. For detailed information, please refer to the FIXME section
of documentation.

Example of Thing object:

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
        "placement": "R2",
        "description": "Kitchen cooker hood"
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


Placements
----------

Placement is a some static position in a building / city / other area.
In homes it usually corresponds to one room.

Placement object
^^^^^^^^^^^^^^^^

Placement object has the following structure:

:id:
    A list of commands that can be sent to this Thing

:friendly_name:
    Some user-friendly name of this particular placement that can be
    modified and directly displayed to user.

:image_url:
    A URL to related picture of this placement (room).

:description:
    .. WARNING::
        Deprecation pending

    Some description of a placement.

:image:
    .. WARNING::
        Deprecation pending

    A URL to related picture of this placement (room).

Example of Placement object:

.. code-block:: json

    {
        "id": "R1",
        "friendly_name": "Corridor",
        "image_url": "http://www.gesundheittipps.net/wp-content/uploads/2016/02/Flur_547-1024x610.jpg",
        "description": "Corridor",
        "image": "http://www.gesundheittipps.net/wp-content/uploads/2016/02/Flur_547-1024x610.jpg"
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
