from pantsmud.driver import error, message, parser
from spacegame.core import command_manager, game


def warp_command(mobile, cmd, args):
    params = parser.parse([("celestial_name", parser.STRING)], args)
    universe = game.get_universe()
    celestial = universe.get_celestial(params["celestial_name"], mobile.star_system)
    if not celestial or mobile.star_system is not celestial.star_system:
        raise error.CommandFail()  # TODO Add error message.
    elif mobile.celestial is celestial:
        raise error.CommandFail()  # TODO Add error message.
    mobile.celestial = celestial
    message.command_success(mobile, cmd)


def init():
    command_manager.add_command("warp", warp_command)
