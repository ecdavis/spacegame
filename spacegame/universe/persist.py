from pantsmud.driver import storage
from spacegame.universe import star_system, universe


def load_universe(path):
    """
    Load the Universe data stored at the given path.
    """
    return storage.load_file(path, universe.Universe)


def save_universe(path, universe):
    """
    Save the Universe data to the given path.
    """
    return storage.save_object(path, universe)


def load_star_systems(path):
    """
    Load all StarSystem data stored under the given path. This function is not recursive.
    """
    return storage.load_files(path, "*.star_system.json", star_system.StarSystem)


def save_star_systems(path, universe):
    """
    Save all StarSystem data to files under the given path.
    """
    return storage.save_objects(path, ".star_system.json", universe.star_systems.values())
