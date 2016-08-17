from pantsmud.driver import game
from spacegame.game import echo


def get_universe():
    return game.world


def init():
    echo.init()
