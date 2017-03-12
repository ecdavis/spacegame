from pantsmud.driver import parser
from pantsmud.util import error, message


class Service(object):
    def __init__(self, universe, messages):
        self.universe = universe
        self.messages = messages

    def chat_global(self, mobile, message):
        for m in self.universe.get_mobiles():
            if m is mobile:
                continue
            self.messages.chat_global(m, mobile.name, message)
        return mobile.name, message

    def chat_private(self, mobile, target_name, message):
        target = self.universe.get_entity(target_name)
        if not target:
            raise error.CommandFail()  # TODO Add error message
        if target is mobile:
            raise error.CommandFail()  # TODO Add error message
        self.messages.chat_private(target, mobile.name, message)
        return mobile.name, target.name, message


def make_chat_global_endpoint(service):
    def chat_global_endpoint(request):
        mobile_name, message = service.chat_global(
            request["mobile"],
            request["message"]
        )
        return {
            "mobile_from": mobile_name,
            "message": message
        }
    return chat_global_endpoint


def make_chat_private_endpoint(service):
    def chat_private_endpoint(request):
        from_name, to_name, message = service.chat_private(
            request["mobile"],
            request["target_name"],
            request["message"]
        )
        return {
            "mobile_from": from_name,
            "mobile_to": to_name,
            "message": message
        }
    return chat_private_endpoint


def make_chat_global_command(endpoint):
    def chat_global_command(brain, cmd, args):
        params = parser.parse([("message", parser.STRING)], args)
        request = {
            "mobile": brain.mobile,
            "message": params["message"]
        }
        response = endpoint(request)
        message.command_success(brain, cmd, response)
    return chat_global_command


def make_chat_private_command(endpoint):
    def chat_private_command(brain, cmd, args):
        params = parser.parse([("mobile_name", parser.WORD), ("message", parser.STRING)], args)
        request = {
            "mobile": brain.mobile,
            "target_name": params["mobile_name"],
            "message": params["message"]
        }
        response = endpoint(request)
        message.command_success(brain, cmd, response)
    return chat_private_command


def init(commands, messages, universe):
    service = Service(universe, messages)
    commands.add_command(
        "chat.global",
        make_chat_global_command(
            make_chat_global_endpoint(service)
        )
    )
    commands.add_command(
        "chat.private",
        make_chat_private_command(
            make_chat_private_endpoint(service)
        )
    )
