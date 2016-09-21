import os
import os.path
import uuid
from pantsmud.util import convert, storage
from spacegame import config
from spacegame.universe import mobile


class User(object):
    def __init__(self, user_uuid=None):
        if user_uuid:
            self.uuid = user_uuid
        else:
            self.uuid = uuid.uuid4()
        self.name = ""
        self.universe = None
        self.brain_uuid = None
        self.player_uuid = None

    def load_data(self, data):
        self.uuid = uuid.UUID(data["uuid"])
        self.name = data["name"]
        self.player_uuid = uuid.UUID(data["player_uuid"]) if data["player_uuid"] else None

    def save_data(self):
        return {
            "uuid": str(self.uuid),
            "name": str(self.name),
            "player_uuid": str(self.player_uuid) if self.player_uuid else ''
        }

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


def user_exists(user_uuid):
    return os.path.exists(config.path.user_file_pattern % convert.uuid_to_base32(user_uuid))


def load_user(user_uuid):
    return storage.load_file(config.path.user_file_pattern % convert.uuid_to_base32(user_uuid), User)


def save_user(user):
    storage.save_object(config.path.user_file_pattern % convert.uuid_to_base32(user.uuid), user)


def player_name_exists(player_name):
    for filename in os.listdir(config.path.player_dir):
        p = storage.load_file(os.path.join(config.path.player_dir, filename), mobile.Mobile)
        if p.name == player_name:
            return True
    return False


def player_exists(player_uuid):
    return os.path.exists(config.path.player_file_pattern % convert.uuid_to_base32(player_uuid))


def load_player(player_uuid):
    return storage.load_file(config.path.player_file_pattern % convert.uuid_to_base32(player_uuid), mobile.Mobile)


def save_player(player):
    storage.save_object(config.path.player_file_pattern % convert.uuid_to_base32(player.uuid), player)
