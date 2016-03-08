import pandas as pd


def to_timeseries(data):
    # TODO: Make waaaaaay more general. Allow for steps specification, or if they want in seconds, minutes, etc.
    """

    :param data: 1-dimension iterable.
    :return: pandas.Series object
    """

    return pd.Series(data)
