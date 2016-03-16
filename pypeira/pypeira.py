try:
    from pypeira.io.common import read as _read
    import pypeira.core.brightness as brightness
except ImportError:
    from io.common import read as _read
    import core.brightness as brightness

import matplotlib.pyplot as plt

from matplotlib import style
style.use('ggplot')


class IRA(object):
    """
    The Image Reduction and Analysis (IRA) to which we will attach and pass information.
    This class will be used as a config from where one can call functions, and simply
    pass default values set on the instance of the class by the user. Attributes such as:

    * header keywords
    * time steps
    * centroid methods and parameters
    * time format
    * etc.

    """
    ### IMPORTANT ###
    # This class will eventually be populated with a ton of attributes corresponding
    # to certain configuration parameters for which headers to read, which method to
    # use for finding centroids, etc.
    # The plan is to use this object as a config, which you can then call functions
    # from, and the functions will use the attributes of this object as arguments.
    # This way you won't have to retype the parameters, etc. every time. That also
    # means that the static methods below will not stay static for long, but it's
    # simply temporary as to avoid IDE suggestions about making them static.

    ### UP FOR DISCUSSION ###
    # I was considering simply using this object's self as an argument for each
    # function, and simply pass the entire "config" around instead of having
    # arguments for each. After some thought I didn't quite fancy this idea,
    # not only for the performance hit as more and more information is acquired,
    # but also because it would disallow use of the methods outside of this class.
    # For the sake of modularity, I think sacrificing some readability that goes
    # with all the arguments for the methods is worth it.

    _header_kwds_defaults = [
        'BITPIX',               # Four-byte single precision floating point
        'NAXIS',                # Nr. of axes
        'NAXIS1',               # Nr. of rows, Spitzer = 32
        'NAXIS2',               # Nr. of columns, Spitzer = 32
        'NAXIS3',               # Nr. of images in a set or "high" of data-cube, Spitzer = 64
        'CHNLNUM',              # Channel number used
        'FRAMTIME',             # Time spent integrating whole array
        'EXPTIME',              # Effective integration time per pixel
        'EXPTYE',               # Exposure type
        'BMJD_OBS',             # Solar System Barycenter Mod. Julian Date
        'FLUXCONV',             # Flux conversion factor (MJy/sr per DN/sec)
        'RONOISE',              # Readout Noise from array
        'BUNIT',                # Units of image data (default: MJy/sr)
        'GAIN',                 # e/DN conversion
        'BADPIX',               # T/F representing if there are bad pixels or not
        'ZEROPIX'               # If BADPIX is T, then this will give number of bad pixels
    ]

    def __init__(self, header=None, header_kwds=None):
        # See above comment for why this is almost empty. Will be populated in the future.
        self.header = header

        if header_kwds is not None:
            self.header_kwds = header_kwds
        else:
            self.header_kwds = self._header_kwds_defaults

    def read_header(self, path, inplace=False):
        # Stores the values of a set of header keywords on the instance. Doesn't have any uses as of yet.
        headers = _read(path, headers_only=True)

        if inplace:
            for kwd in self.header_kwds:
                self.header[kwd] = headers[0][kwd]

        return headers

    @staticmethod
    def read(path, ftype='fits', fits_type=None, walk=True, headers_only=False, image_only=False, *args, **kwargs):
        return _read(
            path,
            ftype=ftype,
            fits_type=fits_type,
            walk=walk,
            headers_only=headers_only,
            image_only=image_only,
            *args, **kwargs
        )

    @staticmethod
    def get_brightest(hdus):
        return brightness.get_brightest(hdus)

    @staticmethod
    def pixel_data(idx, hdus, zipped=False):
        # Get data for a specific pixel
        return brightness.pixel_data(idx, hdus, zipped)

    @staticmethod
    def plot_brightest(hdus):
        idx, brightest = brightness.get_brightest(hdus)

        xs, ys = brightness.pixel_data(idx, hdus)

        plt.scatter(xs, ys)



