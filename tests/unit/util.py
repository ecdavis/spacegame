import unittest
import pantsmud.driver
from pantsmud.driver import hook
import spacegame.core


class UnitTestCase(unittest.TestCase):
    def setUp(self):
        pantsmud.driver.init()
        spacegame.core.init(hook)
