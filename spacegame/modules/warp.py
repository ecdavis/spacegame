import random
import pantsmud.game
from pantsmud.driver import parser
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


class Service(object):
    def __init__(self, entities, hooks, universe):
        self.entities = entities
        self.hooks = hooks
        self.universe = universe

    def warp(self, mobile, destination_uuid):
        destination, position = self._find_warp_destination(mobile, destination_uuid)
        if destination is None or position is None:
            raise error.CommandFail("no destination")
        self.hooks.run(hook_types.CELESTIAL_EXIT, mobile)
        mobile.celestial = destination
        mobile.position = position
        return None

    def warp_beacon(self, mobile):
        beacon = self.entities.Entity(is_warp_beacon=True)
        beacon.celestial = mobile.celestial
        beacon.position = mobile.position
        self.universe.add_entity(beacon)
        return {
            "beacon_uuid": str(beacon.uuid)
        }

    def warp_scan(self, mobile):
        beacons = mobile.star_system.get_entities(is_warp_beacon=True)
        beacon_data = {b.name: str(b.uuid) for b in beacons if b.celestial is not mobile.celestial}
        celestials = mobile.star_system.get_celestials(uuids=mobile.aux["warp"].scanner)
        celestial_data = {c.name: str(c.uuid) for c in celestials if c is not mobile.celestial}
        return {
            "beacons": beacon_data,
            "celestials": celestial_data
        }

    def warp_scan_activate(self, mobile):
        celestials = mobile.star_system.get_celestials()
        celestial_data = {c.name: c.uuid for c in celestials if c is not mobile.celestial}
        mobile.aux["warp"].scanner = celestial_data.values()[:]
        for k, v in celestial_data.items():  # TODO ugh
            celestial_data[k] = str(v)
        return {
            "celestials": celestial_data
        }

    def _find_warp_destination(self, mobile, destination_uuid):
        beacons = mobile.star_system.get_entities(is_warp_beacon=True)
        for beacon in beacons:
            if beacon.uuid == destination_uuid:
                return beacon.celestial, _random_position_around(beacon.position)
        celestials = mobile.star_system.get_celestials(uuids=mobile.aux["warp"].scanner)
        for celestial in celestials:
            if celestial.uuid == destination_uuid:
                return celestial, _random_position_around((0+celestial.warp_radius, 0, 0))
        return None, None


class Endpoint(object):
    def __init__(self, service):
        self.service = service

    def warp(self, request):
        return self.service.warp(
            request["mobile"],
            request["destination_uuid"]
        )

    def warp_beacon(self, request):
        return self.service.warp_beacon(
            request["mobile"]
        )

    def warp_scan(self, request):
        return self.service.warp_scan(
            request["mobile"]
        )

    def warp_scan_activate(self, request):
        return self.service.warp_scan_activate(
            request["mobile"]
        )


def make_warp_command(endpoint):
    def warp_command(brain, cmd, args):
        params = parser.parse([("destination_uuid", parser.UUID)], args)
        request = {
            "mobile": brain.mobile,
            "destination_uuid": params["destination_uuid"]
        }
        response = endpoint.warp(request)
        message.command_success(brain, cmd, response)
    return warp_command


def make_warp_beacon_command(endpoint):
    def warp_beacon_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        response = endpoint.warp_beacon(request)
        message.command_success(brain, cmd, response)
    return warp_beacon_command


def make_warp_scan_command(endpoint):
    def warp_scan_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        response = endpoint.warp_scan(request)
        message.command_success(brain, cmd, response)
    return warp_scan_command


def make_warp_scan_activate_command(endpoint):
    def warp_scan_activate_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        response = endpoint.warp_scan_activate(request)
        message.command_success(brain, cmd, response)
    return warp_scan_activate_command


def _random_position_around(position):
    add = (random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))
    return (
        position[0] + add[0],
        position[1] + add[1],
        position[2] + add[2]
    )


def clear_warp_scanner(_, mobile):
    mobile.aux["warp"].scanner = []


def init(auxiliaries, commands, hooks, universe):
    auxiliaries.install(aux_types.AUX_TYPE_ENTITY, "warp", WarpAux)
    hooks.add(hook_types.CELESTIAL_EXIT, clear_warp_scanner)
    hooks.add(hook_types.STAR_SYSTEM_EXIT, clear_warp_scanner)
    service = Service(entity, hooks, universe)
    endpoint = Endpoint(service)
    commands.add_command("warp", make_warp_command(endpoint))
    commands.add_command("warp.beacon", make_warp_beacon_command(endpoint))
    commands.add_command("warp.scan", make_warp_scan_command(endpoint))
    commands.add_command("warp.scan.activate", make_warp_scan_activate_command(endpoint))
