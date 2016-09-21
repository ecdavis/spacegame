import logging
from pantsmud.driver import command
from pantsmud.util import message


_command_manager = None


class LoginCommandManager(command.CommandManager):
    def input_handler(self, brain, line):
        if not brain.is_client:
            logging.error("Brain '%s' has login input handler but it is not a client.", str(brain.uuid))
            message.command_internal_error(brain)
            return
        if brain.mobile:
            logging.error("Brain '%s' has login input handler it already has a player '%s'.",
                          str(brain.uuid), str(brain.mobile.uuid))
            message.command_internal_error(brain)
            return
        return command.CommandManager.input_handler(self, brain, line)


def add_command(name, func):
    return _command_manager.add(name, func)


def command_exists(name):
    return _command_manager.exists(name)


def login_input_handler(actor, line):
    return _command_manager.input_handler(actor, line)


def init():
    global _command_manager
    _command_manager = LoginCommandManager(__name__)

