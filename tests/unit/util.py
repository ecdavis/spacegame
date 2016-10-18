import unittest
import pantsmud.driver
import spacegame.core


class UnitTestCase(unittest.TestCase):
    def setUp(self):
        pantsmud.driver.init()
        spacegame.core.init()
