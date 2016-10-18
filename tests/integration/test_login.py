import json
import socket
import uuid
from tests.integration.util import IntegrationTestCase


class LoginIntegrationTestCase(IntegrationTestCase):
    def test_register(self):
        client = self.get_client()
        username = "test_register"
        client.send("register %s\r\n" % username)
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("register", response["data"]["command"])
        self.assertEqual(username, response["data"]["result"]["name"])

    def test_register_with_existing_user_returns_failure(self):
        client = self.get_client()
        username = "test_register_existing_user"
        client.send("register %s\r\n" % username)
        first_response = json.loads(client.recv(4096))
        self.assertEqual("command.success", first_response["message"])

        client.send("register %s\r\n" % username)
        second_response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", second_response["message"])
        self.assertEqual("register", second_response["data"]["command"])

    def test_register_with_no_parameters_returns_error(self):
        client = self.get_client()
        client.send("register\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("register", response["data"]["command"])
        # TODO Verify error message?

    def test_register_with_multiple_parameters_returns_error(self):
        client = self.get_client()
        client.send("register one two\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("register", response["data"]["command"])
        # TODO Verify error message?

    def test_login(self):
        client = self.get_client()
        client.send("login 1500b58c-55df-40ec-aecd-a60436aaa1ac\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("login", response["data"]["command"])
        self.assertEqual("test_login", response["data"]["result"]["name"])

    def test_register_and_login(self):
        client = self.get_client()
        username = "test_register_and_login"
        client.send("register %s\r\n" % username)
        register_response = json.loads(client.recv(4096))
        uuid = register_response["data"]["result"]["uuid"]

        client.send("login %s\r\n" % uuid)
        login_response = json.loads(client.recv(4096))
        self.assertEqual("command.success", login_response["message"])
        self.assertEqual("login", login_response["data"]["command"])
        self.assertEqual(username, login_response["data"]["result"]["name"])

    def test_login_with_non_existent_uuid_returns_failure(self):
        client = self.get_client()
        client.send("login %s\r\n" % str(uuid.uuid4()))
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("login", response["data"]["command"])
        # TODO Verify error message

    def test_login_with_no_parameters_returns_error(self):
        client = self.get_client()
        client.send("login\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("login", response["data"]["command"])
        # TODO Verify error message?

    def test_login_with_multiple_parameters_returns_error(self):
        client = self.get_client()
        client.send("login one two\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("login", response["data"]["command"])
        # TODO Verify error message

    def test_login_with_invalid_parameter_returns_error(self):
        client = self.get_client()
        client.send("login notauuid\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("login", response["data"]["command"])
        # TODO Verify error message

    def test_quit(self):
        client = self.get_client()
        client.send("quit\r\n")
        response = client.recv(4096)
        self.assertEqual('', response)

    def test_quit_with_parameters_returns_error(self):
        client = self.get_client()
        client.send("quit one\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("quit", response["data"]["command"])
        # TODO Verify error message
