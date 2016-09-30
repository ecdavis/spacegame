from spacegame.application import create_universe
from tests.unit.util import UnitTestCase


class ApplicationUnitTestCase(UnitTestCase):
    def test_create_universe(self):
        u = create_universe()
        self.assertEquals(2, len(u.star_systems))
        self.assertSetEqual({"The Solar System", "Alpha Centauri"}, set([s.name for s in u.star_systems.values()]))
        self.assertEquals(3, len(u.celestials))
        self.assertSetEqual({"Sol", "Earth", "Alpha Centauri"}, set([c.name for c in u.celestials.values()]))
