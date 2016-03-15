import pytest

import unittest

from pypeira.pypeira import IRA
from pypeira.core.time import fits_get_time


class MyTest(unittest.TestCase):
    def setUp(self):
        self.ira = IRA()
        self.path = "/home/tor/Dropbox/pypeira/pypeira/test/test_imgs/ch2"

    def test_get_brightest(self):
        data = self.ira.read(self.path, fits_type='bcd')
        idx, max_bright = self.ira.get_brightest(data)

        self.assertAlmostEqual(max_bright, 703.52435, places=5)
        self.assertEqual((45, 15, 15), idx)

    def test_fits_get_time(self):
        data = self.ira.read(self.path, fits_type='bcd')

        self.assertAlmostEqual(fits_get_time(data[0]), 56270.4887105, places=7)
