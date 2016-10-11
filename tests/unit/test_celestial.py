import mock
from spacegame.universe.celestial import Celestial
from tests.unit.util import UnitTestCase


class CelestialUnitTestCase(UnitTestCase):
    def test_star_system_getter_and_setter(self):
        star_system = mock.MagicMock()
        celestial = Celestial()
        self.assertIsNone(celestial.star_system)
        celestial.star_system = star_system
        self.assertEqual(celestial.star_system_uuid, star_system.uuid)
        celestial.star_system = None
        self.assertIsNone(celestial.star_system)
