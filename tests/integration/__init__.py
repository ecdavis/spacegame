import unittest
from tests.integration.test_placeholder import PlaceholderIntegrationTestCase


def get_integration_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(PlaceholderIntegrationTestCase)
    ])
