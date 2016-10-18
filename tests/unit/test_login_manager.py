import mock
from spacegame.core.login_manager import add_command, command_exists, login_input_handler
from tests.unit.util import UnitTestCase


class LoginManagerUnitTestCase(UnitTestCase):
    def test_login_input_handler_when_is_client_is_False(self):
        brain = mock.MagicMock()
        brain.is_client = False
        brain.message = mock.MagicMock()
        login_input_handler(brain, "test_login_input_handler_when_is_client")
        brain.message.assert_called()

    def test_login_input_handler_when_mobile_is_not_None(self):
        brain = mock.MagicMock()
        brain.is_client = True
        brain.mobile = mock.MagicMock()
        brain.message = mock.MagicMock()
        login_input_handler(brain, "test_login_input_handler_when_mobile")
        brain.message.assert_called()

    def test_command_exists_when_command_exists_returns_True(self):
        cmd_name = "test_command_exists_when_command_exists"
        command = mock.MagicMock(__name__=cmd_name)
        command.__name__ = cmd_name
        add_command(cmd_name, command)
        self.assertTrue(command_exists(cmd_name))

    def test_command_exists_when_command_doesnt_exist_returns_False(self):
        cmd_name = "test_command_exists_when_command_doesnt_exist"
        self.assertFalse(command_exists(cmd_name))
