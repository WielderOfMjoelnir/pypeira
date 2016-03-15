import numpy as np


def get_max(data, max_val=0, idx=0):
    """

    Parameters
    ----------
    data: numpy.array
        A multidimensional numpy array with entries to be compared.
    max_val:
        The "starting" maximum value. Usually used if one wants to
        compare several 'data's, simply to carry over the max value
        of the previous comparisons.
    idx: (int, ... ), float
        See get_brightest() for more information.

    Returns
    -------
    idx, max_val: (int, ... ), float
        idx is the index of the maximum value, represented in a n-tuple of
        the form (dim1, dim2, ... ).
        max_val is a float representing the maximum value in the array.
    """
    # Use np.ndenumerate(data) to iterate through (idx, val)-pairs
    # i.e. (i, j, k), data[i][j][k] pairs
    for i, j in np.ndenumerate(data):
        if not np.isnan(j) and j > max_val:
            idx = i
            max_val = j

    return idx, max_val


def get_brightest(hdus):
    """

    Parameters
    ----------
    hdus: [FITS object ... ]
        A list or tuple of FITS objects containing the Image_HDU's with entries to be compared.

    Returns
    -------
    idx, max_bright: (int, int, int), float
        idx is the index of the brightest pixel, represented in a triple-tuple of
        the form (data-layer, row, column), usually of max lengths (64, 32, 32).
        max_bright is a float representing the brightness of the brightest pixel
        found.

    """
    # Instantiate variables
    max_bright = 0
    idx = 0

    # Iterate through the hdus in the FITS object
    for hdu in hdus:
        # Read image data from HDU
        pxls = hdu[0].read()

        # Hold the current idxs and brightness
        curr_idx, curr_bright = get_max(pxls)

        # Compare with maximums
        if curr_bright > max_bright:
            max_bright = curr_bright
            idx = curr_idx

    return idx, max_bright
