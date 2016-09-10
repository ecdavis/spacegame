import json
import time
from tests.integration.util import IntegrationTestCase


class ThrustIntegrationTestCase(IntegrationTestCase):
    def test_thrust_speed(self):
        self.register_and_login("test_thrust_speed")
        self.socket.send("position\r\n")
        start_response = json.loads(self.socket.recv(4096))
        start_position = start_response["data"]["result"]["position"]

        self.socket.send("thrust.speed 5\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("thrust.speed", response["data"]["command"])

        time.sleep(0.5)
        self.socket.send("position\r\n")
        end_response = json.loads(self.socket.recv(4096))
        end_position = end_response["data"]["result"]["position"]
        self.assertNotEqual(start_position, end_position)

    def test_thrust_speed_with_negative_speed_returns_failure(self):
        self.register_and_login("test_thrust_speed_with_negative_speed")
        self.socket.send("thrust.speed -1\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.speed", response["data"]["command"])
        # TODO Verify error message

    def test_thrust_speed_with_speed_over_10_returns_failure(self):
        self.register_and_login("test_thrust_speed_with_speed_over_10")
        self.socket.send("thrust.speed 11\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("thrust.speed", response["data"]["command"])
        # TODO Verify error message

    def test_thrust_speed_with_float_parameter_returns_error(self):
        self.register_and_login("test_thrust_speed_with_float_parameter")
        self.socket.send("thrust.speed 5.5\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("thrust.speed", response["data"]["command"])
        # TODO Verify error message

    def test_thrust_speed_with_no_parameter_returns_error(self):
        self.register_and_login("test_thrust_speed_with_no_parameter")
        self.socket.send("thrust.speed\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("thrust.speed", response["data"]["command"])
        # TODO Verify error message

    def test_thrust_speed_with_multiple_parameters_returns_error(self):
        self.register_and_login("test_thrust_speed_with_multiple_parameters")
        self.socket.send("thrust.speed 5 5\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("thrust.speed", response["data"]["command"])
        # TODO Verify error message
