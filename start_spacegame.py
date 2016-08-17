import logging
import os.path
import pants
from pantsmud.driver import game, net
import spacegame
from spacegame.universe import persist


UNIVERSE_PATH = os.path.abspath("data/universe/")
UNIVERSE_FILE = os.path.join(UNIVERSE_PATH, "universe.json")


if __name__ == '__main__':
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.DEBUG)

    # Initialize the game.
    spacegame.init()
    engine = pants.Engine.instance()
    universe = persist.load_universe(UNIVERSE_FILE)
    game.init(engine, universe)
    net.init()
    game.start()
