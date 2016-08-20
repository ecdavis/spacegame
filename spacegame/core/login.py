import logging
from pantsmud.driver import command, message, parser
from spacegame.core import command_manager, game, user
from spacegame.universe import mobile


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


_login_command_handler = LoginCommandManager(__name__)
login_input_handler = _login_command_handler.input_handler


def register_command(brain, cmd, args):
    params = parser.parse([("name", parser.WORD)], args)
    if user.player_name_exists(params["name"]):
        brain.message("register.fail")
        return
    u = user.User()
    p = mobile.Mobile()
    p.name = params["name"]
    u.player_uuid = p.uuid
    user.save_user(u)
    user.save_player(p)
    brain.message("register.success", {"name": p.name, "uuid": str(u.uuid)})


def login_command(brain, cmd, args):
    params = parser.parse([("uuid", parser.UUID)], args)
    user_uuid = params["uuid"]
    if not user.user_exists(user_uuid):
        logging.debug("login failed due to non-existent user")
        brain.message("login.fail")
        return
    u = user.load_user(user_uuid)
    if not u.player_uuid or not user.player_exists(u.player_uuid):
        logging.debug("login failed due to non-existent player")
        brain.message("login.fail")
        return
    p = user.load_player(u.player_uuid)
    brain.message("login.success", {"name": p.name})
    brain.replace_input_handler(command_manager.command_input_handler, "game")
    p.attach_brain(brain)
    game.get_universe().add_mobile(p)


def quit_command(brain, cmd, args):
    parser.parse([], args)
    brain.close()


def init():
    _login_command_handler.add("register", register_command)
    _login_command_handler.add("login", login_command)
    _login_command_handler.add("quit", quit_command)
