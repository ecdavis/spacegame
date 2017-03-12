import random
import pantsmud.game
from pantsmud.driver import hook, parser
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
        self.messages.command_success(mobile, "jump", None)


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
    return jump_command


def init(commands, universe):
    service = Service(hook, message, universe)
    endpoint = Endpoint(service)
    commands.add_command("jump", make_jump_command(endpoint))
