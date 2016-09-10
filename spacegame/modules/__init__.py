from spacegame.modules import chat, echo, info, jump, login, thrust, warp


def init():
    chat.init()
    echo.init()
    info.init()
    jump.init()
    login.init()
    thrust.init()
    warp.init()


def start():
    thrust.start()
