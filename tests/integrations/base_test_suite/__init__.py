"""
Base test suite module is a set of generic tests for platform-
specific implementations of Thing-related interfaces (like Thing,
Actuator, Switch and Connection).

TestCases from this module can be used as super classes for your
own platform-specific test cases. But shouldn't be executed by
their own.
"""


from unittest import TestSuite


def load_tests(loader, tests, pattern) -> TestSuite:
    """
    Custom load_tests function for this module. It just returns
    an empty test suite and so allows to hide all tests in this
    module from automatic discovery

    More info about such functions:
    https://docs.python.org/3/library/unittest.html#load-tests-protocol
    """
    return TestSuite()
