import unittest
from tests.unit.modules.test_chat import ChatServiceUnitTestCase, ChatEndpointUnitTestCase, ChatCommandUnitTestCase


def get_modules_unit_tests():
    return unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(tc) for tc in (
        ChatServiceUnitTestCase,
        ChatEndpointUnitTestCase,
        ChatCommandUnitTestCase,
    )])
