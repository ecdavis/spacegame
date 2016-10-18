import unittest
from tests.unit.test_application import ApplicationUnitTestCase
from tests.unit.test_celestial import CelestialUnitTestCase
from tests.unit.test_entity import EntityUnitTestCase
from tests.unit.test_config import PathConfigUnitTestCase
from tests.unit.test_star_system import StarSystemUnitTestCase
from tests.unit.test_universe import UniverseUnitTestCase
from tests.unit.test_user import UserUnitTestCase


def get_unit_tests():
    return unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(tc) for tc in (
        ApplicationUnitTestCase,
        CelestialUnitTestCase,
        EntityUnitTestCase,
        PathConfigUnitTestCase,
        StarSystemUnitTestCase,
        UniverseUnitTestCase,
        UserUnitTestCase
    )])
