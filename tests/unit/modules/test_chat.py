import mock
from pantsmud.util import error
from spacegame.core import messages
from spacegame.modules import chat
from spacegame.universe import universe
from tests.unit.util import UnitTestCase


class ChatServiceUnitTestCase(UnitTestCase):
    def setUp(self):
        self.universe = universe.Universe()
        self.messages = messages.Messages()
        self.service = chat.Service(self.universe, self.messages)

        self.mobile1 = mock.MagicMock()
        self.mobile1.name = "mobile1"
        self.universe.add_entity(self.mobile1)

        self.mobile2 = mock.MagicMock()
        self.mobile2.name = "mobile2"
        self.universe.add_entity(self.mobile2)

        self.mobile3 = mock.MagicMock()
        self.mobile3.name = "mobile3"
        self.universe.add_entity(self.mobile3)

    def test_chat_global(self):
        expected_result = ("mobile1", "foo")
        expected_notification = {
            "notification": "chat.global",
            "data": {
                "mobile_from": "mobile1",
                "message": "foo"
            }
        }

        actual_result = self.service.chat_global(self.mobile1, "foo")

        self.assertEqual(expected_result, actual_result)
        self.mobile1.message.assert_not_called()
        self.mobile2.message.assert_called_once_with("notify", expected_notification)
        self.mobile3.message.assert_called_once_with("notify", expected_notification)

    def test_chat_private(self):
        expected_result = ("mobile1", "mobile2", "foo")
        expected_notification = {
            "notification": "chat.private",
            "data": {
                "mobile_from": "mobile1",
                "mobile_to": "mobile2",
                "message": "foo"
            }
        }

        actual_result = self.service.chat_private(self.mobile1, "mobile2", "foo")

        self.assertEqual(expected_result, actual_result)
        self.mobile1.message.assert_not_called()
        self.mobile2.message.assert_called_once_with("notify", expected_notification)
        self.mobile3.message.assert_not_called()

    def test_chat_private_raises_command_fail_when_target_does_not_exist(self):
        self.assertRaises(
            error.CommandFail,
            self.service.chat_private,
            self.mobile1,
            "mobile0",
            "foo"
        )

    def test_chat_private_raises_command_fail_when_target_is_mobile(self):
        self.assertRaises(
            error.CommandFail,
            self.service.chat_private,
            self.mobile1,
            "mobile1",
            "foo"
        )


class ChatEndpointUnitTestCase(UnitTestCase):
    def setUp(self):
        self.universe = universe.Universe()
        self.messages = messages.Messages()
        self.service = chat.Service(self.universe, self.messages)

        self.chat_global_endpoint = chat.make_chat_global_endpoint(self.service)
        self.chat_private_endpoint = chat.make_chat_private_endpoint(self.service)

        self.mobile1 = mock.MagicMock()
        self.mobile1.name = "mobile1"
        self.universe.add_entity(self.mobile1)

        self.mobile2 = mock.MagicMock()
        self.mobile2.name = "mobile2"
        self.universe.add_entity(self.mobile2)

        self.mobile3 = mock.MagicMock()
        self.mobile3.name = "mobile3"
        self.universe.add_entity(self.mobile3)

    def test_chat_global(self):
        request = {
            "mobile": self.mobile1,
            "message": "foo"
        }
        expected = {
            "mobile_from": "mobile1",
            "message": "foo"
        }
        actual = self.chat_global_endpoint(request)
        self.assertEqual(expected, actual)

    def test_chat_private(self):
        request = {
            "mobile": self.mobile1,
            "target_name": "mobile2",
            "message": "foo"
        }
        expected = {
            "mobile_from": "mobile1",
            "mobile_to": "mobile2",
            "message": "foo"
        }
        actual = self.chat_private_endpoint(request)
        self.assertEqual(expected, actual)


class ChatCommandUnitTestCase(UnitTestCase):
    def setUp(self):
        self.universe = universe.Universe()
        self.messages = messages.Messages()
        self.service = chat.Service(self.universe, self.messages)

        self.chat_global_endpoint = chat.make_chat_global_endpoint(self.service)
        self.chat_private_endpoint = chat.make_chat_private_endpoint(self.service)

        self.chat_global_command = chat.make_chat_global_command(self.chat_global_endpoint)
        self.chat_private_command = chat.make_chat_private_command(self.chat_private_endpoint)

        self.brain1 = mock.MagicMock()
        self.mobile1 = mock.MagicMock()
        self.brain1.mobile = self.mobile1
        self.mobile1.brain = self.brain1
        self.mobile1.name = "mobile1"
        self.universe.add_entity(self.mobile1)

        self.mobile2 = mock.MagicMock()
        self.mobile2.name = "mobile2"
        self.universe.add_entity(self.mobile2)

        self.mobile3 = mock.MagicMock()
        self.mobile3.name = "mobile3"
        self.universe.add_entity(self.mobile3)

    def test_chat_global(self):
        self.chat_global_command(self.brain1, "chat.global", "foo bar baz")
        self.brain1.message.assert_called_once_with(
            "command.success",
            {
                "command": "chat.global",
                "result": {
                    "mobile_from": "mobile1",
                    "message": "foo bar baz"
                }
            }
        )

    def test_chat_private(self):
        self.chat_private_command(self.brain1, "chat.private", "mobile2 foo bar baz")
        self.brain1.message.assert_called_once_with(
            "command.success",
            {
                "command": "chat.private",
                "result": {
                    "mobile_from": "mobile1",
                    "mobile_to": "mobile2",
                    "message": "foo bar baz"
                }
            }
        )
