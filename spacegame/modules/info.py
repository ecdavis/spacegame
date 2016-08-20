from pantsmud.driver import parser
from spacegame.core import command_manager


def position_command(mobile, _, args):
    params = parser.parse([], args)
    mobile.message("position.success", {"position": mobile.position})


def location_command(mobile, _, args):
    params = parser.parse([], args)
    mobile.message("location.success", {"celestial": mobile.celestial.name, "star_system": mobile.star_system.name})


def init():
    command_manager.add_command("position", position_command)
    command_manager.add_command("location", location_command)
