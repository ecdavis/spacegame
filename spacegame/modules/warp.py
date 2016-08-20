from pantsmud.driver import parser
from spacegame.core import command_manager, game


def warp_command(mobile, _, args):
    params = parser.parse([("celestial_name", parser.STRING)], args)
    universe = game.get_universe()
    celestial = universe.get_celestial(params["celestial_name"], mobile.star_system)
    if not celestial:
        mobile.message("warp.fail")  # TODO Add error message.
        return
    elif mobile.celestial is celestial:
        mobile.message("warp.fail")  # TODO Add error message.
        return
    elif mobile.star_system is not celestial.star_system:
        mobile.message("warp.fail")  # TODO Add error message.
        return
    mobile.celestial = celestial
    mobile.message("warp.success")


def init():
    command_manager.add_command("warp", warp_command)
