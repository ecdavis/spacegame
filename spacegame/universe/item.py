import uuid
from pantsmud.driver import auxiliary
from spacegame.core import aux_types


class Item(object):
    """
    A representation of an item in the game universe.
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = ""
        self.universe = None
        self.aux = auxiliary.new_data(aux_types.AUX_TYPE_ITEM)

    def load_data(self, data):
        """
        Loads a dictionary containing saved Item data onto the object.

        This method expects well-formed data. It will validate all fields and raise an exception if any of the data is
        invalid.

        Data layout:
            {
                "uuid": "<uuid>",
                "name": "<word>",
                "auxiliary": <dict>  # This will be passed to pantsmud.auxiliary.load_data
            }
        """
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.aux = auxiliary.load_data(self.aux, data["auxiliary"])

    def save_data(self):
        """
        Returns a dictionary containing Entity data ready to be serialized.
        """
        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "auxiliary": auxiliary.save_data(self.aux)
        }
