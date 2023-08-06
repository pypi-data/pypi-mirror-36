import io
import unittest

import six
import yaml
from path import Path

from yaml_tags import tag_registry


class RandomTestCase(unittest.TestCase):
    cwd = Path(__file__).parent.abspath()

    def setUp(self):
        super(RandomTestCase, self).setUp()

        tag_registry.require('random_int', 'random_float', 'random_str')

    def test_int_on_data(self):
        with io.open(self.cwd / 'data/random/int/a.yml') as fh:
            data = yaml.load(fh)

        self.assertIsNotNone(data)
        rand_number = data['b']

        self.assertIsNotNone(rand_number)
        six.assertRegex(self, str(rand_number), r'[\d]+')

    def test_float_on_data(self):
        with io.open(self.cwd / 'data/random/float/a.yml') as fh:
            data = yaml.load(fh)

        self.assertIsNotNone(data)
        rand_number = data['b']

        self.assertIsNotNone(rand_number)
        six.assertRegex(self, str(rand_number), r'[\d]+.[\d]+')

    def test_str_on_data(self):
        with io.open(self.cwd / 'data/random/str/a.yml') as fh:
            data = yaml.load(fh)

        self.assertIsNotNone(data)
        rand_str_10_mixed = data['b']
        self.assertIsNotNone(rand_str_10_mixed)
        six.assertRegex(self, rand_str_10_mixed, r'[a-zA-Z0-9]{10}')

        rand_str_100_upper = data['c']
        self.assertIsNotNone(rand_str_100_upper)
        six.assertRegex(self, rand_str_100_upper, r'[A-Z0-9]{100}')

        rand_str_50_lower = data['d']
        self.assertIsNotNone(rand_str_50_lower)
        six.assertRegex(self, rand_str_50_lower, r'[a-z0-9]{50}')


if __name__ == '__main__':
    unittest.main()
