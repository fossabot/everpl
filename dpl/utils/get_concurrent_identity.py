"""
This module contains an implementation of some logic
that will allow to get a unique identifier of current
thread or asynchronous task that is currently executed.

Such ability allows to distinguish different concurrent
processes and, for example, to control access to some
unique non-sharable resources.

The following code was inspired by a one available by this link:
https://docs.atlassian.com/aiolocals/latest/_modules/aiolocals/local.html
"""


import asyncio
import threading


def get_concurrent_identity():
    """
    Allows to get some identifier which can be used to
    distinguish different threads and their asynchronous
    tasks one from each other

    :return: some identifier of the current asynchronous
             task in process or of the current running
             thread if called not from a asynchronous Task
    """
    current_task = asyncio.Task.current_task()

    if current_task is None:
        identity = threading.current_thread().ident
    else:
        identity = id(current_task)

    return identity
