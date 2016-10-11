from spacegame import config
from tests.unit.util import UnitTestCase


class PathConfigUnitTestCase(UnitTestCase):
    def test_data_dir_is_invalid_raises_Exception(self):
        self.assertRaises(Exception, config._PathConfig, '/this/is/not/a/valid/path')

    def test_data_dir_is_None_raises_Exception(self):
        path_config = config._PathConfig(None)
        self.assertRaises(Exception, getattr, path_config, 'data_dir')
