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
        client.send("login 1500b58c-55df-40ec-aecd-a60436aaa1ac\r\n")
        response1 = json.loads(client.recv(4096))
        self.assertEqual("command.success", response1["message"])
        self.assertEqual("login", response1["data"]["command"])
        self.assertEqual("test_user", response1["data"]["result"]["name"])

        client.send("quit\r\n")
        response2 = client.recv(4096)
        self.assertEqual('', response2)

    def test_register_and_quit(self):
        client = self.get_client()
        self.register_and_login(client, "test_register_and_quit")
        client.send("quit\r\n")
        response = client.recv(4096)
        self.assertEqual('', response)

    def test_quit_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_quit_validate_parameters")
        self.validate_num_parameters(client, "quit", num_parameters=0)

    def test_shutdown_validate_parameters(self):
        client = self.get_client()
        self.register_and_login(client, "test_shutdown_validate_parameters")
        self.validate_num_parameters(client, "shutdown", num_parameters=0)


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
