import unittest
from tests.integration.test_chat import ChatIntegrationTestCase
from tests.integration.test_echo import EchoIntegrationTestCase, ShutdownIntegrationTestCase
from tests.integration.test_info import InfoIntegrationTestCase
from tests.integration.test_inventory import InventoryIntegrationTestCase
from tests.integration.test_jump import JumpIntegrationTestCase
from tests.integration.test_login import LoginIntegrationTestCase
from tests.integration.test_thrust import ThrustIntegrationTestCase
from tests.integration.test_warp import WarpIntegrationTestCase, WarpStatefulIntegrationTestCase


def get_integration_tests():
    test_loader = unittest.TestLoader()
    return unittest.TestSuite([test_loader.loadTestsFromTestCase(tc) for tc in (
        ChatIntegrationTestCase,
        EchoIntegrationTestCase,
        InfoIntegrationTestCase,
        InventoryIntegrationTestCase,
        JumpIntegrationTestCase,
        LoginIntegrationTestCase,
        ThrustIntegrationTestCase,
        WarpIntegrationTestCase,
        WarpStatefulIntegrationTestCase,
        ShutdownIntegrationTestCase
    )])
