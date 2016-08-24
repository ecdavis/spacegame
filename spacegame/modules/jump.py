from pantsmud.driver import error, message, parser
import random
from spacegame.core import command_manager, game


def jump_command(mobile, cmd, args):
    params = parser.parse([("system_name", parser.STRING)], args)
    universe = game.get_universe()
    star_system = universe.get_star_system(params["system_name"])
    if not star_system:
        raise error.CommandFail()  # TODO Add error message.
    elif mobile.star_system is star_system:
        raise error.CommandFail()  # TODO Add error message.
    mobile.celestial = random.choice(list(star_system.core_celestials))
    message.command_success(mobile, cmd, None)


def init():
    command_manager.add_command("jump", jump_command)
