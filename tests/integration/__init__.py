import unittest
from tests.integration.test_info import InfoIntegrationTestCase
from tests.integration.test_jump import JumpIntegrationTestCase
from tests.integration.test_login import LoginIntegrationTestCase
from tests.integration.test_warp import WarpIntegrationTestCase


def get_integration_tests():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(InfoIntegrationTestCase),
        unittest.TestLoader().loadTestsFromTestCase(JumpIntegrationTestCase),
        unittest.TestLoader().loadTestsFromTestCase(LoginIntegrationTestCase),
        unittest.TestLoader().loadTestsFromTestCase(WarpIntegrationTestCase)
    ])
