import mock
from spacegame.universe.mobile import Mobile
from tests.unit.util import UnitTestCase


class MobileUnitTestCase(UnitTestCase):
    def test_brain_getter_and_setter(self):
        brain = mock.MagicMock()
        mobile = Mobile()
        self.assertIsNone(mobile.brain)
        mobile.brain = brain
        self.assertEqual(mobile.brain_uuid, brain.uuid)
        mobile.brain = None
        self.assertIsNone(mobile.brain)

    def test_environment_getter(self):
        mobile = Mobile()
        self.assertEqual(mobile.environment, mobile.universe)
