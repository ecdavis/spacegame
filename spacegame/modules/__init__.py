from spacegame.modules import chat, info, jump, login, thrust, warp


def init():
    chat.init()
    info.init()
    jump.init()
    login.init()
    thrust.init()
    warp.init()


def start():
    thrust.start()
