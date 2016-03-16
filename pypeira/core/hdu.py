import numpy as np
import os.path

from pypeira.io.reader import _read_file
from pypeira.core.brightness import get_max


class HDU(object):
    """
    Will function as a standardized Header Data Unit for this package.

    The plan is that there will be subclasses of this, either specific to
    the source of the data or to the file the HDU is created from. This
    is something that would depend on how similar the header files of
    the different telescopes are, if FITS is the standard for ALL, etc.
    Would like to discuss this with mentor if possible.

    Original plan was to leverage the FITS objects from fitsio, which provides both
    performance (parser written in C and Fortran). As it turns out you run into
    quite a bit of problems when iterating over a large number of FITS files,
    as the number of simultaneously "opened" is quite limited.
    """
    def __init__(self, path, ftype=None, dtype=None, *args, **kwargs):

        self.path = path
        self.ftype = ftype
        self.dtype = dtype

        # Get the name of the file
        if os.path.isfile(path):
            self.filename = os.path.split(path)[1]
        else:
            raise RuntimeError("{0} is not a file.".format(path))

        self.naxis = None           # Number of axes
        self.ndims = None           # Array of dimensions for each axis in order with greatest numbered axis first
        self.timestamp = None       # The timestamp of the observation in BMJD
        self.frametime = None       # Integration time for whole array

        # Read the file
        data = self._read(*args, **kwargs)

        if data:
            self._header = data[0]
            self._image = data[1]

            self.init_from_hdr()
        else:
            self._header = None
            self._image = None

    def _read(self, *args, **kwargs):
        return _read_file(
            self.path,
            ftype=self.ftype,
            data_type=self.dtype,
            *args,
            **kwargs
        )

    def init_from_hdr(self):
        self.naxis = self.hdr.get('NAXIS')
        self.ndims = np.zeros(self.naxis)

        # Iterate through each NAXIS keyword of the header to get the dimensions
        for i in range(1, self.naxis + 1):
            self.ndims[self.naxis - i] = self.hdr.get('NAXIS{0}'.format(i))

        self.ndims = self.ndims.astype(np.dtype('int64'))

        self.timestamp = self.hdr.get('BMJD_OBS')
        self.frametime = self.hdr.get('FRAMTIME')

    @property
    def hdr(self):
        return self._header

    @property
    def img(self):
        return self._image

    @property
    def has_data(self):
        if np.any(self.img):
            return True
        else:
            return False

    def pixel_values(self, idx):
        idx_length = len(idx)

        if idx_length == self.naxis:
            # Strip away the index for the "data-layer", as this is what we wan
            # want to iterate over
            pix_idx = idx[1:]

        elif idx_length == self.naxis - 1:
            pix_idx = idx

        else:
            raise RuntimeError("Index needs to be equal to or one less than the number"
                               "of axes in the data-cube.")

        # Instantiate the array to hold the data for each pixel
        pix_val = np.zeros(self.ndims[0])

        # Iterate through the "data-layers", which is the 1st entry in ndims
        for i in np.arange(0, self.ndims[0]):
            pix_val[i] = self.img[i, pix_idx[0], pix_idx[1]]

        return pix_val

    def get_max(self):
        return get_max(self.img)
