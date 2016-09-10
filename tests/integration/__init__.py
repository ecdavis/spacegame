import unittest
from tests.integration.test_login import LoginIntegrationTestCase


def get_integration_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(LoginIntegrationTestCase)
    ])
