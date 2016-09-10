import json
from tests.integration.util import IntegrationTestCase


class ChatIntegrationTestCase(IntegrationTestCase):
    def test_chat_global(self):
        client1 = self.get_client()
        self.register_and_login(client1, "test_chat_global_1")
        client2 = self.get_client()
        self.register_and_login(client2, "test_chat_global_2")

        client1.send("chat.global hello, world!\r\n")
        response1 = json.loads(client1.recv(4096))
        response2 = json.loads(client2.recv(4096))

        self.assertEqual("command.success", response1["message"])
        self.assertEqual("chat.global", response1["data"]["command"])
        self.assertEqual("hello, world!", response1["data"]["result"]["message"])

        self.assertEqual("notify", response2["message"])
        self.assertEqual("chat.global", response2["data"]["notification"])
        self.assertEqual("hello, world!", response2["data"]["data"]["message"])
        self.assertEqual("test_chat_global_1", response2["data"]["data"]["mobile_from"])

    def test_chat_global_with_no_message_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_chat_global_with_no_message")
        client.send("chat.global\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("chat.global", response["data"]["command"])
        # TODO Verify error message

    def test_chat_private(self):
        client1 = self.get_client()
        self.register_and_login(client1, "test_chat_private_1")
        client2 = self.get_client()
        self.register_and_login(client2, "test_chat_private_2")

        client1.send("chat.private test_chat_private_2 hello, test client!\r\n")
        response1 = json.loads(client1.recv(4096))
        response2 = json.loads(client2.recv(4096))

        self.assertEqual("command.success", response1["message"])
        self.assertEqual("chat.private", response1["data"]["command"])
        self.assertEqual("test_chat_private_1", response1["data"]["result"]["mobile_from"])
        self.assertEqual("test_chat_private_2", response1["data"]["result"]["mobile_to"])
        self.assertEqual("hello, test client!", response1["data"]["result"]["message"])

        self.assertEqual("notify", response2["message"])
        self.assertEqual("chat.private", response2["data"]["notification"])
        self.assertEqual("test_chat_private_1", response2["data"]["data"]["mobile_from"])
        self.assertEqual("test_chat_private_2", response2["data"]["data"]["mobile_to"])
        self.assertEqual("hello, test client!", response2["data"]["data"]["message"])

    def test_chat_private_with_no_parameters_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_chat_private_with_no_parameters")
        client.send("chat.private\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("chat.private", response["data"]["command"])
        # TODO Verify error message

    def test_chat_private_with_no_message_returns_error(self):
        client = self.get_client()
        self.register_and_login(client, "test_chat_private_with_no_message")
        client.send("chat.private test\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.error", response["message"])
        self.assertEqual("chat.private", response["data"]["command"])
        # TODO Verify error message

    def test_chat_private_with_invalid_target_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_chat_private_with_invalid_target")
        client.send("chat.private test test\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("chat.private", response["data"]["command"])
        # TODO Verify error message

    def test_chat_private_with_self_target_returns_failure(self):
        client = self.get_client()
        self.register_and_login(client, "test_chat_private_with_self_target")
        client.send("chat.private test_chat_private_with_self_target test\r\n")
        response = json.loads(client.recv(4096))
        self.assertEqual("command.fail", response["message"])
        self.assertEqual("chat.private", response["data"]["command"])
        # TODO Verify error message
