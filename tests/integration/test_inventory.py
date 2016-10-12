import json
from tests.integration.util import IntegrationTestCase


class InventoryIntegrationTestCase(IntegrationTestCase):
    def test_inventory_empty(self):
        client = self.get_client()
        self.register_and_login(client, "test_inventory_empty")
        client.send("inventory\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("inventory", response["data"]["command"])
        self.assertIsNone(response["data"]["result"]["fitted"])
        self.assertEqual({}, response["data"]["result"]["inventory"])

    def test_inventory_one_item(self):
        client = self.get_client()
        self.register_and_login(client, "test_inventory_one_item")
        client.send("test.add_active_warp_scanner\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("test.add_active_warp_scanner", response1["data"]["command"])
        client.send("inventory\r\n")
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("inventory", response2["data"]["command"])
        self.assertIsNone(response2["data"]["result"]["fitted"])
        self.assertEqual(1, len(response2["data"]["result"]["inventory"]))

    def test_inventory_with_parameters_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_inventory_with_parameters")
        client.send("inventory one\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("inventory", response["data"]["command"])
        # TODO Verify error message
