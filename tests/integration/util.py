import json
import shutil
import socket
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

    def setUp(self):
        self.socket = socket.socket()
        self.socket.settimeout(1.0)
        self.socket.connect(('127.0.0.1', 4040))

    def tearDown(self):
        self.socket.close()

    def register_and_login(self, username):
        self.socket.send("register %s\r\n" % username)
        register_response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", register_response["message"])
        uuid = register_response["data"]["result"]["uuid"]
        self.socket.send("login %s\r\n" % uuid)
        login_response = json.loads(self.socket.recv(4096))
        self.assertEqual("command.success", login_response["message"])

    @classmethod
    def tearDownClass(cls):
        game.engine.stop()
        if cls._game_thread:
            cls._game_thread.join(1.0)
        if cls._data_dir:
            shutil.rmtree(cls._data_dir, ignore_errors=True)