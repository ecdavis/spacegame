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

    def test_position_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_position_validate_parameters")
        self.validate_parameters(client, "position", num_parameters=0)

    def test_location(self):
        client = self.get_client()
        self.register_and_login(client, "test_location")
        client.send("location\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("location", response["data"]["command"])
        self.assertEqual("Sol", response["data"]["result"]["celestial"])
        self.assertEqual("The Solar System", response["data"]["result"]["star_system"])

    def test_location_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_location_validate_parameters")
        self.validate_parameters(client, "location", num_parameters=0)
