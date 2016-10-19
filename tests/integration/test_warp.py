import json
from tests.integration.util import IntegrationTestCase, StatefulIntegrationTestCase


class WarpIntegrationTestCase(IntegrationTestCase):
    def test_warp_scan_with_no_beacons_before_active_scan(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_scan_with_no_beacons_before_active_scan")
        client.send("warp.scan\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("warp.scan", response["data"]["command"])
        self.assertEqual({}, response["data"]["result"]["beacons"])
        self.assertEqual({}, response["data"]["result"]["celestials"])

    def test_warp_scan_with_no_beacons_after_active_scan(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_scan_with_no_beacons_after_active_scan")
        client.send("warp.scan.activate\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("warp.scan.activate", response1["data"]["command"])
        client.send("warp.scan\r\n")
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("warp.scan", response2["data"]["command"])
        self.assertEqual({}, response2["data"]["result"]["beacons"])
        self.assertEqual({"Earth": "f5102606-bacc-4055-8e64-600efb874985"}, response2["data"]["result"]["celestials"])

    def test_warp_scan_activate(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_scan_activate")
        client.send("warp.scan.activate\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("warp.scan.activate", response["data"]["command"])
        self.assertEqual({"Earth": "f5102606-bacc-4055-8e64-600efb874985"}, response["data"]["result"]["celestials"])

    def test_warp_to_celestial_before_active_scan_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_to_celestial_before_active_scan")
        client.send("warp f5102606-bacc-4055-8e64-600efb874985\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("warp", response["data"]["command"])
        # TODO Validate error message

    def test_warp_to_celestial_after_active_scan(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_to_celestial_after_active_scan")
        client.send("warp.scan.activate\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("warp.scan.activate", response1["data"]["command"])
        client.send("warp f5102606-bacc-4055-8e64-600efb874985\r\n")
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("warp", response2["data"]["command"])

    def test_warp_to_non_existent_celestial_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_to_non_existent_celestial")
        client.send("warp.scan.activate\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("warp.scan.activate", response1["data"]["command"])
        client.send("warp 00000000-0000-0000-0000-000000000000\r\n")
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response2["message"])
        self.assertEqual("warp", response2["data"]["command"])
        # TODO Verify error message

    def test_warp_to_celestial_in_other_star_system_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_to_celestial_in_other_star_system")
        client.send("warp.scan.activate\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("warp.scan.activate", response1["data"]["command"])
        client.send("warp 35b81fc4-0313-4fac-9054-7f8cc05cf092\r\n")
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response2["message"])
        self.assertEqual("warp", response2["data"]["command"])
        # TODO Verify error message

    def test_warp_to_current_celestial_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_to_current_celestial")
        client.send("warp.scan.activate\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("warp.scan.activate", response1["data"]["command"])
        client.send("warp a74b22ea-6aa1-4410-b819-32a1b6c6613f\r\n")
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response2["message"])
        self.assertEqual("warp", response2["data"]["command"])
        # TODO Verify error message

    def test_warp_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_validate_parameters")
        self.validate_num_parameters(client, "warp", num_parameters=1)

    def test_warp_beacon_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_beacon_validate_parameters")
        self.validate_num_parameters(client, "warp.beacon", num_parameters=0)

    def test_warp_scan_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_scan_validate_parameters")
        self.validate_num_parameters(client, "warp.scan", num_parameters=0)

    def test_warp_scan_activate_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_scan_activate_validate_parameters")
        self.validate_num_parameters(client, "warp.scan.activate", num_parameters=0)


class WarpStatefulIntegrationTestCase(StatefulIntegrationTestCase):
    def test_warp_beacon(self):
        client = self.get_client()
        self.register_and_login(client, "test_warp_beacon")
        client.send("warp.beacon\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("warp.beacon", response["data"]["command"])

    def test_warp_scan_with_beacons_before_active_scan(self):
        beacon_uuid = self._place_beacon_at_earth("test_warp_scan_with_beacons_before_active_scan_setup")

        client = self.get_client()
        self.register_and_login(client, "test_warp_scan_with_beacons_before_active_scan")
        client.send("warp.scan\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("warp.scan", response["data"]["command"])
        self.assertEqual({"": beacon_uuid}, response["data"]["result"]["beacons"])
        self.assertEqual({}, response["data"]["result"]["celestials"])

    def test_warp_scan_with_beacons_after_active_scan(self):
        beacon_uuid = self._place_beacon_at_earth("test_warp_scan_with_beacons_after_active_scan_setup")

        client = self.get_client()
        self.register_and_login(client, "test_warp_scan_with_beacons_after_active_scan")
        client.send("warp.scan.activate\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("warp.scan.activate", response1["data"]["command"])
        client.send("warp.scan\r\n")
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("warp.scan", response2["data"]["command"])
        self.assertEqual({"": beacon_uuid}, response2["data"]["result"]["beacons"])
        self.assertEqual({"Earth": "f5102606-bacc-4055-8e64-600efb874985"}, response2["data"]["result"]["celestials"])

    def test_warp_to_beacon_before_active_scan(self):
        beacon_uuid = self._place_beacon_at_earth("test_warp_to_beacon_before_active_scan_setup")

        client = self.get_client()
        self.register_and_login(client, "test_warp_to_beacon_before_active_scan")
        client.send("warp %s\r\n" % beacon_uuid)
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("warp", response["data"]["command"])

    def test_warp_to_beacon_after_active_scan(self):
        beacon_uuid = self._place_beacon_at_earth("test_warp_to_beacon_after_active_scan_setup")

        client = self.get_client()
        self.register_and_login(client, "test_warp_to_beacon_after_active_scan")
        client.send("warp.scan.activate\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("warp.scan.activate", response1["data"]["command"])
        client.send("warp %s\r\n" % beacon_uuid)
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("warp", response2["data"]["command"])

    def _place_beacon_at_earth(self, username):
        client = self.get_client()
        self.register_and_login(client, username)
        client.send("warp.scan.activate\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("warp.scan.activate", response1["data"]["command"])
        client.send("warp f5102606-bacc-4055-8e64-600efb874985\r\n")
        response2 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response2["message"])
        self.assertEqual("warp", response2["data"]["command"])
        client.send("warp.beacon\r\n")
        response3 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response3["message"])
        self.assertEqual("warp.beacon", response3["data"]["command"])
        return response3["data"]["result"]["beacon_uuid"]
