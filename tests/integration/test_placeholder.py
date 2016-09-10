import socket
from tests.integration.util import IntegrationTestCase


class PlaceholderIntegrationTestCase(IntegrationTestCase):
    def test_placeholder(self):
        sock = socket.socket()
        sock.settimeout(1.0)
        sock.connect(('127.0.0.1', 4040))
        sock.close()
        self.assertTrue(True)
