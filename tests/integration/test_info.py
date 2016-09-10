import json
from tests.integration.util import IntegrationTestCase


class InfoIntegrationTestCase(IntegrationTestCase):
    def test_position(self):
        self.register_and_login("test_position")
        self.socket.send("position\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("position", response["data"]["command"])
        self.assertEqual([0, 0, 0], response["data"]["result"]["position"])

    def test_position_with_parameters_returns_error(self):
        self.register_and_login("test_position_with_parameters")
        self.socket.send("position one\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("position", response["data"]["command"])
        # TODO Verify error message

    def test_location(self):
        self.register_and_login("test_location")
        self.socket.send("location\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("location", response["data"]["command"])
        self.assertEqual("Sol", response["data"]["result"]["celestial"])
        self.assertEqual("The Solar System", response["data"]["result"]["star_system"])

    def test_location_with_parameters_returns_error(self):
        self.register_and_login("test_location_with_parameters")
        self.socket.send("location one\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("location", response["data"]["command"])
        # TODO Verify error message
