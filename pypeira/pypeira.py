import numpy as np

from io.common import read as _read
import core.brightness
import core.time


class IRA(object):
    """
    The Image Reduction and Analysis (IRA) to which we will attach and pass information.
    """
    def __init__(self, header_kwds=None):
        self.header = dict()

        # Allows the user to set the headers they want beforehand
        if header_kwds:
            self.header_kwds = header_kwds
        else:
            # Should have some default kwds
            self.header_kwds = list()

    @staticmethod
    def read_header(path):
        return _read(path, headers_only=True)

    @staticmethod
    def read(path):
        return _read(path)

    @staticmethod
    def read_dir(path):
        return _read(path)

    @staticmethod
    def get_brightest(fits):
        return core.brightness.get_brightest(fits)

    @staticmethod
    def data_for_pixel(idx, fits):
        # Get data for a specific pixel
        # TODO: Should experiment with different ways of doing this
        #pxl_data = [hdu[0].read()[idx[0]][idx[1]][idx[2]]
        #            for hdu in fits]
        pxl_data = []

        for hdu in fits:
            hd = hdu[0].read()

            print hdu[0].get_filename()

            print hd[idx[0]][idx[1]][idx[2]]

            pxl_data.append(hd[idx[0]][idx[1]][idx[2]])

        return core.time.to_timeseries(pxl_data)


