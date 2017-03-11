from pantsmud.driver import hook
from spacegame.core import handler, login_manager, user


def init():
    handler.init(hook)
    login_manager.init()
