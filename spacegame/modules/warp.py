import random
import pantsmud.game
from pantsmud.driver import auxiliary, command, hook, parser
from pantsmud.util import error, message
from spacegame.core import aux_types, hook_types
from spacegame.universe import entity


class WarpAux(object):
    def __init__(self):
        self.scanner = []

    def load_data(self, data):
        pass

    def save_data(self):
        return {}


def warp_command(brain, cmd, args):
    params = parser.parse([("destination_uuid", parser.UUID)], args)
    mobile = brain.mobile
    destination, position = _find_warp_destination(mobile, params["destination_uuid"])
    if destination is None or position is None:
        raise error.CommandFail("no destination")
    elif destination is mobile.celestial:
        raise error.CommandFail("destination is current celestial")
    hook.run(hook_types.CELESTIAL_EXIT, mobile)
    mobile.celestial = destination
    mobile.position = position
    message.command_success(mobile, cmd)


def _find_warp_destination(mobile, destination_uuid):
    beacons = mobile.star_system.get_entities(is_warp_beacon=True)
    for beacon in beacons:
        if beacon.uuid == destination_uuid:
            return beacon.celestial, _random_position_around(beacon.position)
    celestials = mobile.star_system.get_celestials(uuids=mobile.aux["warp"].scanner)
    for celestial in celestials:
        if celestial.uuid == destination_uuid:
            return celestial, _random_position_around((0, 0, 0))
    return None, None


def _random_position_around(position):
    add = (random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))
    return (
        position[0] + add[0],
        position[1] + add[1],
        position[2] + add[2]
    )


def warp_beacon_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    beacon = entity.Entity(is_warp_beacon=True)
    beacon.celestial = mobile.celestial
    beacon.position = mobile.position
    pantsmud.game.environment.add_entity(beacon)
    message.command_success(mobile, cmd, {"beacon_uuid": str(beacon.uuid)})


def warp_scan_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    beacons = mobile.star_system.get_entities(is_warp_beacon=True)
    beacon_data = {b.name: str(b.uuid) for b in beacons if b.celestial is not mobile.celestial}
    celestials = mobile.star_system.get_celestials(uuids=mobile.aux["warp"].scanner)
    celestial_data = {c.name: str(c.uuid) for c in celestials if c is not mobile.celestial}
    message.command_success(mobile, cmd, {"beacons": beacon_data, "celestials": celestial_data})


def warp_scan_activate_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    celestials = mobile.star_system.get_celestials()
    celestial_data = {c.name: c.uuid for c in celestials if c is not mobile.celestial}
    mobile.aux["warp"].scanner = celestial_data.values()[:]
    for k, v in celestial_data.items():  # TODO ugh
        celestial_data[k] = str(v)
    message.command_success(mobile, cmd, {"celestials": celestial_data})


def clear_warp_scanner(_, mobile):
    mobile.aux["warp"].scanner = []


def init():
    auxiliary.install(aux_types.AUX_TYPE_ENTITY, "warp", WarpAux)
    command.add_command("warp", warp_command)
    command.add_command("warp.beacon", warp_beacon_command)
    command.add_command("warp.scan", warp_scan_command)
    command.add_command("warp.scan.activate", warp_scan_activate_command)
    hook.add("celestial.exit", clear_warp_scanner)
    hook.add("star_system.exit", clear_warp_scanner)
