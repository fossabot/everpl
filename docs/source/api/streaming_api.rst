Streaming API
=============

Starting from v0.4.0 of everpl the new type of API is provided:
the Streaming API.

The streaming API allows to receive updates of system objects
(like Things), push notifications and other system events in real-time:
just after such events had happened. And more of it: client applications
are able to choose what events they are concerned about and what events
they wanna subscribe to.

.. WARNING::
    The information below is a **draft** of specification. **Any**
    part of this document may be **changed** without notice.


General Information
-------------------

For now the Streaming API is implemented over WebSocket two-way
communication protocol [#f1]_. Once WebSocket connection is established and
authorization procedure was complete, an everpl instance and a client
application instance are allowed to send messages to each other.

The format of such messages is described in the next section.


Message Format
--------------

Message is a JSON object, transmitted as a Text data frame [#f2]_
over WebSocket connection. Generally any Message consists of the
specified fields:

:timestamp:
    float, the moment of time when this message was generated,
    formatted as a UNIX time number (i.e. number of seconds
    passed from 1 January 1970 UTC).

:topic:
    string, a topic of this message (described in detail below).

:body:
    Another JSON object. The type and format of this object is
    dependent on a topic of the message.


Message topics allow to group messages by... topics. By types of
the messages they belong to, by type of the event they describe.
For example, there can be topics for each object in the system,
the group of messages notifying about object creation, deletion
or updates. Or there is a topic for some push notifications, that
must to be delivered to user (for example, that might be notifications
about a detected motion in a building or about a critical issue in the
system). And so on.

The content of the message body is greatly dependent on a topic.
Each topic is allowed to specify its own set of available fields
that will carry an additional information about what exactly
happened in the system or what to do with that.


Topics and subscriptions
------------------------

Topic is a string of the following format: ``topic/subtopic/subtopic``

Each topic has a hierarchical structure:

- the first part (topic layer; ``topic`` in example) is root topic
  for that category of messages;
- the second and the following parts are sub-topics, sub-categories
  of messages.

Topic layers are separated between each other with a forward slash
sign (``/``; the topic layer separator). The number of such
topic layers is unlimited in theory, but in practice rarely exceeds
the number of three. Please note, that there is no slash at
the beginning of the topic.

All topics are case-sensitive, so such strings as ``my_topic`` and
``My_topic`` correspond to the entirely different topics.

Topic subscriptions
^^^^^^^^^^^^^^^^^^^

As was mentioned earlier, once WebSockets connection is established,
client applications are able to subscribe to different topics.

To subscribe to a topic, a client application must to send the
following message:

.. code-block:: json

    {
        "timestamp": 123456.76,
        "topic": "stream/subscribe",
        "body": {
            "target_topic": "here/is/your/topic"
        }
    }

Where:

- ``topic`` value is constantly equal to ``stream/subscribe``;
- ``timestamp`` is set to the current UNIX time (``123456.76`` on example);
- ``target_topic`` value is set the topic you want to subscribe onto
  (``here/is/your/topic`` on example).


In response to that message you will receive the following message
with an empty body:

.. code-block:: json

    {
        "timestamp": 123456.76,
        "topic": "stream/subscribe_ack",
        "body": {}
    }

.. WARNING::
    All your subscriptions are **not** saved automatically between
    sessions. If you will be disconnected from a server by any
    reason, then you will need to start from scratch and subscribe
    on each of the needed topics again.


Wildcard subscriptions
^^^^^^^^^^^^^^^^^^^^^^

In addition to the individual per-topic subscriptions, you are able
to subscribe to several topics at once. To do so, you have a pair
of additional operators: ``+`` and ``#``.

The ``+`` operator is equal to the "any name on this level of hierarchy"
meaning. For example, if you will subscribe to the ``things/+/updated``
topic, then you will receive messages from topics like
``things/door1/updated``, ``things/player1/updated`` but that doesn't
means that you will receive messages from topics like
``placements/place1/updated``, ``things/player1/updated``, ``things`` or
others automatically.

The ``#`` operator can be present only as the last symbol in the topic
string and means "subscribe to all messages with topics below the
specified level of hierarchy". For example, ``things/#`` allows to
subscribe to any updates (creation, deletion and modification) of any
Thing in the system (topics like ``things/door1/updated``,
``things/player1/updated`` and ``things/door1/deleted``).
And such subscriptions as ``things/player1/#`` allows to watch for
all updates of a specific Thing in the system.

Please note that such operator as ``*`` and partial match topics
like ``things/pla*er1/updated`` are **not** supported by the platform.
Such strings as ``topic/subtopic/foo+``, ``topic/subtopic/foo+bar``,
``topic/#/subtopic`` and ``topic/subtopic/+foo`` are also considered
invalid.


Unsubscribe from a topic
^^^^^^^^^^^^^^^^^^^^^^^^

To unsubscribe to a topic, a client application must to send the
following message:

.. code-block:: json

    {
        "timestamp": 123456.76,
        "topic": "stream/unsubscribe",
        "body": {
            "target_topic": "here/is/your/topic"
        }
    }

Where:

- ``topic`` value is constantly equal to ``stream/subscribe``;
- ``timestamp`` is set to the current UNIX time (``123456.76`` on example);
- ``target_topic`` value is set the topic you want to unsubscribe from
  (``here/is/your/topic`` on example).


In response to that message you will receive the following message
with an empty body:

.. code-block:: json

    {
        "timestamp": 123456.76,
        "topic": "stream/unsubscribe_ack",
        "body": {}
    }


Authentication
--------------

Authentication is performed just after WebSocket connection was
established. To perform an authentication, you need to send your
access token [#f3]_ in the following message:

.. code-block:: json

    {
        "timestamp": 123456.76,
        "topic": "stream/auth",
        "body": {
            "access_token": "here_is_your_token"
        }
    }

Where:

- ``topic`` value is constantly equal to ``stream/auth``;
- ``timestamp`` is set to the current UNIX time (``123456.76`` on example);
- ``access_token`` value is set the your access token to be used
  (``here_is_your_token`` on example).

In response to that message you will receive the following message
with an empty body:

.. code-block:: json

    {
        "timestamp": 123456.76,
        "topic": "stream/auth_ack",
        "body": {}
    }

Once authenticated, you are able to transmit other messages as
described on this page.


Handling Errors
---------------

If there is any error happened in communication, you will receive
a special message with a topic ``stream/error``. Such messages have
the following format:

:timestamp:
    float, the moment of time when this message was generated,
    formatted as a UNIX time number (i.e. number of seconds
    passed from 1 January 1970 UTC).

:topic:
    string, constantly set to the ``stream/error``.

:body:
    Another JSON object. Information about an error in the format
    described in the :doc:`./handling_errors` section of documentation.

Error messages share the common error codes and a format of a body
as described in :doc:`./handling_errors` section of documentation.
So, it's recommended to use the same error handling code for both
Streaming API and REST API errors if possible.

Here is an example of an error message:

.. code-block:: json

    {
        "timestamp": 123456.76,
        "topic": "stream/error",
        "body": {
            "error_id": 2101,
            "devel_message": "Invalid access token",
            "user_message": "Access token was revoked. Please, authenticate."
        }
    }


Message Types
-------------

As was mentioned earlier, there can be different types of messages
with different message bodies for different topics. We already
talked about three special types of messages: error messages
(`Handling Errors`_), authentication (Authentication_)
and subscription (`Topics and subscriptions`_) messages.

Below is a small recap of special message types and a description of
some general message types.

Special Message Types
^^^^^^^^^^^^^^^^^^^^^

1. ``stream/error``
    Indicates an error in communication using Streaming API,
    described above in the `Handling Errors`_ section of
    documentation.

2. ``stream/subscribe``
    Allows streaming client to subscribe on a specific topic.
    Described above in the `Topic subscriptions`_ section of
    documentation.

3. ``stream/subscribe_ack``
    An acknowledgement packet, sent by a server on successful
    subscription. Described above in the `Topic subscriptions`_
    section of documentation.

4. ``stream/unsubscribe``
    Allows streaming client to unsubscribe from a specific topic.
    Described above in the `Unsubscribe from a topic`_ section of
    documentation.

5. ``stream/unsubscribe_ack``
    An acknowledgement packet, sent by a server if the subscription
    was successfully cancelled. Described above in the
    `Unsubscribe from a topic`_ section of documentation.

Object-Related Messages
^^^^^^^^^^^^^^^^^^^^^^^

Object-Related messages are responsible for notification of client
application about the created, updated or deleted objects in the
system. All of such messages has the following structure:

:timestamp:
    float, the moment of time when this message was generated,
    formatted as a UNIX time number (i.e. number of seconds
    passed from 1 January 1970 UTC).

:topic:
    string, topic in the following format:
    ``{object_category}/{object_id}/{what_happened}``.

:body:
    Another JSON object. The DTO of the modified object or ``null``
    if the specified object was deleted.

Where:

- ``{object_category}`` is one of the following values:
  ``things``, ``placements``, ``users`` for Things, Placements
  and Users correspondingly [#f4]_;
- ``{object_id}`` is a unique identifier of the specified object;
- ``{what_happened}`` is one of the following values:
  ``created``, ``updated``, ``deleted`` for messages about the
  created, updated and deleted objects correspondingly;
- the body contents the current state of an object in a
  corresponding format [#f4]_.

So here is an example of such message:

.. code-block:: json

    {
        "timestamp": 1505768807.4725718,
        "topic": "things/F1/updated",
        "body": {
            "commands": ["activate", "deactivate", "toggle", "on", "off"],
            "is_active": false,
            "is_available": true,
            "last_updated": 1505768807.4725718,
            "state": "unknown",
            "friendly_name": "Kitchen cooker hood",
            "type": "switch",
            "id": "F1",
            "placement": "R2"
        }
    }

Notifications
^^^^^^^^^^^^^

Notifications are messages that are supposed to be directly showed
to the user of a client application. They have the following format:

:timestamp:
    float, the moment of time when this message was generated,
    formatted as a UNIX time number (i.e. number of seconds
    passed from 1 January 1970 UTC).

:topic:
    string, constantly set to ``notifications``.

:body:
    Another JSON object. Contains the following fields:

    :title:
        string, a title of the notification

    :text:
        string, an optional field, text to be displayed in notification

    :image_url:
        string, an optional field, a link to the image to be displayed
        in notification

Where optional fields can be omitted (absent) or set to ``null``.


.. WARNING::
    Maybe such field as "urgency" or other fields must to be added?


P.S.
----

If any of the information above reminded you MQTT protocol - it is
no accident. The topic format was greatly inspired by the one in
MQTT protocol. But other things (like the authorization and
subscription procedures, the set of provided features and
underlying implementation) are different.


.. rubric:: Footnotes

.. [#f1] WebSocket protocol is fully documented in
   `RFC 6455 <https://tools.ietf.org/html/rfc6455>`_

.. [#f2] About Text data frames in the WebSocket protocol:
   `RFC 6455 Section 5.6 <https://tools.ietf.org/html/rfc6455#section-5.6>`_

.. [#f3] About how to get an access token is described in :doc:`./rest_api`
   section of documentation, Authentication sub-section.

.. [#f4] Information about all that types of objects can be found at the
   :doc:`./rest_api` section of documentation in corresponding sub-sections.
