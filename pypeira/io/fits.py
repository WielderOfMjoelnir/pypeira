import os
import fitsio


def read_headers(fname, ext=0):
    # Reads the headers from the FITS file

    header = fitsio.read_header(fname, ext=ext)

    return header


def read_image():
    # Reads the image data which are numpy arrays of ndims (specified in the header files)

    pass


def read_hdu(fname, ext=0):
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

    :param fname:
    :param ext:
    :return:
    """

    fits = fitsio.FITS(fname)

    return fits


def read_folder(dir, type='bcd'):
    # Reads an entire folder of specificed file types
    hdus = [fitsio.FITS(os.path.join(dir, f)) for f in os.listdir(dir)
            if f.split('_')[-1][:-5] == type and f[-5:] == '.fits']

    return hdus
