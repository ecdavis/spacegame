import json
from tests.integration.util import IntegrationTestCase


class InfoIntegrationTestCase(IntegrationTestCase):
    def test_position(self):
        client = self.get_client()
        self.register_and_login(client, "test_position")
        client.send("position\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("position", response["data"]["command"])
        self.assertEqual([0, 0, 0], response["data"]["result"]["position"])

    def test_position_with_parameters_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_position_with_parameters")
        client.send("position one\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("position", response["data"]["command"])
        # TODO Verify error message

    def test_location(self):
        client = self.get_client()
        self.register_and_login(client, "test_location")
        client.send("location\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("location", response["data"]["command"])
        self.assertEqual("Sol", response["data"]["result"]["celestial"])
        self.assertEqual("The Solar System", response["data"]["result"]["star_system"])

    def test_location_with_parameters_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_location_with_parameters")
        client.send("location one\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("location", response["data"]["command"])
        # TODO Verify error message
