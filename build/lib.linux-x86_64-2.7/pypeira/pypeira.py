import numpy as np
import warnings

import io.fits as fits2
import core.brightness
import core.time


class IRA(object):
    """
    The Image Reduction and Analysis (IRA) to which we will attach and pass information.
    """
    def __init__(self, header_kwds=None):
        self.header = dict()

        # Allows the user to set the headers they  want beforehand
        if header_kwds:
            self.header_kwds = header_kwds
        else:
            # Should have some default kwds
            self.header_kwds = list()

    def read_header(self, fname):
        # TODO: Fix the import io.fits problem!
        head = fits2.read_headers(fname)

        for h in self.header_kwds:
            self.header[h] = head[h]

        return self.header

    @staticmethod
    def read_folder(dir, type='bcd'):
        return fits2.read_folder(dir, type)

    @staticmethod
    def get_brightest(fits):
        return core.brightness.get_brightest(fits)

    @staticmethod
    def data_for_pixel(idx, fits):
        # Get data for a specific pixel
        # TODO: Should experiment with different ways of doing this
        pxl_data = [hdu[0].read()[idx[0], idx[1], idx[2]]
                    for hdu in fits]

        return core.time.to_timeseries(pxl_data)


