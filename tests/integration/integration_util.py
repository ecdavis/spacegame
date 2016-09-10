import shutil
import tempfile
import threading
import time
import unittest
from pantsmud.driver import game
from spacegame.application import main


class IntegrationTestCase(unittest.TestCase):
    _game_thread = None
    _data_dir = None

    @classmethod
    def setUpClass(cls):
        cls._data_dir = tempfile.mkdtemp()
        print "integration test data dir:", cls._data_dir
        cls._game_thread = threading.Thread(target=main, args=(cls._data_dir,))
        cls._game_thread.start()
        time.sleep(1)  # TODO Figure out a way to remove this.

    @classmethod
    def tearDownClass(cls):
        game.engine.stop()
        if cls._game_thread:
            cls._game_thread.join(1.0)
        if cls._data_dir:
            shutil.rmtree(cls._data_dir, ignore_errors=True)
