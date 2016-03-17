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
        """

        Parameters
        ----------
        path: str
            A string representing the path of the file to be read.
        inplace: bool, optional
            A boolean which tells the function whether or not to attach the header values onto the IRA instance.
            Possible use as is now could be if one simply wants to carry the header files through
            an entire data set instead of grabbing one for each image.

        Returns
        -------
        headers: FITSHDR object
            Can be accessed like a normal dictionary using indices.

        """
        # Stores the values of a set of header keywords on the instance. Doesn't have any uses as of yet.
        headers = _read(path, headers_only=True)

        if inplace:
            for kwd in self.header_kwds:
                self.header[kwd] = headers[0][kwd]

        return headers

    @staticmethod
    def read(path, ftype='fits', dtype=None, walk=True, headers_only=False, image_only=False, *args, **kwargs):
        """
        Proper description will be written when implementation is more complete.

        Reads files from path. Can handle path referencing to both dir and specific file.
        Will walk directory unless specified otherwise.

        Parameters
        ----------
        path: str
            A string representing the path containing the file (could be dir or the path directly to it).
            Notice that if 'walk' is True (which it is by default) and you provide a path to a dir, it
            will walk the directory, reading any files which satisfy the given criteria.
        ftype: str, optional
            A string representing the file type/extension you want to be read.
        dtype: str, optional
            The type of FITS file you want to read. If not None, will filter out all path names not
            ending in "dtype.FITS", i.e. if dtype = 'bcd'

                just_a_test_bcd.FITS

            is a valid, but

                just_a_test.FITS

            is not valid, in this case.
        walk: bool, optional
            Specifies whether or not to walk the directory. If 'path' is not a directory, 'walk'
            affects nothing. Default is True.
        headers_only: bool, optional
            Set to True if you only want to read the headers of the files. If True, the data
            return will only be the headers of the files read. Default is False.
        image_only: bool, optional
            Set to True if you only want to read the image data of the files. NOT IMPLEMENTED.
        *args: optional
            Contains all arguments that will be passed onto the actual reader function, where the
            reader function used for each file type/extension is as specified above.
        **kwargs: optional
            Same as for 'args'. Contains all keyword arguments that will be passed onto the actual
            reader function, where the reader used for each file type/extension is as specified in
            io.reader.

        Returns
        -------
        HDU object
            If 'path' pointed to is a
                single file - returned 'data' will be a single HDU object,
                directory - returned 'data' will be a list of HDU objects,
                no valid files - returned 'data' will be None. "valid" is as specified by the
                ftype argument, which defaults to 'fits'.

            Note for a single file the returned 'data' will be only one HDU object, NOT a list
            as if the path is a directory.

            See pypeira.core.hdu for implementation of HDU.

        FITSHDR object
            If 'headers_only' is not False it will return in the same manner as for the HDU case,
            but now the type of the files will be FITSHDR objects.
            Can be access like a regular dictionary using indices.

            See fitsio.fitslib.FITSHDR for implementation of FITSHDR.

        numpy.array
            If 'image_only' is not False it will return in the same manner as for the HDU case,
            but now the type of the tiles will be numpy.arrays.

        Raises
        ------
        OSError
            Raises OSError if the given path does not exist.
        """
        return _read(
            path,
            ftype=ftype,
            dtype=dtype,
            walk=walk,
            headers_only=headers_only,
            image_only=image_only,
            *args, **kwargs
        )

    @staticmethod
    def get_brightest(hdus):
        """ For docstring, see core.brightness.get_brightest. """
        return brightness.get_brightest(hdus)

    @staticmethod
    def pixel_data(idx, hdus, zipped=False):
        """ For docstring, see core.brightness.pixel_data. """
        # Get data for a specific pixel
        return brightness.pixel_data(idx, hdus, zipped)

    @staticmethod
    def plot_brightest(hdus):
        """ Simply calls the two methods above and plots the data returned. """
        idx, brightest = brightness.get_brightest(hdus)

        xs, ys = brightness.pixel_data(idx, hdus)

        plt.plot(xs, ys)
        plt.show()



