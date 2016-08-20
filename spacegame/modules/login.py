import logging
from pantsmud.driver import parser
from spacegame.core import command_manager, game, login_manager, user
from spacegame.universe import mobile


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
    login_manager.add_command("register", register_command)
    login_manager.add_command("login", login_command)
    login_manager.add_command("quit", quit_command)
