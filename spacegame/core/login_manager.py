import logging
from pantsmud.driver import command, message


class LoginCommandManager(command.CommandManager):
    def input_handler(self, brain, line):
        if not brain.is_user:
            logging.error("Brain '%s' has login input handler but it is not a user.", str(brain.uuid))
            message.command_internal_error(brain)
            return
        if brain.mobile:
            logging.error("Brain '%s' has login input handler it already has a player '%s'.",
                          str(brain.uuid), str(brain.mobile.uuid))
            message.command_internal_error(brain)
            return
        return command.CommandManager.input_handler(self, brain, line)


_login_command_manager = LoginCommandManager(__name__)
add_command = _login_command_manager.add
command_exists = _login_command_manager.exists
login_input_handler = _login_command_manager.input_handler
