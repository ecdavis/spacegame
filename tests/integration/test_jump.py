import json
from tests.integration.util import IntegrationTestCase


class JumpIntegrationTestCase(IntegrationTestCase):
    def test_jump(self):
        client = self.get_client()
        self.register_and_login(client, "test_jump")
        client.send("jump Alpha Centauri\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("jump", response["data"]["command"])

    def test_jump_to_non_existent_star_system_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_jump_to_non_existent_star_system")
        client.send("jump this is not a real star system\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("jump", response["data"]["command"])
        # TODO Verify error message

    def test_jump_to_current_star_system_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_jump_to_current_star_system")
        client.send("jump The Solar System\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("jump", response["data"]["command"])
        # TODO Verify error message

    def test_jump_with_no_parameters_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_jump_with_no_parameters")
        client.send("jump\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("jump", response["data"]["command"])
        # TODO Verify error message
