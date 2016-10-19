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

    def test_inventory_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_inventory_validate_parameters")
        self.validate_parameters(client, "inventory", num_parameters=0)

    def test_fit(self):
        client = self.get_client()
        self.register_and_login(client, "test_fit")
        client.send("test.add_active_warp_scanner\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("test.add_active_warp_scanner", response1["data"]["command"])
        fittable_item_uuid = response1["data"]["result"]["item"]
        client.send("fit %s\r\n" % fittable_item_uuid)
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("fit", response2["data"]["command"])
        client.send("inventory\r\n")
        response3 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response3["message"])
        self.assertEqual("inventory", response3["data"]["command"])
        self.assertEqual(fittable_item_uuid, response3["data"]["result"]["fitted"].values()[0])

    def test_fit_with_already_fitted_item_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_fit_with_already_fitted_item")
        client.send("test.add_active_warp_scanner\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("test.add_active_warp_scanner", response1["data"]["command"])
        fittable_item1_uuid = response1["data"]["result"]["item"]
        client.send("fit %s\r\n" % fittable_item1_uuid)
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("fit", response2["data"]["command"])

        client.send("test.add_active_warp_scanner\r\n")
        response3 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response3["message"])
        self.assertEqual("test.add_active_warp_scanner", response3["data"]["command"])
        fittable_item2_uuid = response1["data"]["result"]["item"]
        client.send("fit %s\r\n" % fittable_item2_uuid)
        response4 = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response4["message"])
        self.assertEqual("fit", response4["data"]["command"])
        # TODO Verify error message

    def test_fit_with_non_existent_item_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_fit_with_non_existent_item")
        client.send("fit 00000000-0000-0000-0000-000000000000\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("fit", response["data"]["command"])
        # TODO Verify error message

    def test_fit_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_fit_validate_parameters")
        self.validate_parameters(client, "fit", num_parameters=1)

    def test_unfit(self):
        client = self.get_client()
        self.register_and_login(client, "test_unfit")
        client.send("test.add_active_warp_scanner\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("test.add_active_warp_scanner", response1["data"]["command"])
        fittable_item_uuid = response1["data"]["result"]["item"]
        client.send("fit %s\r\n" % fittable_item_uuid)
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("fit", response2["data"]["command"])

        client.send("unfit\r\n")
        response3 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response3["message"])
        self.assertEqual("unfit", response3["data"]["command"])

    def test_unfit_with_no_fitted_item_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_unfit_with_no_fitted_item")
        client.send("unfit\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("unfit", response["data"]["command"])
        # TODO Verify error message

    def test_unfit_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_unfit_validate_parameters")
        self.validate_parameters(client, "unfit", num_parameters=0)
