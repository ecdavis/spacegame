import uuid
from pantsmud.driver import auxiliary
from spacegame.core import aux_types


class Entity(object):
    """
    A representation of an entity in the game universe.
    """
    def __init__(self, is_warp_beacon=False):
        self.uuid = uuid.uuid4()
        self.name = ""
        self.universe = None
        self.brain_uuid = None
        self.celestial_uuid = None
        self.position = (0, 0, 0)
        self.vector = (1.0, 0.0, 0.0)
        self.speed = 0
        self.is_warp_beacon = is_warp_beacon
        self.aux = auxiliary.new_data(aux_types.AUX_TYPE_ENTITY)

    def load_data(self, data):
        """
        Loads a dictionary containing saved Entity data onto the object.

        This method expects well-formed data. It will validate all fields and raise an exception if any of the data is
        invalid.

        Data layout:
            {
                "uuid": "<uuid>",
                "name": "<word>",
                "celestial_uuid": "<uuid>",
                "auxiliary": <dict>  # This will be passed to pantsmud.auxiliary.load_data
            }
        """
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.celestial_uuid = uuid.UUID(data["celestial_uuid"])  # TODO This isn't safe if the Celestial no longer exists.
        self.is_warp_beacon = data["is_warp_beacon"]
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing Entity data ready to be serialized.
        """
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "celestial_uuid": str(self.celestial_uuid),
            "is_warp_beacon": self.is_warp_beacon,
            "auxiliary": auxiliary.save_data(self.aux)
        }

    @property
    def environment(self):
        """
        Get the Entity's Environment, if it has one.
        """
        # TODO This is really hacky. Either rename Universe to World or reconsider PantsMUD's
        # TODO on brains having a world attached.
        return self.universe

    @property
    def brain(self):
        """
        Get the Entity's Brain, if it has one.
        """
        if self.brain_uuid:
            return self.universe.brains[self.brain_uuid]
        else:
            return self.brain_uuid

    @brain.setter
    def brain(self, brain):
        """
        Set the Entity's Brain.
        """
        if brain:
            self.brain_uuid = brain.uuid
        else:
            self.brain_uuid = None

    def attach_brain(self, brain):
        """
        Attach a Brain to this Entity.
        """
        self.brain = brain
        brain.mobile = self

    def detach_brain(self):
        """
        Detach a Brain from this Entity.
        """
        self.brain.mobile = None
        self.brain = None

    def message(self, name, data=None):
        """
        Send a message to the Entity's Brain, if it has one.
        """
        if self.brain:
            self.brain.message(name, data)

    @property
    def celestial(self):
        """
        Get the Entity's Celestial, if it has one.
        """
        if self.celestial_uuid:
            return self.universe.celestials[self.celestial_uuid]
        else:
            return self.celestial_uuid

    @celestial.setter
    def celestial(self, celestial):
        """
        Set the Entity's Celestial.
        """
        if celestial:
            self.celestial_uuid = celestial.uuid
        else:
            self.celestial_uuid = None

    @property
    def star_system(self):
        """
        Get the Entity's StarSystem.

        This is the StarSystem of the Entity's Celestial, if it has one.
        """
        if self.celestial:
            return self.celestial.star_system
        else:
            return None

    def velocity(self):
        """
        Get the Entity's current velocity.
        """
        return (round(self.vector[0]*self.speed, 3),  # X
                round(self.vector[1]*self.speed, 3),  # Y
                round(self.vector[2]*self.speed, 3))  # Z


def new_mobile():
    return Entity()
