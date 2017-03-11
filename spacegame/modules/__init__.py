from pantsmud.driver import auxiliary, command, hook
from spacegame.modules import chat, echo, info, inventory, jump, login, thrust, warp


def init():
    chat.init(command)
    echo.init(command)
    info.init(command)
    inventory.init(auxiliary, command, hook)
    jump.init()
    login.init()
    thrust.init()
    warp.init()


def start():
    thrust.start()
