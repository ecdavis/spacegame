from pantsmud.driver import parser
from pantsmud.util import message


class Service(object):
    def __init__(self, messages):
        self.messages = messages

    def position(self, mobile):
        return mobile.position

    def location(self, mobile):
        return mobile.celestial.name, mobile.star_system.name


class Endpoint(object):
    def __init__(self, service):
        self.service = service

    def position(self, request):
        result = self.service.position(
            request["mobile"]
        )
        return {
            "position": result
        }

    def location(self, request):
        celestial_name, star_system_name = self.service.location(
            request["mobile"]
        )
        return {
            "celestial": celestial_name,
            "star_system": star_system_name
        }


def make_position_command(endpoint):
    def position_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        response = endpoint.position(request)
        message.command_success(brain, cmd, response)
    return position_command


def make_location_command(endpoint):
    def location_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        response = endpoint.location(request)
        message.command_success(brain, cmd, response)
    return location_command


def init(commands, messages):
    service = Service(messages)
    endpoint = Endpoint(service)
    commands.add_command("position", make_position_command(endpoint))
    commands.add_command("location", make_location_command(endpoint))
