import mock
from spacegame.universe.entity import Entity
from tests.unit.util import UnitTestCase


class EntityUnitTestCase(UnitTestCase):
    def test_celestial_getter_and_setter(self):
        celestial = mock.MagicMock()
        entity = Entity()
        self.assertIsNone(entity.celestial)
        entity.celestial = celestial
        self.assertEqual(entity.celestial_uuid, celestial.uuid)
        entity.celestial = None
        self.assertIsNone(entity.star_system)

    def test_star_system_getter(self):
        entity = Entity()
        self.assertIsNone(entity.star_system)
