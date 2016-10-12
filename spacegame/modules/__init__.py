from spacegame.modules import chat, echo, info, inventory, jump, login, thrust, warp


def init():
    chat.init()
    echo.init()
    info.init()
    inventory.init()
    jump.init()
    login.init()
    thrust.init()
    warp.init()


def start():
    thrust.start()
