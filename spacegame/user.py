import os.path
import uuid
from pantsmud.driver import storage, util


USER_FILE_PATH = "data/users/%s.user.json"
PLAYER_FILE_PATH = "data/players/%s.mobile.json"


class User(object):
    def __init__(self, user_uuid=None):
        if user_uuid:
            self.uuid = user_uuid
        else:
            self.uuid = uuid.uuid4()

    def load_data(self, data):
        self.uuid = uuid.UUID(data["uuid"])

    def save_data(self):
        return {
            "uuid": str(self.uuid)
        }


def user_exists(user_uuid):
    return os.path.exists(USER_FILE_PATH % util.uuid_to_base32(user_uuid))


def load_user(user_uuid):
    return storage.load_file(USER_FILE_PATH % util.uuid_to_base32(user_uuid), User)


def save_user(user):
    storage.save_object(USER_FILE_PATH % util.uuid_to_base32(user.uuid), user)
