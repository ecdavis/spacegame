from pantsmud.driver import parser


class Service(object):
    def __init__(self, messages):
        self.messages = messages

    def position(self, mobile):
        data = {
            "position": mobile.position
        }
        self.messages.command_success(mobile, "position", data)

    def location(self, mobile):
        data = {
            "celestial": mobile.celestial.name,
            "star_system": mobile.star_system.name
        }
        self.messages.command_success(mobile, "location", data)


class Endpoint(object):
    def __init__(self, service):
        self.service = service

    def position(self, request):
        self.service.position(
            request["mobile"]
        )

    def location(self, request):
        self.service.location(
            request["mobile"]
        )


def make_position_command(endpoint):
    def position_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        endpoint.position(request)
    return position_command


def make_location_command(endpoint):
    def location_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        endpoint.location(request)
    return location_command


def init(commands, messages):
    service = Service(messages)
    endpoint = Endpoint(service)
    commands.add_command("position", make_position_command(endpoint))
    commands.add_command("location", make_location_command(endpoint))
