from pantsmud.driver import parser
from pantsmud.util import error, message


def chat_global_command(brain, cmd, args):
    params = parser.parse([("message", parser.STRING)], args)
    mobile = brain.mobile
    universe = mobile.universe
    data = {"mobile_from": mobile.name, "message": params["message"]}
    message.command_success(mobile, cmd, data)
    for m in universe.get_mobiles():
        if m is mobile:
            continue
        message.notify(m, cmd, data)


def chat_private_command(brain, cmd, args):
    params = parser.parse([("mobile_name", parser.WORD), ("message", parser.STRING)], args)
    mobile = brain.mobile
    target = mobile.universe.get_entity(params["mobile_name"])
    if not target:
        raise error.CommandFail()  # TODO Add error message.
    if target is mobile:
        raise error.CommandFail()  # TODO Add error message.
    data = {
        "mobile_from": mobile.name,
        "mobile_to": target.name,
        "message": params["message"]
    }
    message.notify(target, cmd, data)
    message.command_success(mobile, cmd, data)


def init(commands):
    commands.add_command("chat.global", chat_global_command)
    commands.add_command("chat.private", chat_private_command)
