import pantsmud.game
from pantsmud.driver import command, parser
from pantsmud.util import error, message


def warp_command(brain, cmd, args):
    params = parser.parse([("celestial_name", parser.STRING)], args)
    mobile = brain.mobile
    universe = pantsmud.game.environment
    celestial = universe.get_celestial(params["celestial_name"], mobile.star_system)
    if not celestial or mobile.star_system is not celestial.star_system:
        raise error.CommandFail()  # TODO Add error message.
    elif mobile.celestial is celestial:
        raise error.CommandFail()  # TODO Add error message.
    mobile.celestial = celestial
    message.command_success(mobile, cmd)


def init():
    command.add_command("warp", warp_command)
