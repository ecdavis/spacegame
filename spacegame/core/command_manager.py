import logging
from pantsmud.driver import command
from pantsmud.util import message


_command_manager = None


class GameCommandManager(command.CommandManager):
    def run(self, brain, cmd, args):
        command.CommandManager.run(self, brain.mobile, cmd, args)

    def input_handler(self, brain, line):
        if not brain.mobile:
            logging.error("Brain '%s' has game input handler but does not have a mobile attached.", str(brain.uuid))
            message.command_internal_error(brain)
            return
        return command.CommandManager.input_handler(self, brain, line)


def add_command(name, func):
    return _command_manager.add(name, func)


def command_exists(name):
    return _command_manager.exists(name)


def command_input_handler(actor, line):
    return _command_manager.input_handler(actor, line)


def init():
    global _command_manager
    _command_manager = GameCommandManager(__name__)

