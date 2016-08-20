from pantsmud.driver import storage
from spacegame.universe import solar_system, universe


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


def load_solar_systems(path):
    """
    Load all SolarSystem data stored under the given path. This function is not recursive.
    """
    return storage.load_files(path, "*.solar_system.json", solar_system.SolarSystem)


def save_solar_systems(path, universe):
    """
    Save all SolarSystem data to files under the given path.
    """
    return storage.save_objects(path, ".solar_system.json", universe.solar_systems.values())
