import uuid
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
        self.identities = {}
        self.mobiles = {}
        self.star_systems = {}
        self.celestials = {}
        self.core_star_system_uuids = set()
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_ENVIRONMENT)

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
        self.core_star_system_uuids = set((uuid.UUID(s) for s in data["core_star_system_uuids"]))
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing Universe data ready to be serialized.
        """
        return {
            "core_star_system_uuids": list((str(u) for u in self.core_star_system_uuids)),
            "auxiliary": auxiliary.save_data(self.aux)
        }

    @property
    def core_star_systems(self):
        """
        Get the Universe's core Star Systems.

        When adding an entity to the Universe, it should be placed in one of these star systems.
        """
        return set((self.star_systems[u] for u in self.core_star_system_uuids))

    def add_brain(self, brain):
        """
        Add a Brain to the Universe.
        """
        brain.environment = self
        self.brains[brain.uuid] = brain

    def remove_brain(self, brain):
        """
        Remove a Brain from the Universe.
        """
        del self.brains[brain.uuid]
        brain.environment = None

    def get_identity(self, identity_name):
        """
        Get an Identity by name.
        """
        for identity in self.identities.itervalues():
            if identity.name == identity_name:
                return identity
        return None

    def add_identity(self, identity):
        """
        Add an Identity to the Universe.
        """
        identity.universe = self
        self.identities[identity.uuid] = identity

    def remove_identity(self, identity):
        """
        Remove an Identity from the Universe.
        """
        del self.identities[identity.uuid]
        identity.universe = None

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

    def get_star_system(self, star_system_name):
        """
        Get a StarSystem by name.
        """
        for star_system in self.star_systems.itervalues():
            if star_system.name == star_system_name:
                return star_system
        return None

    def add_star_system(self, star_system):
        """
        Add a StarSystem to the Universe.
        """
        star_system.universe = self
        self.star_systems[star_system.uuid] = star_system

    def get_celestial(self, celestial_name, star_system=None):
        """
        Get a Celestial by name, optionally filter by StarSystem.
        """
        for celestial in self.celestials.itervalues():
            if star_system and celestial.star_system is not star_system:
                continue
            if celestial.name == celestial_name:
                return celestial
        return None

    def get_celestials(self, star_systems=None, uuids=None):
        """
        Get Celestials filtered by StarSystem, UUID, or both.
        """
        celestials = self.celestials.values()
        if star_systems is not None:
            celestials = filter(lambda c: c.star_system in star_systems, celestials)
        if uuids is not None:
            celestials = filter(lambda c: c.uuid in uuids, celestials)
        return celestials

    def add_celestial(self, celestial):
        """
        Add a Celestial to the Universe.
        """
        celestial.universe = self
        self.celestials[celestial.uuid] = celestial

    def pulse(self):
        """
        Pulse all StarSystems contained by the Universe.
        """
        for _, star_system in self.star_systems.iteritems():
            star_system.pulse()

    def force_reset(self):
        """
        Force all StarSystems contained by the Universe to reset.
        """
        for _, star_system in self.star_systems.iteritems():
            star_system.force_reset()
