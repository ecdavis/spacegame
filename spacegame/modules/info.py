from pantsmud.driver import parser
from pantsmud.util import message


class Service(object):
    def position(self, mobile):
        return mobile.position

    def location(self, mobile):
        return mobile.celestial.name, mobile.star_system.name


def make_position_endpoint(service):
    def position_endpoint(request):
        result = service.position(
            request["mobile"]
        )
        return {
            "position": result
        }
    return position_endpoint


def make_location_endpoint(service):
    def location_endpoint(request):
        celestial_name, star_system_name = service.location(
            request["mobile"]
        )
        return {
            "celestial": celestial_name,
            "star_system": star_system_name
        }
    return location_endpoint


def make_position_command(endpoint):
    def position_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        response = endpoint(request)
        message.command_success(brain, cmd, response)
    return position_command


def make_location_command(endpoint):
    def location_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        response = endpoint(request)
        message.command_success(brain, cmd, response)
    return location_command


def init(commands):
    service = Service()
    commands.add_command(
        "position",
        make_position_command(
            make_position_endpoint(service)
        )
    )
    commands.add_command(
        "location",
        make_location_command(
            make_location_endpoint(service)
        )
    )
