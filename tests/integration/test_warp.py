import json
from tests.integration.util import IntegrationTestCase


class WarpIntegrationTestCase(IntegrationTestCase):
    def test_warp(self):
        self.register_and_login("test_warp")
        self.socket.send("warp Earth\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("warp", response["data"]["command"])

    def test_warp_to_non_existent_celestial_returns_failure(self):
        self.register_and_login("test_warp_to_non_existent_celestial")
        self.socket.send("warp this is not a real star system\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("warp", response["data"]["command"])
        # TODO Verify error message

    def test_warp_to_celestial_in_other_star_system_returns_failure(self):
        self.register_and_login("test_warp_to_celestial_in_other_star_system")
        self.socket.send("warp Alpha Centauri\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("warp", response["data"]["command"])
        # TODO Verify error message

    def test_warp_to_current_celestial_returns_failure(self):
        self.register_and_login("test_warp_to_current_celestial")
        self.socket.send("warp Sol\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("warp", response["data"]["command"])
        # TODO Verify error message

    def test_warp_with_no_parameters_returns_error(self):
        self.register_and_login("test_warp_with_no_parameters")
        self.socket.send("warp\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("warp", response["data"]["command"])
        # TODO Verify error message
