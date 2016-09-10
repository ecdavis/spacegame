import json
from tests.integration.util import IntegrationTestCase


class JumpIntegrationTestCase(IntegrationTestCase):
    def test_jump(self):
        self.register_and_login("test_jump")
        self.socket.send("jump Alpha Centauri\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("jump", response["data"]["command"])

    def test_jump_to_non_existent_star_system_returns_failure(self):
        self.register_and_login("test_jump_to_non_existent_star_system")
        self.socket.send("jump this is not a real star system\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("jump", response["data"]["command"])
        # TODO Verify error message

    def test_jump_to_current_star_system_returns_failure(self):
        self.register_and_login("test_jump_to_current_star_system")
        self.socket.send("jump The Solar System\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("jump", response["data"]["command"])
        # TODO Verify error message

    def test_jump_with_no_parameters_returns_error(self):
        self.register_and_login("test_jump_with_no_parameters")
        self.socket.send("jump\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("jump", response["data"]["command"])
        # TODO Verify error message
