from spacegame.modules import chat, jump, login, thrust, warp


def init():
    chat.init()
    jump.init()
    login.init()
    thrust.init()
    warp.init()


def start():
    thrust.start()
