import uuid
from pantsmud.driver import hook, auxiliary


class SolarSystem(object):
    """
    A location within the game universe.
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.universe = None
        self.name = ""
        self._reset_interval = -1
        self.reset_timer = -1
        self.aux = auxiliary.new_data(auxiliary.AUX_TYPE_ZONE)

    def load_data(self, data):
        """
        Loads a dictionary containing saved SolarSystem data onto the object.

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
        self.reset_interval = data["reset_interval"]
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing SolarSystem data ready to be serialized.
        """
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "reset_interval": self.reset_interval,
            "auxiliary": auxiliary.save_data(self.aux)
        }

    @property
    def reset_interval(self):
        """
        Get the SolarSystem's reset interval in minutes.

        A negative interval indicates that the SolarSystem will never be reset.
        """
        return self._reset_interval

    @reset_interval.setter
    def reset_interval(self, interval):
        """
        Set the SolarSystem's reset interval in minutes.

        If the SolarSystem was previously set to never reset, it will now begin to reset as expected. If the current
        reset timer is greater than the new interval, it will be set to the new interval.
        """
        if self.reset_interval < 0 or self.reset_timer > interval:
            self.reset_timer = interval
        self._reset_interval = interval

    def pulse(self):
        """
        Pulse the SolarSystem, i.e. decrement its reset timer.

        When the reset timer reaches zero, the SolarSystem will be reset and the reset timer will be set back to the
        reset interval value.
        """
        self.reset_timer -= 1
        if self.reset_timer == 0:  #
            self.reset_timer = self.reset_interval
            hook.run(hook.HOOK_RESET_ZONE, self)

    def force_reset(self):
        """
        Force the SolarSystem to reset, regardless of the current reset timer value.
        """
        self.reset_timer = 1
        self.pulse()
