from pantsmud.driver import storage
from spacegame.universe import universe


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
