import unittest
from tests.integration import get_integration_tests
from tests.unit import get_unit_tests


def get_all_tests():
    return unittest.TestSuite([
        get_unit_tests(),
        get_integration_tests()
    ])
