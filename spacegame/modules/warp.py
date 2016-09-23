import pantsmud.game
from pantsmud.driver import auxiliary, command, hook, parser
from pantsmud.util import error, message
from spacegame.core import hook_types


class WarpAux(object):
    def __init__(self):
        self.scanner = []

    def load_data(self, data):
        pass

    def save_data(self):
        return {}


def warp_command(brain, cmd, args):
    params = parser.parse([("celestial_name", parser.STRING)], args)
    mobile = brain.mobile
    universe = pantsmud.game.environment
    celestial = universe.get_celestial(params["celestial_name"], mobile.star_system)
    if not celestial or celestial.uuid not in mobile.aux["warp"].scanner:
        raise error.CommandFail("Could not find celestial to warp to.")  # TODO Add error message.
    elif mobile.celestial is celestial:
        raise error.CommandFail()  # TODO Add error message.
    hook.run(hook_types.CELESTIAL_EXIT, mobile)
    mobile.celestial = celestial
    message.command_success(mobile, cmd)


def warp_scan_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    universe = pantsmud.game.environment
    celestials = universe.get_celestials(star_systems=[mobile.star_system], uuids=mobile.aux["warp"].scanner)
    celestial_uuids = [c.uuid for c in celestials]
    mobile.aux["warp"].scanner = celestial_uuids
    celestial_names = [c.name for c in celestials]
    message.command_success(mobile, cmd, {"celestial_names": celestial_names})


def warp_scan_activate_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    universe = pantsmud.game.environment
    celestials = universe.get_celestials(star_systems=[mobile.star_system])
    celestial_uuids = [c.uuid for c in celestials]
    mobile.aux["warp"].scanner = celestial_uuids
    celestial_names = [c.name for c in celestials]
    message.command_success(mobile, cmd, {"celestial_names": celestial_names})


def clear_warp_scanner(_, mobile):
    mobile.aux["warp"].scanner = []


def init():
    auxiliary.install(auxiliary.AUX_TYPE_MOBILE, "warp", WarpAux)
    command.add_command("warp", warp_command)
    command.add_command("warp.scan", warp_scan_command)
    command.add_command("warp.scan.activate", warp_scan_activate_command)
    hook.add("celestial.exit", clear_warp_scanner)
    hook.add("star_system.exit", clear_warp_scanner)
