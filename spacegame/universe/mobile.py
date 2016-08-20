import uuid
from pantsmud.driver import auxiliary


class Mobile(object):
    """
    A representation of a mobile entity in the game universe.
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = ""
        self.universe = None
        self.brain_uuid = None
        self.celestial_uuid = None
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_MOBILE)

    def load_data(self, data):
        """
        Loads a dictionary containing saved Mobile data onto the object.

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
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing Mobile data ready to be serialized.
        """
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "celestial_uuid": str(self.celestial_uuid),
            "auxiliary": auxiliary.save_data(self.aux)
        }

    @property
    def world(self):
        """
        Get the Mobile's World, if it has one.
        """
        # TODO This is really hacky. Either rename Universe to World or reconsider PantsMUD's
        # TODO on brains having a world attached.
        return self.universe

    @property
    def brain(self):
        """
        Get the Mobile's Brain, if it has one.
        """
        if self.brain_uuid:
            return self.universe.brains[self.brain_uuid]
        else:
            return self.brain_uuid

    @brain.setter
    def brain(self, brain):
        """
        Set the Mobile's Brain.
        """
        if brain:
            self.brain_uuid = brain.uuid
        else:
            self.brain_uuid = None

    def attach_brain(self, brain):
        """
        Attach a Brain to this Mobile.
        """
        self.brain = brain
        brain.mobile = self

    def detach_brain(self):
        """
        Detach a Brain from this Mobile.
        """
        self.brain.mobile = None
        self.brain = None

    @property
    def celestial(self):
        """
        Get the Mobile's Celestial, if it has one.
        """
        if self.celestial_uuid:
            return self.universe.celestials[self.celestial_uuid]
        else:
            return self.celestial_uuid

    @celestial.setter
    def celestial(self, celestial):
        """
        Set the Mobile's Celestial.
        """
        if celestial:
            self.celestial_uuid = celestial.uuid
        else:
            self.celestial_uuid = None

    @property
    def star_system(self):
        """
        Get the Mobile's StarSystem.

        This is the StarSystem of the Mobile's Celestial, if it has one.
        """
        if self.celestial:
            return self.celestial.star_system
        else:
            return None

    def message(self, name, data=None):
        """
        Send a message to the Mobile's Brain, if it has one.
        """
        if self.brain:
            self.brain.message(name, data)
