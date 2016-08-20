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
        self.mobiles = {}
        self.solar_systems = {}
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
        brain.universe = None

    def get_mobile(self, mobile_name):
        """
        Get a Mobile by name.
        """
        for mobile in self.mobiles.itervalues():
            if mobile.name == mobile_name:
                return mobile
        return None

    def add_mobile(self, mobile):
        """
        Add a Mobile to the Universe.
        """
        mobile.universe = self
        self.mobiles[mobile.uuid] = mobile

    def remove_mobile(self, mobile):
        """
        Remove a Mobile from the Universe.
        """
        del self.mobiles[mobile.uuid]
        mobile.universe = None

    def get_solar_system(self, solar_system_name):
        """
        Get a SolarSystem by name.
        """
        for solar_system in self.solar_systems.itervalues():
            if solar_system.name == solar_system_name:
                return solar_system
        return None

    def add_solar_system(self, solar_system):
        """
        Add a SolarSystem to the Universe.
        """
        solar_system.universe = self
        self.solar_systems[solar_system.uuid] = solar_system

    def pulse(self):
        """
        Pulse all SolarSystems contained by the Universe.
        """
        for _, solar_system in self.solar_systems.iteritems():
            solar_system.pulse()

    def force_reset(self):
        """
        Force all SolarSystems contained by the Universe to reset.
        """
        for _, solar_system in self.solar_systems.iteritems():
            solar_system.force_reset()
