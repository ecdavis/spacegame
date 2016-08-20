from pantsmud.driver import parser
from spacegame.core import command_manager, game


def jump_command(mobile, _, args):
    params = parser.parse([("system_name", parser.STRING)], args)
    universe = game.get_universe()
    solar_system = universe.get_solar_system(params["system_name"])
    if not solar_system:
        mobile.message("jump.fail")  # TODO Add error message.
        return
    elif mobile.solar_system is solar_system:
        mobile.message("jump.fail")  # TODO Add error message.
        return
    mobile.solar_system = solar_system
    mobile.message("jump.success")


def init():
    command_manager.add_command("jump", jump_command)
