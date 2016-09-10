import json
from tests.integration.util import IntegrationTestCase


class InfoIntegrationTestCase(IntegrationTestCase):
    def test_position(self):
        self.register_and_login("test_position")
        self.socket.send("position\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("position", response["data"]["command"])
        print response

    def test_location(self):
        self.register_and_login("test_location")
        self.socket.send("location\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("location", response["data"]["command"])
        print response
