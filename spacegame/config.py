import os.path


class _PathConfig(object):
    def __init__(self, data_path):
        self.data_path = os.path.abspath(data_path)

    @property
    def data_dir(self):
        return self.data_path

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


path = _PathConfig("data")
