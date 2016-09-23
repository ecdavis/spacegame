import json
from tests.integration.util import IntegrationTestCase


class WarpIntegrationTestCase(IntegrationTestCase):
    def test_warp(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp")
        client.send("warp.scan.activate\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("warp.scan.activate", response1["data"]["command"])
        self.assertEqual(set(["Sol", "Earth"]), set(response1["data"]["result"]["celestial_names"]))
        client.send("warp Earth\r\n")
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("warp", response2["data"]["command"])

    def test_warp_to_unscanned_celestial_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp2")
        client.send("warp Earth\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("warp", response["data"]["command"])

    def test_warp_to_non_existent_celestial_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_to_non_existent_celestial")
        client.send("warp this is not a real star system\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("warp", response["data"]["command"])
        # TODO Verify error message

    def test_warp_to_celestial_in_other_star_system_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_to_celestial_in_other_star_system")
        client.send("warp Alpha Centauri\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("warp", response["data"]["command"])
        # TODO Verify error message

    def test_warp_to_current_celestial_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_to_current_celestial")
        client.send("warp Sol\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("warp", response["data"]["command"])
        # TODO Verify error message

    def test_warp_with_no_parameters_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_with_no_parameters")
        client.send("warp\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("warp", response["data"]["command"])
        # TODO Verify error message

    def test_warp_scan_before_active_scan(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_scan_before_active_scan")
        client.send("warp.scan\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("warp.scan", response["data"]["command"])
        self.assertEqual([], response["data"]["result"]["celestial_names"])

    def test_warp_scan_after_active_scan(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_scan_after_active_scan")
        client.send("warp.scan.activate\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("warp.scan.activate", response1["data"]["command"])
        self.assertEqual(set(["Sol", "Earth"]), set(response1["data"]["result"]["celestial_names"]))
        client.send("warp.scan\r\n")
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("warp.scan", response2["data"]["command"])
        self.assertEqual(set(["Sol", "Earth"]), set(response2["data"]["result"]["celestial_names"]))
