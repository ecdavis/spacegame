import random
import pantsmud.game
from pantsmud.driver import command, parser
from pantsmud.util import error, message


def jump_command(brain, cmd, args):
    params = parser.parse([("system_name", parser.STRING)], args)
    mobile = brain.mobile
    universe = pantsmud.game.environment
    star_system = universe.get_star_system(params["system_name"])
    if not star_system:
        raise error.CommandFail()  # TODO Add error message.
    elif mobile.star_system is star_system:
        raise error.CommandFail()  # TODO Add error message.
    mobile.celestial = random.choice(list(star_system.core_celestials))
    message.command_success(mobile, cmd, None)


def init():
    command.add_command("jump", jump_command)
