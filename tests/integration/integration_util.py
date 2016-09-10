import threading
import time
import unittest
from pantsmud.driver import game
from spacegame.application import main


class IntegrationTestCase(unittest.TestCase):
    _game_thread = None

    @classmethod
    def setUpClass(cls):
        cls._game_thread = threading.Thread(target=main, args=("data",))
        cls._game_thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        game.engine.stop()
        if cls._game_thread:
            cls._game_thread.join(1.0)
