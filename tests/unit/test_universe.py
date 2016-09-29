import mock
from spacegame.universe import universe
from tests.unit.util import UnitTestCase


class UniverseUnitTestCase(UnitTestCase):
    def test_get_entities_with_no_filters(self):
        u = universe.Universe()
        entity1 = mock.MagicMock()
        entity2 = mock.MagicMock()
        entity3 = mock.MagicMock()
        u.add_entity(entity1)
        u.add_entity(entity2)
        u.add_entity(entity3)
        entities = u.get_entities()
        self.assertSetEqual(
            {entity1, entity2, entity3},
            set(entities)
        )

    def test_get_entities_with_one_uuid(self):
        u = universe.Universe()
        uuid1 = mock.MagicMock()
        entity1 = mock.MagicMock()
        entity1.uuid = uuid1
        entity2 = mock.MagicMock()
        entity3 = mock.MagicMock()
        u.add_entity(entity1)
        u.add_entity(entity2)
        u.add_entity(entity3)
        entities = u.get_entities(uuids=[uuid1])
        self.assertSetEqual(
            {entity1},
            set(entities)
        )

    def test_get_entities_with_multiple_uuids(self):
        u = universe.Universe()
        uuid1 = mock.MagicMock()
        uuid2 = mock.MagicMock()
        entity1 = mock.MagicMock()
        entity1.uuid = uuid1
        entity2 = mock.MagicMock()
        entity2.uuid = uuid2
        entity3 = mock.MagicMock()
        u.add_entity(entity1)
        u.add_entity(entity2)
        u.add_entity(entity3)
        entities = u.get_entities(uuids=[uuid1, uuid2])
        self.assertSetEqual(
            {entity1, entity2},
            set(entities)
        )

    def test_get_star_systems_with_no_filters(self):
        u = universe.Universe()
        star_system1 = mock.MagicMock()
        star_system2 = mock.MagicMock()
        star_system3 = mock.MagicMock()
        u.add_star_system(star_system1)
        u.add_star_system(star_system2)
        u.add_star_system(star_system3)
        star_systems = u.get_star_systems()
        self.assertSetEqual(
            {star_system1, star_system2, star_system3},
            set(star_systems)
        )

    def test_get_star_systems_with_one_uuid(self):
        u = universe.Universe()
        uuid1 = mock.MagicMock()
        star_system1 = mock.MagicMock()
        star_system1.uuid = uuid1
        star_system2 = mock.MagicMock()
        star_system3 = mock.MagicMock()
        u.add_star_system(star_system1)
        u.add_star_system(star_system2)
        u.add_star_system(star_system3)
        star_systems = u.get_star_systems(uuids=[uuid1])
        self.assertSetEqual(
            {star_system1},
            set(star_systems)
        )

    def test_get_star_systems_with_multiple_uuids(self):
        u = universe.Universe()
        uuid1 = mock.MagicMock()
        uuid2 = mock.MagicMock()
        star_system1 = mock.MagicMock()
        star_system1.uuid = uuid1
        star_system2 = mock.MagicMock()
        star_system2.uuid = uuid2
        star_system3 = mock.MagicMock()
        u.add_star_system(star_system1)
        u.add_star_system(star_system2)
        u.add_star_system(star_system3)
        star_systems = u.get_star_systems(uuids=[uuid1, uuid2])
        self.assertSetEqual(
            {star_system1, star_system2},
            set(star_systems)
        )

    def test_pulse(self):
        u = universe.Universe()
        star_system1 = mock.MagicMock()
        star_system2 = mock.MagicMock()
        star_system3 = mock.MagicMock()
        u.add_star_system(star_system1)
        u.add_star_system(star_system2)
        u.add_star_system(star_system3)
        u.pulse()
        star_system1.pulse.assert_called()
        star_system2.pulse.assert_called()
        star_system3.pulse.assert_called()

    def test_force_reset(self):
        u = universe.Universe()
        star_system1 = mock.MagicMock()
        star_system2 = mock.MagicMock()
        star_system3 = mock.MagicMock()
        u.add_star_system(star_system1)
        u.add_star_system(star_system2)
        u.add_star_system(star_system3)
        u.force_reset()
        star_system1.force_reset.assert_called()
        star_system2.force_reset.assert_called()
        star_system3.force_reset.assert_called()
