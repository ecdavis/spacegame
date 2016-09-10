import logging
import os.path
import pants
from pantsmud.driver import game, net
import spacegame
from spacegame.core import user
from spacegame.universe import celestial, persist, star_system, universe


UNIVERSE_PATH = os.path.abspath("data/universe/")
UNIVERSE_FILE = os.path.join(UNIVERSE_PATH, "universe.json")
STAR_SYSTEM_PATH = os.path.join(UNIVERSE_PATH, "star_systems")
CELESTIAL_PATH = os.path.join(UNIVERSE_PATH, "celestials")


def check_and_create_directories():
    ensure_dirs_exist = [
        UNIVERSE_PATH,
        STAR_SYSTEM_PATH,
        CELESTIAL_PATH,
        user.USER_DIR_PATH,
        user.PLAYER_DIR_PATH
    ]
    for d in ensure_dirs_exist:
        directory = os.path.abspath(d)
        if not os.path.exists(directory):
            os.makedirs(directory)


def check_and_create_universe():
    if os.path.exists(UNIVERSE_FILE):
        logging.debug("Universe exists, skipping creation.")
        return
    u = universe.Universe()
    s = star_system.StarSystem()
    s.name = "The Solar System"
    u.add_star_system(s)
    c = celestial.Celestial()
    c.name = "Sol"
    u.add_celestial(c)
    c.star_system = s
    s.core_celestial_uuids.add(c.uuid)
    u.core_star_system_uuids.add(s.uuid)
    save_universe(u)


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


def main():
    check_and_create_directories()
    check_and_create_universe()
    spacegame.init()
    engine = pants.Engine.instance()
    universe = load_universe()
    game.init(engine, universe)
    net.init()
    spacegame.start()
    game.start()
    save_universe(universe)
