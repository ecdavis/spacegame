import mock
from pantsmud.driver import hook
from spacegame.core import hook_types
from spacegame.universe.star_system import StarSystem
from tests.unit.util import UnitTestCase


class StarSystemUnitTestCase(UnitTestCase):
    def setUp(self):
        UnitTestCase.setUp(self)
        self.hook_star_system_reset = mock.MagicMock()
        self.hook_star_system_reset.__name__ = 'hook_star_system_reset'
        hook.add(hook_types.STAR_SYSTEM_RESET, self.hook_star_system_reset)
        self.star_system = StarSystem()
        self.star_system.reset_interval = 10

    def test_change_reset_interval_from_negative_updates_reset_timer(self):
        self.star_system.reset_interval = -1
        self.star_system.reset_timer = -1
        self.star_system.reset_interval = 10
        self.assertEqual(self.star_system.reset_timer, 10)

    def test_change_reset_interval_with_reset_timer_below_one_updates_reset_timer(self):
        self.star_system.reset_timer = 0
        self.star_system.reset_interval = 5
        self.assertEqual(self.star_system.reset_timer, 5)

    def test_reduce_reset_interval_below_reset_timer_updates_reset_timer(self):
        self.star_system.reset_interval = 10
        self.star_system.reset_timer = 10
        self.star_system.reset_interval = 5
        self.assertEqual(self.star_system.reset_timer, 5)

    def test_increase_reset_interval_above_reset_timer_does_not_change_reset_timer(self):
        self.star_system.reset_timer = 10
        self.star_system.reset_interval = 20
        self.assertEqual(self.star_system.reset_timer, 10)

    def test_force_reset_resets_reset_timer(self):
        self.star_system.force_reset()
        self.assertEqual(self.star_system.reset_timer, self.star_system.reset_interval)

    def test_force_reset_calls_hook_star_system_reset(self):
        self.star_system.force_reset()
        self.hook_star_system_reset.assert_called()

    def test_force_reset_with_negative_reset_interval_calls_hook_star_system_reset(self):
        self.star_system.reset_interval = -1
        self.star_system.force_reset()
        self.hook_star_system_reset.assert_called()

    def test_pulse_with_reset_timer_above_one_does_not_call_hook_star_system_reset(self):
        self.star_system.reset_timer = 2
        self.star_system.pulse()
        self.hook_star_system_reset.assert_not_called()

    def test_pulse_with_reset_timer_at_one_calls_hook_star_system_reset(self):
        self.star_system.reset_timer = 1
        self.star_system.pulse()
        self.hook_star_system_reset.assert_called()

    def test_pulse_with_reset_timer_below_one_does_not_call_hook_star_system_reset(self):
        self.star_system.reset_timer = 0
        self.star_system.pulse()
        self.hook_star_system_reset.assert_not_called()

    def test_pulse_with_reset_timer_above_one_decrements_reset_timer(self):
        self.star_system.reset_timer = 2
        self.star_system.pulse()
        self.assertEqual(self.star_system.reset_timer, 1)

    def test_pulse_with_reset_timer_at_one_resets_reset_timer(self):
        self.star_system.reset_timer = 1
        self.star_system.pulse()
        self.assertEqual(self.star_system.reset_timer, self.star_system.reset_interval)

    def test_pulse_with_reset_timer_at_zero_decrements_reset_timer(self):
        self.star_system.reset_timer = 0
        self.star_system.pulse()
        self.assertEqual(self.star_system.reset_timer, -1)

    def test_pulse_with_reset_timer_below_zero_does_not_change_reset_timer(self):
        self.star_system.reset_timer = -1
        self.star_system.pulse()
        self.assertEqual(self.star_system.reset_timer, -1)
