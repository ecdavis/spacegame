import json
import os.path
import random
import shutil
import socket
import tempfile
import threading
import time
import unittest
import pantsmud.game
from spacegame.application import main


def _random_port():
    return random.randint(10000, 50000)


class StatefulIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self._data_dir = os.path.join(tempfile.mkdtemp(), 'data')
        shutil.copytree(os.path.join(os.path.dirname(__file__), 'data'), self._data_dir)
        print "integration test data dir:", self._data_dir
        self._port = _random_port()
        print "integration test port", self._port
        self._game_thread = threading.Thread(target=main, args=(self._data_dir, self._port))
        self._game_thread.start()
        time.sleep(1)  # TODO Figure out a way to remove this.
        self.clients = []

    def tearDown(self):
        for client in self.clients:
            client.close()
        pantsmud.game.engine.stop()
        if self._game_thread:
            self._game_thread.join(1.0)
        if self._data_dir:
            shutil.rmtree(self._data_dir, ignore_errors=True)

    def get_client(self):
        client = socket.socket()
        client.settimeout(1.0)
        client.connect(('127.0.0.1', self._port))
        self.clients.append(client)
        return client

    def register_and_login(self, client, username):
        client.send("register %s\r\n" % username)
        register_response = json.loads(client.recv(4096))
        self.assertEqual("command.success", register_response["message"])
        uuid = register_response["data"]["result"]["uuid"]
        client.send("login %s\r\n" % uuid)
        login_response = json.loads(client.recv(4096))
        self.assertEqual("command.success", login_response["message"])


class IntegrationTestCase(unittest.TestCase):
    _game_thread = None
    _data_dir = None

    @classmethod
    def setUpClass(cls):
        cls._data_dir = os.path.join(tempfile.mkdtemp(), 'data')
        shutil.copytree(os.path.join(os.path.dirname(__file__), 'data'), cls._data_dir)
        print "integration test data dir:", cls._data_dir
        cls._port = _random_port()
        print "integration test port", cls._port
        cls._game_thread = threading.Thread(target=main, args=(cls._data_dir, cls._port))
        cls._game_thread.start()
        time.sleep(1)  # TODO Figure out a way to remove this.

    def setUp(self):
        self.clients = []

    def tearDown(self):
        for client in self.clients:
            client.close()

    def get_client(self):
        client = socket.socket()
        client.settimeout(1.0)
        client.connect(('127.0.0.1', self._port))
        self.clients.append(client)
        return client

    def register_and_login(self, client, username):
        client.send("register %s\r\n" % username)
        register_response = json.loads(client.recv(4096))
        self.assertEqual("command.success", register_response["message"])
        uuid = register_response["data"]["result"]["uuid"]
        client.send("login %s\r\n" % uuid)
        login_response = json.loads(client.recv(4096))
        self.assertEqual("command.success", login_response["message"])

    def validate_num_parameters(self, client, command, num_parameters=0):
        # TODO Validate parameter content as well as quantity
        for i in range(max(num_parameters*2, 10)):
            if i == num_parameters:
                continue
            client.send("%s %s\r\n" % (command, ' '.join(map(str, range(i)))))
            response = json.loads(client.recv(4096))
            self.assertEqual("command.error", response["message"], "%s with %d parameters" % (command, i))
            self.assertEqual(command, response["data"]["command"])
            # TODO Validate error message

    @classmethod
    def tearDownClass(cls):
        pantsmud.game.engine.stop()
        if cls._game_thread:
            cls._game_thread.join(1.0)
        if cls._data_dir:
            shutil.rmtree(cls._data_dir, ignore_errors=True)
