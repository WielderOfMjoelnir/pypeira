import numpy as np


def get_max(data, max_val=0, idx=0):
    # TODO: Handle aribtrary number of dimensions
    """

    :param data: Multidimensional numpy array containing the pixels.
    :param max_val: The maximum value to compare to. Default = 0.
    :param idx: The index of the current maximum value. Default = 0.
    :return: (idx, max_val)-tuple,
    where idx are the indices of the maximum value, and max_val the maximum value.
    """
    # Use np.ndenumerate(data) to iterate through (idx, val)-pairs
    # i.e. (i, j, k), data[i][j][k] pairs
    for i, j in np.ndenumerate(data):
        if not np.isnan(j) and j > max_val:
            idx = i
            max_val = j

    return idx, max_val


def get_brightest(fits):
        """
        Obtains the brightest pixel together with it's indices.

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

            # Hold the current idxs and brightness
            curr_idx, curr_bright = get_max(pxls)

            # Compare with maximums
            if curr_bright > max_bright:
                max_bright = curr_bright
                idx = curr_idx

        return idx, max_bright
