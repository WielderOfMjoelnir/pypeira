import numpy as np
import warnings

import io.fits as fits


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
        head = fits.read_headers(fname)

        for h in self.header_kwds:
            self.header[h] = head[h]

        return self.header

    def read_folder(self, dir, type='bcd'):
        return fits.read_folder(dir, type)
