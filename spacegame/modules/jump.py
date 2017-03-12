import random
from pantsmud.driver import parser
from pantsmud.util import error, message
from spacegame.core import hook_types


class Service(object):
    def __init__(self, hooks, messages, universe):
        self.hooks = hooks
        self.messages = messages
        self.universe = universe

    def jump(self, mobile, system_name):
        star_system = self.universe.get_star_system(system_name)
        if not star_system:
            raise error.CommandFail()  # TODO Add error message.
        elif mobile.star_system is star_system:
            raise error.CommandFail()  # TODO Add error message.
        self.hooks.run(hook_types.STAR_SYSTEM_EXIT, mobile)
        mobile.celestial = random.choice(list(star_system.core_celestials))


class Endpoint(object):
    def __init__(self, service):
        self.service = service

    def jump(self, request):
        self.service.jump(
            request["mobile"],
            request["system_name"]
        )


def make_jump_command(endpoint):
    def jump_command(brain, cmd, args):
        params = parser.parse([("system_name", parser.STRING)], args)
        request = {
            "mobile": brain.mobile,
            "system_name": params["system_name"]
        }
        endpoint.jump(request)
        message.command_success(brain, cmd, None)
    return jump_command


def init(commands, hooks, messages, universe):
    service = Service(hooks, messages, universe)
    endpoint = Endpoint(service)
    commands.add_command("jump", make_jump_command(endpoint))
