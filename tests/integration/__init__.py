import unittest
from tests.integration.test_info import InfoIntegrationTestCase
from tests.integration.test_jump import JumpIntegrationTestCase
from tests.integration.test_login import LoginIntegrationTestCase


def get_integration_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(InfoIntegrationTestCase),
        unittest.TestLoader().loadTestsFromTestCase(JumpIntegrationTestCase),
        unittest.TestLoader().loadTestsFromTestCase(LoginIntegrationTestCase)
    ])
