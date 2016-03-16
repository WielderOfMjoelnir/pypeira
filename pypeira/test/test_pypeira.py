from __future__ import print_function

import pytest
import unittest

import fitsio
import numpy as np

from pypeira.pypeira import IRA
from pypeira.core.hdu import HDU


class HDUtest(unittest.TestCase):
    def setUp(self):
        self.ira = IRA()
        self.path = "data/test_imgs/ch2/bcd/SPITZER_I2_46467840_0000_0000_2_bcd.fits"
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
        self.path = "data/test_imgs/ch2/bcd/SPITZER_I2_46467840_0002_0000_2_bcd.fits"

    def test_reader(self):
        hdu = self.ira.read(self.path, data_type='bcd')
        hdu_no_dtype = self.ira.read(self.path)
        fits = fitsio.FITS(self.path)

        self.assertEqual(hdu.naxis, fits[0].read_header()['NAXIS'])
        self.assertEqual(hdu.img.any(), fits[0].read().any())
        self.assertEqual(hdu.img.any(), hdu_no_dtype.img.any())
        self.assertEqual(hdu.hdr['NAXIS'], hdu_no_dtype.hdr['NAXIS'])


class BrightnessTest(unittest.TestCase):
    def setUp(self):
        self.ira = IRA()
        self.path = "data/test_imgs/ch2/bcd/SPITZER_I2_46467840_0004_0000_2_bcd.fits"

    def test_get_max(self):
        hdu = self.ira.read(self.path)
        fits_img = fitsio.read(self.path)

        self.assertAlmostEqual(hdu.get_max()[1], np.nanmax(fits_img), 5)
