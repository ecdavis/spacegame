import unittest
from tests.unit.test_placeholder import PlaceholderTestCase


def get_unit_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(PlaceholderTestCase)
    ])
