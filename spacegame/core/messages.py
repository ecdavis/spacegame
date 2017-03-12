from pantsmud.util.message import notify


class Messages(object):
    def chat_global(self, actor, mobile_name, message):
        notify(
            actor,
            "chat.global",
            {
                "mobile_from": mobile_name,
                "message": message
            }
        )

    def chat_private(self, actor, from_name, message):
        notify(
            actor,
            "chat.private",
            {
                "mobile_from": from_name,
                "mobile_to": actor.name,
                "message": message
            }
        )
