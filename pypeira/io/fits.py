import os
import fitsio

"""
A FITS file is comprised of segments called Header/Data Units (HDUs), where the first
HDU is called the 'Primary HDU', or 'Primary Array'. The primary data array can contain
a 1-999 dimensional array of 1, 2 or 4 byte integers or 4 or 8 byte floating point numbers
using IEEE representation. A typical primary array could contain a 1-D spectrum, a 2-D image,
or a 3-D data cube (this is what's coming from the SSC).

Any number of additional HDUs may follow the primary array. These additional HDUs are
referred to as FITS 'extensions'. Three types of standard extensions are currently defined:

* Image Extensions
    * Contain a 0-999 dimensional array of pixels, similar to primary array
    * Header begins with XTENSION = 'IMAGE'
* ASCII Tables Extensions
    * Store tabular information with all numberic information stored in ASCII formats
    While ASCII tables are generellay less efficient than binary tables, they can be
    made relatively human readable and can store numeric information with essentially
    arbitrary size and accuracy (e.g., 16 byte reals).
    * Header begins with XTENSION = 'TABLE'
* Binary Table Extensions
    * Store tabular information in a binary represetation. Each cell in the table
    can be an array but the dimensionality of the array must be constant within a
    column. The strict standard supports only one-dimensional arrays, but a convention
    to support multi-dimensional arrays are widely accepted.
    * Header begins with XTENSION = 'BINTABLE'

In addition to the structures above, there is one other type of FITS HDU called
"Random Groups" that is almost exclusively used for applications in radio interferometry.
The random groups format should not be used for other types of applications.
.. [REF] fits.gsfc.nasa.gov/fits_primer.html
"""


def read_headers(fname, *args, **kwargs):
    # Reads the headers from the FITS file

    header = fitsio.read_header(fname, **kwargs)

    return header


def read_image(fname, *args, **kwargs):
    # Reads the image data from the FITS file

    data = fitsio.read(fname, *args, **kwargs)

    return data


def read_fits(fname, headers_only=False, image_only=False, *args, **kwargs):
    """


    Parameters
    ----------
    fname: str
        Path to the FITS file you want to read
    headers_only: bool, optional
        Set to True if you only want to read the headers of the file. If True, the data
        return will only be the headers of the files read. Default is False.
    image_only: bool, optional
        Set to True if you only want to read the image data of the file. If True, the data
        return will be a numpy array corresponding to the image data of the files read.
        Default is False.
    *args: optional
        Contains all arguments that will be passed onto the fitsio reader. This reader will
        be fitsio.read_headers() or fitsio.FITS() depending on if 'headers_only' is True or False.
    **kwargs: optional
        Contains all keyword arguments that will be passed to the fitsio reader.

    Returns
    -------
    FITS object
        If none of the "only"-keywords are not False, then a FITS object will be returned.

        See fitsio.fitslib.FITS for implementation of FITS.

    FITSHDR object
        If 'headers_only' is not False it will return in the same manner as for the FITS object,
        but now the type of the files will be FITSHDR objects.

        See fitsio.fitslib.FITSHDR for implementation of FITSHDR.

    numpy.array
        If 'image_only' is not False it will return in the same manner as for the FITS object,
        but now the type of the tiles will be numpy.arrays.
    """
    if headers_only:
        fits = read_headers(fname, *args, **kwargs)
    elif image_only:
        fits = read_image(fname, *args, **kwargs)
    else:
        fits = fitsio.FITS(fname, *args, **kwargs)

    return fits

