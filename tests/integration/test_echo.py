import json
import socket
from tests.integration.util import IntegrationTestCase


class EchoIntegrationTestCase(IntegrationTestCase):
    def test_echo(self):
        self.register_and_login("test_echo")
        self.socket.send("echo foo bar baz\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", response["message"])
        self.assertEqual("echo", response["data"]["command"])
        self.assertEqual("foo bar baz", response["data"]["result"]["line"])

    def test_quit(self):
        self.register_and_login("test_quit")
        self.socket.send("quit\r\n")
        response = self.socket.recv(4096)
        self.assertEqual('', response)

    def test_quit_with_parameters_returns_error(self):
        self.register_and_login("test_quit_with_parameters")
        self.socket.send("quit one\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("quit", response["data"]["command"])
        # TODO Verify error message

    def test_shutdown_with_parameters_returns_error(self):
        self.register_and_login("test_shutdown_with_parameters")
        self.socket.send("shutdown one\r\n")
        response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("shutdown", response["data"]["command"])
        # TODO Verify error message


class ShutdownIntegrationTestCase(IntegrationTestCase):
    @classmethod
    def tearDownClass(cls):
        return

    def test_shutdown(self):
        self.register_and_login("test_shutdown")
        self.socket.send("shutdown\r\n")
        response = self.socket.recv(4096)
        self.assertEqual('', response)

        client = socket.socket()
        client.settimeout(5.0)
        self.assertRaises(socket.error, client.connect, ('127.0.0.1', self._port))
