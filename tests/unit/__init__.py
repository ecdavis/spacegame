import unittest
from tests.unit.test_universe import UniverseUnitTestCase


def get_unit_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(UniverseUnitTestCase)
    ])
