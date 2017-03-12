from pantsmud.driver import parser
from pantsmud.util import error


class Service(object):
    def __init__(self, universe, messages):
        self.universe = universe
        self.messages = messages

    def chat_global(self, mobile, message):
        data = {"mobile_from": mobile.name, "message": message}
        for m in self.universe.get_mobiles():
            if m is mobile:
                continue
            self.messages.notify(m, "chat.global", data)
        self.messages.command_success(mobile, "chat.global", data)

    def chat_private(self, mobile, target_name, message):
        target = self.universe.get_entity(target_name)
        if not target:
            raise error.CommandFail()  # TODO Add error message
        if target is mobile:
            raise error.CommandFail()  # TODO Add error message
        data = {
            "mobile_from": mobile.name,
            "mobile_to": target.name,
            "message": message
        }
        self.messages.notify(target, "chat.private", data)
        self.messages.command_success(mobile, "chat.private", data)


class Endpoint(object):
    def __init__(self, service):
        self.service = service

    def chat_global(self, request):
        self.service.chat_global(
            request["mobile"],
            request["message"]
        )

    def chat_private(self, request):
        self.service.chat_private(
            request["mobile"],
            request["target_name"],
            request["message"]
        )


def make_chat_global_command(endpoint):
    def chat_global_command(brain, cmd, args):
        params = parser.parse([("message", parser.STRING)], args)
        request = {
            "mobile": brain.mobile,
            "message": params["message"]
        }
        endpoint.chat_global(request)
    return chat_global_command


def make_chat_private_command(endpoint):
    def chat_private_command(brain, cmd, args):
        params = parser.parse([("mobile_name", parser.WORD), ("message", parser.STRING)], args)
        request = {
            "mobile": brain.mobile,
            "target_name": params["mobile_name"],
            "message": params["message"]
        }
        endpoint.chat_private(request)
    return chat_private_command


def init(commands, messages, universe):
    service = Service(universe, messages)
    endpoint = Endpoint(service)
    commands.add_command("chat.global", make_chat_global_command(endpoint))
    commands.add_command("chat.private", make_chat_private_command(endpoint))
