from pantsmud.driver import auxiliary


class Universe(object):
    """
    A collection of all the objects in the game universe.

    The primary role of this class is to maintain a mapping of object UUIDs to object references. It is also
    responsible for maintaining a valid universe state at all times.
    """
    def __init__(self):
        self.sessions = set()
        self.brains = {}
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_WORLD)

    def load_data(self, data):
        """
        Loads a dictionary containing saved Universe data onto the object.

        This method expects well-formed data. It will validate all fields and raise an exception if any of the data is
        invalid.

        Data layout:
            {
                "auxiliary": <dict>  # This will be passed to pantsmud.auxiliary.load_data
            }
        """
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing Universe data ready to be serialized.
        """
        return {
            "auxiliary": auxiliary.save_data(self.aux)
        }

    def add_brain(self, brain):
        """
        Add a Brain to the Universe.
        """
        brain.world = self
        self.brains[brain.uuid] = brain

    def remove_brain(self, brain):
        """
        Remove a Brain from the Universe.
        """
        del self.brains[brain.uuid]
        brain.world = None

    def pulse(self):
        pass

    def force_reset(self):
        pass
