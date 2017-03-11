from spacegame.core import handler, login_manager, user


def init(hooks):
    handler.init(hooks)
    login_manager.init()
