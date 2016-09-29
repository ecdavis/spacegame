import uuid
from pantsmud.driver import auxiliary
from spacegame.universe import mobile


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
        self.entities = {}
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

    def get_entity(self, entity_name):
        """
        Get a Entity by name.
        """
        for entity in self.entities.itervalues():
            if entity.name == entity_name:
                return entity
        return None

    def get_entities(self, star_systems=None, uuids=None, is_warp_beacon=None):
        """
        Get Entities filtered by StarSystem, UUID, flags, or a combination.
        """
        entities = self.entities.values()
        if star_systems is not None:
            entities = filter(lambda e: e.star_system in star_systems, entities)
        if uuids is not None:
            entities = filter(lambda e: e.uuid in uuids, entities)
        if is_warp_beacon is not None:
            entities = filter(lambda e: e.is_warp_beacon is is_warp_beacon, entities)
        return entities

    def add_entity(self, entity):
        """
        Add a Entity to the Universe.
        """
        entity.universe = self
        self.entities[entity.uuid] = entity

    def remove_entity(self, entity):
        """
        Remove a Entity from the Universe.
        """
        del self.entities[entity.uuid]
        entity.universe = None

    def get_mobiles(self):
        mobiles = self.entities.values()
        mobiles = filter(lambda e: isinstance(e, mobile.Mobile), mobiles)  # TODO Make it a flag
        return mobiles

    def get_star_system(self, star_system_name):
        """
        Get a StarSystem by name.
        """
        for star_system in self.star_systems.itervalues():
            if star_system.name == star_system_name:
                return star_system
        return None

    def get_star_systems(self, uuids=None):
        """
        Get StarSystems filtered by UUID.
        """
        star_systems = self.star_systems.values()
        if uuids is not None:
            star_systems = filter(lambda s: s.uuid in uuids, star_systems)
        return star_systems

    def add_star_system(self, star_system):
        """
        Add a StarSystem to the Universe.
        """
        star_system.universe = self
        self.star_systems[star_system.uuid] = star_system

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
