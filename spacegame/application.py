import logging
import os.path
import pants
import pantsmud.driver
import pantsmud.game
import pantsmud.net
import spacegame
from spacegame import config
from spacegame.universe import celestial, persist, star_system, universe


def check_and_create_directories():
    ensure_dirs_exist = [
        config.path.universe_dir,
        config.path.star_system_dir,
        config.path.celestial_dir,
        config.path.user_dir,
        config.path.player_dir
    ]
    for d in ensure_dirs_exist:
        directory = os.path.abspath(d)
        if not os.path.exists(directory):
            os.makedirs(directory)


def check_and_create_universe():
    if os.path.exists(config.path.universe_file):
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
    u = persist.load_universe(config.path.universe_file)
    for s in persist.load_star_systems(config.path.star_system_dir):
        u.add_star_system(s)
    for c in persist.load_celestials(config.path.celestial_dir):
        u.add_celestial(c)
    return u


def save_universe(u):
    persist.save_celestials(config.path.celestial_dir, u)
    persist.save_star_systems(config.path.star_system_dir, u)
    persist.save_universe(config.path.universe_file, u)


def main(data_dir):

    # Ensure data exists/is created
    config.configure(data_dir)
    check_and_create_directories()
    check_and_create_universe()
    universe = load_universe()

    # Create the engine
    engine = pants.Engine.instance()

    # Load up our code -- driver before game
    pantsmud.driver.init()
    pantsmud.game.init(engine, universe)
    spacegame.init()

    # Create the server
    server = pantsmud.net.GameServer(engine=engine)
    server.listen(4040)

    # Start the game
    spacegame.start()
    pantsmud.game.start()

    # Save the universe!
    save_universe(universe)
