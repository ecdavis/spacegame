from pantsmud.driver import parser
from pantsmud.util import message
from spacegame.core import command_manager


def position_command(mobile, cmd, args):
    parser.parse([], args)
    message.command_success(mobile, cmd, {"position": mobile.position})


def location_command(mobile, cmd, args):
    parser.parse([], args)
    message.command_success(mobile, cmd, {"celestial": mobile.celestial.name, "star_system": mobile.star_system.name})


def init():
    command_manager.add_command("position", position_command)
    command_manager.add_command("location", location_command)
