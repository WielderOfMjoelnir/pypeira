import pytest
import unittest

import fitsio

from pypeira.pypeira import IRA
from pypeira.core.time import fits_get_time
from pypeira.core.hdu import HDU


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


class HDUtest(unittest.TestCase):
    def setUp(self):
        self.ira = IRA()
        self.path = "/home/tor/Dropbox/pypeira/pypeira/test/test_imgs/ch2/bcd/SPITZER_I2_46467840_0000_0000_2_bcd.fits"
        self.hdu = HDU(self.path, ftype='fits', dtype='bcd')

    def test_header(self):
        myhdr = self.hdu.hdr
        hdr = fitsio.read_header(self.path)

        self.assertEqual(myhdr['NAXIS'], hdr['NAXIS'])
        self.assertEqual(myhdr['NAXIS3'], hdr['NAXIS3'])
        self.assertEqual(myhdr['BITPIX'], hdr['BITPIX'])

    def test_image(self):
        myimg = self.hdu.img
        img = fitsio.read(self.path)

        self.assertEqual(myimg.any(), img.any())


class ReaderTest(unittest.TestCase):
    def setUp(self):
        self.ira = IRA()
        self.path = "/home/tor/Dropbox/pypeira/pypeira/test/test_imgs/ch2/bcd/SPITZER_I2_46467840_0000_0000_2_bcd.fits"

    def test_reader(self):
        data = self.ira.read(self.path, data_type='bcd')