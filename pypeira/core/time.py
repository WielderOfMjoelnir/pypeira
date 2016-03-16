def hdu_get_time(hdu, time_format='bmjd'):
    """
    Will be used as a key function for the list.sort() or sorted() functions.
    Example,

        hdus.sort(key=key_fits_by_time)

    where hdus is a list of FITS objects, will call key_fits_by_time() on each element
    in the list, and then sort the elements according to the value returned from the
    key function, that is in this case key_fits_by_time().
    Parameters
    ----------
    hdu: FITS object
        The FITS object which is an element in the list that is to be sorted.
    time_format: str, optional
        The time format you want to sort by, even though it should not matter.

    Returns
    -------
    float
        It's the header entry BMJD_OBS (Barycentric Julian Date of observation), which
        will then be used as the comparison attribute of each element in the list to
        sorted.
    """
    format_to_kwrd = {
        'bmjd': 'BMJD_OBS',
        'hmjd': 'HMJD_OSB',
        'mjd': 'MJD_OBS',
        'utc': 'UTCS_OSB',
        'date': 'DATE_OBS',
        'dce': 'ET_OBS'
    }

    if format_to_kwrd.get(time_format):
        return hdu.hdr[format_to_kwrd.get(time_format)]
    else:
        return None
