import numpy as np
import warnings

import io.fits as fits2
import core.brightness


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
        head = fits2.read_headers(fname)

        for h in self.header_kwds:
            self.header[h] = head[h]

        return self.header

    def read_folder(self, dir, type='bcd'):
        return fits2.read_folder(dir, type)

    @staticmethod
    def get_brightest(fits):
        """

        :param fits: FITS object,
        Containing Image_HDU's which can be accessed by indices.
        :return: (idx, max_brightness),
        Where idx are the indices of the brightest pixel, and max_brightness the maximum brightness of the pixel.
        """
        # Instatiate variables
        max_bright = 0
        idx = 0

        # Iterate through the hdus in the FITS object
        for hdu in fits:
            # Read image data from HDU
            pxls = hdu[0].read()

            curr_idx, curr_bright = core.brightness.get_max(pxls)

            if curr_bright > max_bright:
                max_bright = curr_bright

        return idx, max_bright
