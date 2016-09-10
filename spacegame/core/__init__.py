from spacegame.core import command_manager, handler, login_manager, user


def init():
    command_manager.init()
    handler.init()
    login_manager.init()
