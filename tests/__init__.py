import unittest
from tests.unit.placeholder import PlaceholderTestCase


def get_unit_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(PlaceholderTestCase)
    ])
