from pantsmud.driver import command, parser
from pantsmud.util import message


def position_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    message.command_success(mobile, cmd, {"position": mobile.position})


def location_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    message.command_success(mobile, cmd, {"celestial": mobile.celestial.name, "star_system": mobile.star_system.name})


def init():
    command.add_command("position", position_command)
    command.add_command("location", location_command)
