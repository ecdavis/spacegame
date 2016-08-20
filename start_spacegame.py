import logging
import os.path
import pants
from pantsmud.driver import game, net
import spacegame
from spacegame.universe import persist


UNIVERSE_PATH = os.path.abspath("data/universe/")
UNIVERSE_FILE = os.path.join(UNIVERSE_PATH, "universe.json")
STAR_SYSTEM_PATH = os.path.join(UNIVERSE_PATH, "star_systems")
CELESTIAL_PATH = os.path.join(UNIVERSE_PATH, "celestials")


def load_universe():
    u = persist.load_universe(UNIVERSE_FILE)
    for s in persist.load_star_systems(STAR_SYSTEM_PATH):
        u.add_star_system(s)
    for c in persist.load_celestials(CELESTIAL_PATH):
        u.add_celestial(c)
    return u


def save_universe(u):
    persist.save_celestials(CELESTIAL_PATH, u)
    persist.save_star_systems(STAR_SYSTEM_PATH, u)
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
    spacegame.start()
    game.start()
    save_universe(universe)
