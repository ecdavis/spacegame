import logging
from pantsmud.driver import command, message, parser
from spacegame import echo, user


class LoginCommandManager(command.CommandManager):
    def input_handler(self, brain, line):
        if not brain.is_user:
            logging.error("Brain '%s' has login input handler but it is not a user.", str(brain.uuid))
            message.command_internal_error(brain)
            return
        return command.CommandManager.input_handler(self, brain, line)


_login_command_handler = LoginCommandManager(__name__)
login_input_handler = _login_command_handler.input_handler


def register_command(brain, cmd, args):
    parser.parse([], args)
    u = user.User()
    user.save_user(u)
    brain.message("register.success", {"uuid": str(u.uuid)})


def login_command(brain, cmd, args):
    params = parser.parse([("uuid", parser.UUID)], args)
    user_uuid = params["uuid"]
    if not user.user_exists(user_uuid):
        logging.debug("login failed due to non-existent user")
        brain.message("login.fail")
        return
    u = user.load_user(user_uuid)
    brain.message("login.success")
    brain.replace_input_handler(echo.echo_input_handler, "echo")


def quit_command(brain, cmd, args):
    parser.parse([], args)
    brain.close()


def init():
    _login_command_handler.add("register", register_command)
    _login_command_handler.add("login", login_command)
    _login_command_handler.add("quit", quit_command)
