import json
from tests.integration.util import IntegrationTestCase


class JumpIntegrationTestCase(IntegrationTestCase):
    def test_jump(self):
        self.register_and_login("test_jump")
        self.socket.send("jump Alpha Centauri\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("jump", response["data"]["command"])
