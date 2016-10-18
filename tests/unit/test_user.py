import mock
from spacegame.core.user import User
from tests.unit.util import UnitTestCase


class UserUnitTestCase(UnitTestCase):
    def test_brain_getter_and_setter(self):
        brain = mock.MagicMock()
        entity = User()
        self.assertIsNone(entity.brain)
        entity.brain = brain
        self.assertEqual(entity.brain_uuid, brain.uuid)
        entity.brain = None
        self.assertIsNone(entity.brain)
