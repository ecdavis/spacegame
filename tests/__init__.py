import unittest
from tests.integration.test_placeholder import PlaceholderIntegrationTestCase
from tests.unit.placeholder import PlaceholderTestCase


def get_all_tests():
    return unittest.TestSuite([
        get_unit_tests(),
        get_integration_tests()
    ])


def get_unit_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(PlaceholderTestCase)
    ])


def get_integration_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(PlaceholderIntegrationTestCase)
    ])
