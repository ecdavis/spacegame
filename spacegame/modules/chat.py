from pantsmud.driver import parser

from spacegame.core import command_manager


def chat_global_command(mobile, _, args):
    params = parser.parse([("message", parser.STRING)], args)
    universe = mobile.universe
    for m in (universe.mobiles[u] for u in universe.mobiles):
        m.message("chat.global", {"mobile_from": mobile.name, "message": params["message"]})


def chat_private_command(mobile, _, args):
    params = parser.parse([("mobile_name", parser.WORD), ("message", parser.STRING)], args)
    target = mobile.universe.get_mobile(params["mobile_name"])
    if not target:
        mobile.message("chat.private.fail")  # TODO Add error message.
        return
    if target is mobile:
        mobile.message("chat.private.fail")  # TODO Add error message.
        return
    data = {
        "mobile_from": mobile.name,
        "mobile_to": target.name,
        "message": params["message"]
    }
    target.message("chat.private", data)
    mobile.message("chat.private", data)


def init():
    command_manager.add_command("chat.global", chat_global_command)
    command_manager.add_command("chat.private", chat_private_command)
