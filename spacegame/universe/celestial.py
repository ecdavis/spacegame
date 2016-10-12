import uuid
from pantsmud.driver import auxiliary
from spacegame.core import aux_types


class Celestial(object):
    """
    A location within a star system.
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.universe = None
        self.name = ""
        self.star_system_uuid = None
        self.aux = auxiliary.new_data(aux_types.AUX_TYPE_CELESTIAL)

    def load_data(self, data):
        """
        Loads a dictionary containing saved Celestial data onto the object.

        This method expects well-formed data. It will validate all fields and raise an exception if any of the data is
        invalid.

        Data layout:
            {
                "uuid": "<uuid>",
                "name": "<string>",
                "star_system_uuid": "<uuid>",
                "auxiliary": <dict>  # This will be passed to pantsmud.auxiliary.load_data
            }
        """
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.star_system_uuid = uuid.UUID(data["star_system_uuid"])
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing Celestial data ready to be serialized.
        """
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "star_system_uuid": str(self.star_system_uuid),
            "auxiliary": auxiliary.save_data(self.aux)
        }

    @property
    def star_system(self):
        """
        Get the Celestial's StarSystem, if it has one.
        """
        if self.star_system_uuid:
            return self.universe.star_systems[self.star_system_uuid]
        else:
            return self.star_system_uuid

    @star_system.setter
    def star_system(self, star_system):
        """
        Set the Celestial's StarSystem.
        """
        if star_system:
            self.star_system_uuid = star_system.uuid
        else:
            self.star_system_uuid = None
