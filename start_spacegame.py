import logging
import os.path
import pants
from pantsmud.driver import game, net
import spacegame
from spacegame.universe import persist


UNIVERSE_PATH = os.path.abspath("data/universe/")
UNIVERSE_FILE = os.path.join(UNIVERSE_PATH, "universe.json")
SOLAR_SYSTEM_PATH = os.path.join(UNIVERSE_PATH, "solar_systems")


def load_universe():
    u = persist.load_universe(UNIVERSE_FILE)
    for s in persist.load_solar_systems(SOLAR_SYSTEM_PATH):
        u.add_solar_system(s)
    return u


def save_universe(u):
    persist.save_solar_systems(SOLAR_SYSTEM_PATH, u)
    persist.save_universe(UNIVERSE_FILE, u)


if __name__ == '__main__':
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.DEBUG)

    # Initialize the game.
    spacegame.init()
    engine = pants.Engine.instance()
    universe = load_universe()
    game.init(engine, universe)
    net.init()
    game.start()
    save_universe(universe)
