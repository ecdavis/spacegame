from pantsmud.driver import parser
import random
from spacegame.core import command_manager, game


def jump_command(mobile, _, args):
    params = parser.parse([("system_name", parser.STRING)], args)
    universe = game.get_universe()
    star_system = universe.get_star_system(params["system_name"])
    if not star_system:
        mobile.message("jump.fail")  # TODO Add error message.
        return
    elif mobile.star_system is star_system:
        mobile.message("jump.fail")  # TODO Add error message.
        return
    mobile.celestial = random.choice(list(star_system.core_celestials))
    mobile.message("jump.success")


def init():
    command_manager.add_command("jump", jump_command)
