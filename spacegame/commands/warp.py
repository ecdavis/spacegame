from pantsmud.driver import parser
from pantsmud.util import message
from spacegame.modules import warp


def warp_command(brain, cmd, args):
    params = parser.parse([("destination_uuid", parser.UUID)], args)
    result = warp.do_warp(brain.mobile, params["destination_uuid"])
    message.command_success(brain, cmd, result)


def warp_beacon_command(brain, cmd, args):
    parser.parse([], args)
    result = warp.do_warp_beacon(brain.mobile)
    message.command_success(brain, cmd, result)


def warp_scan_command(brain, cmd, args):
    parser.parse([], args)
    result = warp.do_warp_scan(brain.mobile)
    message.command_success(brain, cmd, result)


def warp_scan_activate_command(brain, cmd, args):
    parser.parse([], args)
    result = warp.do_warp_scan_activate(brain.mobile)
    message.command_success(brain, cmd, result)


def init(commands):
    commands.add_command("warp", warp_command)
    commands.add_command("warp.beacon", warp_beacon_command)
    commands.add_command("warp.scan", warp_scan_command)
    commands.add_command("warp.scan.activate", warp_scan_activate_command)
