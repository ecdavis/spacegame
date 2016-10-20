import random
import pantsmud.game
from pantsmud.driver import auxiliary, hook
from pantsmud.util import error
from spacegame.core import aux_types, hook_types
from spacegame.universe import entity


class WarpAux(object):
    def __init__(self):
        self.scanner = []

    def load_data(self, data):
        pass

    def save_data(self):
        return {}


def do_warp(mobile, destination_uuid):
    destination, position = _find_warp_destination(mobile, destination_uuid)
    if destination is None or position is None:
        raise error.CommandFail("no destination")
    hook.run(hook_types.CELESTIAL_EXIT, mobile)
    mobile.celestial = destination
    mobile.position = position
    return None


def _find_warp_destination(mobile, destination_uuid):
    beacons = mobile.star_system.get_entities(is_warp_beacon=True)
    for beacon in beacons:
        if beacon.uuid == destination_uuid:
            return beacon.celestial, _random_position_around(beacon.position)
    celestials = mobile.star_system.get_celestials(uuids=mobile.aux["warp"].scanner)
    for celestial in celestials:
        if celestial.uuid == destination_uuid:
            return celestial, _random_position_around((0+celestial.warp_radius, 0, 0))
    return None, None


def _random_position_around(position):
    add = (random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))
    return (
        position[0] + add[0],
        position[1] + add[1],
        position[2] + add[2]
    )


def do_warp_beacon(mobile):
    beacon = entity.Entity(is_warp_beacon=True)
    beacon.celestial = mobile.celestial
    beacon.position = mobile.position
    pantsmud.game.environment.add_entity(beacon)
    return {
        "beacon_uuid": str(beacon.uuid)
    }


def do_warp_scan(mobile):
    beacons = mobile.star_system.get_entities(is_warp_beacon=True)
    beacon_data = {b.name: str(b.uuid) for b in beacons if b.celestial is not mobile.celestial}
    celestials = mobile.star_system.get_celestials(uuids=mobile.aux["warp"].scanner)
    celestial_data = {c.name: str(c.uuid) for c in celestials if c is not mobile.celestial}
    return {
        "beacons": beacon_data,
        "celestials": celestial_data
    }


def do_warp_scan_activate(mobile):
    celestials = mobile.star_system.get_celestials()
    celestial_data = {c.name: c.uuid for c in celestials if c is not mobile.celestial}
    mobile.aux["warp"].scanner = celestial_data.values()[:]
    for k, v in celestial_data.items():  # TODO ugh
        celestial_data[k] = str(v)
    return {
        "celestials": celestial_data
    }


def clear_warp_scanner(_, mobile):
    mobile.aux["warp"].scanner = []


def init():
    auxiliary.install(aux_types.AUX_TYPE_ENTITY, "warp", WarpAux)
    hook.add(hook_types.CELESTIAL_EXIT, clear_warp_scanner)
    hook.add(hook_types.STAR_SYSTEM_EXIT, clear_warp_scanner)
