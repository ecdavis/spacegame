from pantsmud.driver import auxiliary, command, hook
from spacegame.core import login_manager
from spacegame.modules import chat, echo, info, inventory, jump, login, thrust, warp


def init():
    chat.init(command)
    echo.init(command)
    info.init(command)
    inventory.init(auxiliary, command, hook)
    jump.init(command)
    login.init(login_manager)
    thrust.init()
    warp.init()


def start():
    thrust.start()
