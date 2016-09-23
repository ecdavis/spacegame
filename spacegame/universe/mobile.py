from spacegame.universe import entity


class Mobile(entity.Entity):
    """
    A representation of a mobile entity in the game universe.
    """
    def __init__(self):
        entity.Entity.__init__(self)
        self.brain_uuid = None

    @property
    def environment(self):
        """
        Get the Mobile's Environment, if it has one.
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

    def message(self, name, data=None):
        """
        Send a message to the Mobile's Brain, if it has one.
        """
        if self.brain:
            self.brain.message(name, data)
