import unittest
import pantsmud.driver


class UnitTestCase(unittest.TestCase):
    def setUp(self):
        pantsmud.driver.init()
