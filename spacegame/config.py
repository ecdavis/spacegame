import os.path


UNIVERSE_PATH = os.path.abspath("data/universe/")
UNIVERSE_FILE = os.path.join(UNIVERSE_PATH, "universe.json")
STAR_SYSTEM_PATH = os.path.join(UNIVERSE_PATH, "star_systems")
CELESTIAL_PATH = os.path.join(UNIVERSE_PATH, "celestials")
USER_DIR_PATH = "data/users/"
USER_FILE_PATH = USER_DIR_PATH + "%s.user.json"
PLAYER_DIR_PATH = "data/players/"
PLAYER_FILE_PATH = PLAYER_DIR_PATH + "%s.mobile.json"
