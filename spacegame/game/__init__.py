from pantsmud.driver import game
from spacegame.game import echo, handler, login


def get_universe():
    return game.world


def init():
    echo.init()
    handler.init()
    login.init()
