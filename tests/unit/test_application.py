import os.path
import tempfile
from spacegame.application import check_and_create_directories, check_and_create_universe, create_universe,\
    load_universe
import spacegame.config
from tests.unit.util import UnitTestCase


class ApplicationUnitTestCase(UnitTestCase):
    def test_create_universe(self):
        u = create_universe()
        self.assertEquals(2, len(u.star_systems))
        self.assertSetEqual({"The Solar System", "Alpha Centauri"}, set([s.name for s in u.star_systems.values()]))
        self.assertEquals(3, len(u.celestials))
        self.assertSetEqual({"Sol", "Earth", "Alpha Centauri"}, set([c.name for c in u.celestials.values()]))

    def test_check_and_create_directories(self):
        test_data_dir = os.path.join(tempfile.mkdtemp(), 'data')
        os.makedirs(test_data_dir)
        spacegame.config.configure(test_data_dir)
        ensure_dirs_exist = [
            spacegame.config.path.universe_dir,
            spacegame.config.path.star_system_dir,
            spacegame.config.path.celestial_dir,
            spacegame.config.path.user_dir,
            spacegame.config.path.player_dir
        ]
        check_and_create_directories()
        for d in ensure_dirs_exist:
            self.assertTrue(os.path.exists(d))

    def test_check_and_create_universe(self):
        test_data_dir = os.path.join(tempfile.mkdtemp(), 'data')
        os.makedirs(test_data_dir)
        spacegame.config.configure(test_data_dir)
        check_and_create_directories()
        check_and_create_universe()
        load_universe()

