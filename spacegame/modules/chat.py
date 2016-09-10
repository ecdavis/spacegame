from pantsmud.driver import parser
from pantsmud.util import error, message
from spacegame.core import command_manager


def chat_global_command(mobile, cmd, args):
    params = parser.parse([("message", parser.STRING)], args)
    universe = mobile.universe
    data = {"mobile_from": mobile.name, "message": params["message"]}
    message.command_success(mobile, cmd, data)
    for m in (universe.mobiles[u] for u in universe.mobiles if u is not mobile.uuid):
        message.notify(m, cmd, data)


def chat_private_command(mobile, cmd, args):
    params = parser.parse([("mobile_name", parser.WORD), ("message", parser.STRING)], args)
    target = mobile.universe.get_mobile(params["mobile_name"])
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


def init():
    command_manager.add_command("chat.global", chat_global_command)
    command_manager.add_command("chat.private", chat_private_command)
