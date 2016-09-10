import os
import os.path
import uuid
from pantsmud.driver import storage, util
from spacegame import config
from spacegame.universe import mobile


class User(object):
    def __init__(self, user_uuid=None):
        if user_uuid:
            self.uuid = user_uuid
        else:
            self.uuid = uuid.uuid4()
        self.player_uuid = None

    def load_data(self, data):
        self.uuid = uuid.UUID(data["uuid"])
        self.player_uuid = uuid.UUID(data["player_uuid"]) if data["player_uuid"] else None

    def save_data(self):
        return {
            "uuid": str(self.uuid),
            "player_uuid": str(self.player_uuid) if self.player_uuid else ''
        }


def user_exists(user_uuid):
    return os.path.exists(config.USER_FILE_PATH % util.uuid_to_base32(user_uuid))


def load_user(user_uuid):
    return storage.load_file(config.USER_FILE_PATH % util.uuid_to_base32(user_uuid), User)


def save_user(user):
    storage.save_object(config.USER_FILE_PATH % util.uuid_to_base32(user.uuid), user)


def player_name_exists(player_name):
    for filename in os.listdir(config.PLAYER_DIR_PATH):
        p = storage.load_file(os.path.join(config.PLAYER_DIR_PATH, filename), mobile.Mobile)
        if p.name == player_name:
            return True
    return False


def player_exists(player_uuid):
    return os.path.exists(config.PLAYER_FILE_PATH % util.uuid_to_base32(player_uuid))


def load_player(player_uuid):
    return storage.load_file(config.PLAYER_FILE_PATH % util.uuid_to_base32(player_uuid), mobile.Mobile)


def save_player(player):
    storage.save_object(config.PLAYER_FILE_PATH % util.uuid_to_base32(player.uuid), player)
