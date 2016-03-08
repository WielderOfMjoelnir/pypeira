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
