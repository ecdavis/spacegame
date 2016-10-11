import unittest
from tests.unit.test_application import ApplicationUnitTestCase
from tests.unit.test_celestial import CelestialUnitTestCase
from tests.unit.test_entity import EntityUnitTestCase
from tests.unit.test_config import PathConfigUnitTestCase
from tests.unit.test_mobile import MobileUnitTestCase
from tests.unit.test_universe import UniverseUnitTestCase


def get_unit_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(ApplicationUnitTestCase),
        unittest.TestLoader().loadTestsFromTestCase(CelestialUnitTestCase),
        unittest.TestLoader().loadTestsFromTestCase(EntityUnitTestCase),
        unittest.TestLoader().loadTestsFromTestCase(MobileUnitTestCase),
        unittest.TestLoader().loadTestsFromTestCase(PathConfigUnitTestCase),
        unittest.TestLoader().loadTestsFromTestCase(UniverseUnitTestCase)
    ])
