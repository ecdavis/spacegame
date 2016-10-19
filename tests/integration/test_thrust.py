import json
import time
from tests.integration.util import IntegrationTestCase


class ThrustIntegrationTestCase(IntegrationTestCase):
    def test_thrust_speed(self):
        client = self.get_client()
        self.register_and_login(client, "test_thrust_speed")
        client.send("position\r\n")
        start_response = json.loads(client.recv(4096))
        start_position = start_response["data"]["result"]["position"]

        client.send("thrust.speed 5\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("thrust.speed", response["data"]["command"])

        time.sleep(0.5)
        client.send("position\r\n")
        end_response = json.loads(client.recv(4096))
        end_position = end_response["data"]["result"]["position"]
        self.assertNotEqual(start_position, end_position)

    def test_thrust_speed_with_negative_speed_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_thrust_speed_with_negative_speed")
        client.send("thrust.speed -1\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.speed", response["data"]["command"])
        # TODO Verify error message

    def test_thrust_speed_with_speed_over_10_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_thrust_speed_with_speed_over_10")
        client.send("thrust.speed 11\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.speed", response["data"]["command"])
        # TODO Verify error message

    def test_thrust_speed_with_float_parameter_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_thrust_speed_with_float_parameter")
        client.send("thrust.speed 5.5\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("thrust.speed", response["data"]["command"])
        # TODO Verify error message

    def test_thrust_speed_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_thrust_speed_validate_parameters")
        self.validate_parameters(client, "thrust.speed", num_parameters=1)

    def test_thrust_vector(self):
        client = self.get_client()
        self.register_and_login(client, "test_thrust_vector")
        client.send("thrust.vector 0.0 1.0 0.0\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify success.

    def test_thrust_vector_with_vector_sum_greater_than_one_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_thrust_vector_with_vector_sum_greater_than_one")
        client.send("thrust.vector 0.5 0.5 0.5\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

    def test_thrust_vector_with_vector_entries_greater_than_one_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_thrust_vector_with_vector_entries_greater_than_one")
        client.send("thrust.vector 1.1 0 0\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

        client.send("thrust.vector 0 1.1 0\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

        client.send("thrust.vector 0 0 1.1\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

        client.send("thrust.vector 1.1 0 1.1\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

        client.send("thrust.vector 1.1 1.1 1.1\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

    def test_thrust_vector_with_vector_entries_less_than_negative_one_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_thrust_vector_with_vector_entries_less_than_negative__one")
        client.send("thrust.vector -1.1 0 0\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

        client.send("thrust.vector 0 -1.1 0\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

        client.send("thrust.vector 0 0 -1.1\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

        client.send("thrust.vector -1.1 0 -1.1\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

        client.send("thrust.vector -1.1 -1.1 -1.1\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.vector", response["data"]["command"])
        # TODO Verify error message

    def test_thrust_vector_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_thrust_vector_validate_parameters")
        self.validate_parameters(client, "thrust.vector", num_parameters=3)
