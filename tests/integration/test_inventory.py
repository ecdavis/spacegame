import json
from tests.integration.util import IntegrationTestCase


class InventoryIntegrationTestCase(IntegrationTestCase):
    def test_inventory(self):
        client = self.get_client()
        self.register_and_login(client, "test_inventory")
        client.send("inventory\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("inventory", response["data"]["command"])
        self.assertEqual({}, response["data"]["result"]["inventory"])

    def test_inventory_with_parameters_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_inventory_with_parameters")
        client.send("inventory one\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("inventory", response["data"]["command"])
        # TODO Verify error message
