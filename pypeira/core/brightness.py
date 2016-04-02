from __future__ import division

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
    hdus: [HDU objects ... ]
        A list or tuple of HDU objects containing the image data with entries to be compared.

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
        pxls = hdu.img

        # Hold the current idxs and brightness
        curr_idx, curr_bright = get_max(pxls)

        # Compare with maximums
        if curr_bright > max_bright:
            max_bright = curr_bright
            idx = curr_idx

    return idx, max_bright


def pixel_data(idx, hdus, zipped=False):
    """
    Functions as a wrapper for extracting data for a specific pixel for the
    different HDU formats (currently only using FITS).

    Parameters
    ----------
    idx: (int ... )
        The n-dimensional index of the pixel.
    hdus: [HDU, ... ]
        An iterable of HDU objects which contain the relevant data.
    zipped: bool, optional
        Specifies whether or not to return the time and pixel value zipped. That is, if zipped = True
        then the returned values are in the form

            [(timestamp, pixel_value), ... ]

        while if zipped = False, the returned values will in the form

            [timestamp, ... ], [pixel_value, ... ]

        The reason for this is that for some operations you might want to keep the timestamp
        and the pixel_value paired together, while in other cases, like when plotting, it's
        more convenient to have them in two different lists. Note that lists will still
        have the same order, thus (timestamps[i], pixel_values[i]) for zipped = False is the
        same as the ith pair if we had zipped = True.

    Returns
    -------
    pxl_data: iterable (list for now, might turn into generator if the process turns out to be demanding)
        The entire set of data for the specified index/pixel in this set of HDUs.

    None
        If the file type/extension is not known.
    """
    # Conversion from secs to BMJD
    sec_to_day = 1 / (3600 * 24)

    # Dimension of data cube / number of images in data cube - normally 64
    # Assuming same dimension for all data cubes
    dims = hdus[0].ndims[0]

    # Prove the first HDU to get the total number of entries needed
    # Assuming all HDUs to have the same dimensions
    pix_vals = np.empty(dims * len(hdus))
    times = np.empty(dims * len(hdus))

    # Sort the HDUs using the Barycenter Mod. Julian Date of the observation as key
    hdus.sort(key=lambda x: x.timestamp)

    # Iterate through the HDUs
    for j in range(0, len(hdus)):
        # Array of pixel values for
        np.put(pix_vals, np.arange(j * dims, j * dims + dims), hdus[j].pixel_values(idx))

        # Assume equal time between each integration
        time_increment = (hdus[j].integ_end - hdus[j].integ_start) / hdus[j].ndims[0]
        times_curr = [(hdus[j].timestamp + (time_increment * i * sec_to_day)) for i in range(0, hdus[j].ndims[0])]

        # Array of all the timestamps, where we add i * frametime to the timestamp
        np.put(times, np.arange(j * dims, j * dims + dims), times_curr)

    if zipped:
        # Returns the two arrays zipped in (time, pix_val)-pairs
        return zip(times, pix_vals)
    else:
        # Returns the two arrays separate: times, pix_vals
        return times, pix_vals
