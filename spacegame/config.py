import os.path


class _PathConfig(object):
    def __init__(self, data_dir):
        if data_dir is not None:
            data_dir = os.path.abspath(data_dir)
            if not os.path.exists(data_dir):
                raise Exception("Invalid configuration.")  # TODO Proper exception
        self._data_dir = data_dir

    @property
    def data_dir(self):
        if self._data_dir is None:
            raise Exception("Invalid configuration.")  # TODO Proper exception
        return self._data_dir

    @property
    def universe_dir(self):
        return os.path.join(self.data_dir, "universe")

    @property
    def universe_file(self):
        return os.path.join(self.universe_dir, "universe.json")

    @property
    def star_system_dir(self):
        return os.path.join(self.universe_dir, "star_systems")

    @property
    def celestial_dir(self):
        return os.path.join(self.universe_dir, "celestials")

    @property
    def user_dir(self):
        return os.path.join(self.data_dir, "users")

    @property
    def user_file_pattern(self):
        return os.path.join(self.user_dir, "%s.user.json")

    @property
    def player_dir(self):
        return os.path.join(self.data_dir, "players")

    @property
    def player_file_pattern(self):
        return os.path.join(self.player_dir, "%s.mobile.json")


path = _PathConfig(None)


def configure(data_dir):
    global path
    path = _PathConfig(data_dir)
