import uuid
from pantsmud.driver import auxiliary, hook
from spacegame.core import aux_types, hook_types


class StarSystem(object):
    """
    A location within the game universe.
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.universe = None
        self.name = ""
        self.core_celestial_uuids = set()
        self._reset_interval = -1
        self.reset_timer = -1
        self.aux = auxiliary.new_data(aux_types.AUX_TYPE_STAR_SYSTEM)

    def load_data(self, data):
        """
        Loads a dictionary containing saved StarSystem data onto the object.

        This method expects well-formed data. It will validate all fields and raise an exception if any of the data is
        invalid.

        Data layout:
            {
                "uuid": "<uuid>",
                "reset_interval": <int>,
                "auxiliary": <dict>  # This will be passed to pantsmud.auxiliary.load_data
            }
        """
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.core_celestial_uuids = set((uuid.UUID(s) for s in data["core_celestial_uuids"]))
        self.reset_interval = data["reset_interval"]
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing StarSystem data ready to be serialized.
        """
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "core_celestial_uuids": list((str(u) for u in self.core_celestial_uuids)),
            "reset_interval": self.reset_interval,
            "auxiliary": auxiliary.save_data(self.aux)
        }

    @property
    def core_celestials(self):
        """
        Get the StarSystem's core Celestials.

        When adding an entity to the StarSystem, it should be placed in one of these Celestials.
        """
        return set((self.universe.celestials[u] for u in self.core_celestial_uuids))

    @property
    def reset_interval(self):
        """
        Get the StarSystem's reset interval in minutes.

        A negative interval indicates that the StarSystem will never be reset.
        """
        return self._reset_interval

    @reset_interval.setter
    def reset_interval(self, interval):
        """
        Set the StarSystem's reset interval in minutes.

        If the StarSystem was previously set to never reset, it will now begin to reset as expected. If the current
        reset timer is greater than the new interval, it will be set to the new interval.
        """
        if self.reset_interval < 0 or self.reset_timer > interval or self.reset_timer < 1:
            self.reset_timer = interval
        self._reset_interval = interval

    def get_celestials(self, uuids=None):
        """
        Get Celestials in this StarSystem, optionally filtered by UUID.
        """
        return self.universe.get_celestials(
            star_systems=[self],
            uuids=uuids
        )

    def get_entities(self, uuids=None, is_warp_beacon=None):
        """
        Get Entities in this StarSystem, optionally filtered by UUID, flags, or a combination.
        """
        return self.universe.get_entities(
            star_systems=[self],
            uuids=uuids,
            is_warp_beacon=is_warp_beacon
        )

    def pulse(self):
        """
        Pulse the StarSystem, i.e. decrement its reset timer.

        When the reset timer reaches zero, the StarSystem will be reset and the reset timer will be set back to the
        reset interval value.
        """
        if self.reset_timer > -1:
            self.reset_timer -= 1
        if self.reset_timer == 0:
            self.reset_timer = self.reset_interval
            hook.run(hook_types.STAR_SYSTEM_RESET, self)

    def force_reset(self):
        """
        Force the StarSystem to reset, regardless of the current reset timer value.
        """
        self.reset_timer = 1
        self.pulse()
