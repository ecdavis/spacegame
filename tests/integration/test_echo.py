import json
import socket
import time
from tests.integration.util import IntegrationTestCase


class EchoIntegrationTestCase(IntegrationTestCase):
    def test_echo(self):
        client = self.get_client()
        self.register_and_login(client, "test_echo")
        client.send("echo foo bar baz\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("echo", response["data"]["command"])
        self.assertEqual("foo bar baz", response["data"]["result"]["line"])

    def test_quit(self):
        client = self.get_client()
        self.register_and_login(client, "test_quit")
        client.send("quit\r\n")
        response = client.recv(4096)
        self.assertEqual('', response)

    def test_quit_with_parameters_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_quit_with_parameters")
        client.send("quit one\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("quit", response["data"]["command"])
        # TODO Verify error message

    def test_shutdown_with_parameters_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_shutdown_with_parameters")
        client.send("shutdown one\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("shutdown", response["data"]["command"])
        # TODO Verify error message


class ShutdownIntegrationTestCase(IntegrationTestCase):
    @classmethod
    def tearDownClass(cls):
        return

    def test_shutdown(self):
        client = self.get_client()
        self.register_and_login(client, "test_shutdown")
        client.send("shutdown\r\n")
        response = client.recv(4096)
        self.assertEqual('', response)

        time.sleep(2.0)

        self.assertRaises(socket.error, self.get_client)
