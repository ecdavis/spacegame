import logging
import random
import pantsmud.game
from pantsmud.driver import command, parser
from pantsmud.util import error, message
from spacegame.core import login_manager, user
from spacegame.universe import mobile


def register_command(brain, cmd, args):
    params = parser.parse([("name", parser.WORD)], args)
    if user.player_name_exists(params["name"]):
        raise error.CommandFail()  # TODO Add error message.
    u = user.User()
    p = mobile.Mobile()
    p.name = params["name"]
    star_system = random.choice(list(pantsmud.game.environment.core_star_systems))
    p.celestial = random.choice(list(star_system.core_celestials))
    u.player_uuid = p.uuid
    user.save_user(u)
    user.save_player(p)
    message.command_success(brain, cmd, {"name": p.name, "uuid": str(u.uuid)})


def login_command(brain, cmd, args):
    params = parser.parse([("uuid", parser.UUID)], args)
    user_uuid = params["uuid"]
    if not user.user_exists(user_uuid):
        logging.debug("login failed due to non-existent user")
        raise error.CommandFail()  # TODO Add error message.
    u = user.load_user(user_uuid)
    if not u.player_uuid or not user.player_exists(u.player_uuid):
        logging.debug("login failed due to non-existent player")
        raise error.CommandFail()  # TODO Add error message.
    p = user.load_player(u.player_uuid)
    message.command_success(brain, cmd, {"name": p.name})
    brain.replace_input_handler(command.command_input_handler, "game")
    p.attach_brain(brain)
    pantsmud.game.environment.add_mobile(p)


def quit_command(brain, _, args):
    parser.parse([], args)
    brain.close()


def init():
    login_manager.add_command("register", register_command)
    login_manager.add_command("login", login_command)
    login_manager.add_command("quit", quit_command)
