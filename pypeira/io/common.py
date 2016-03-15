import os
import fitsio

import fits


def read_file(path, ftype, fits_type=None, headers_only=False, image_only=False, *args, **kwargs):
    """
    Only reads one file. Main purpose is to be called by read() to read single
    files.

    Parameters
    ----------
    path: str
        The path of the file you want to read. Unlike read() it does not handle both
        files and directorys, only files.
    ftype: str
        The file type/extension of the file you want to read data from. Unlike read()
        this argument is required.
    fits_type: str, optional
        See read().
    headers_only: bool, optional
        See read().
    image_only: bool, optional
        See read().
    *args: optional
        Contais all arguments that will be passed on to the actual read function, where the
        reader function used for each file type/extension is as specified above.
    **kwargs: optional
        Same as for 'args'. Contains all keyword arguments that will be passed onto the actual
        reader function, where the reader used for each file type/extension is as specified above.

    Returns
    -------

    """
    data = None
    # Reads a file
    root, ext = os.path.splitext(path)

    if ext[1:] == ftype:
        if ftype == "fits":
            if fits_type is not None:
                if fits_type == root.split('_')[-1]:
                    data = fits.read_fits(path, headers_only, image_only, *args, **kwargs)
            else:
                data = fits.read_fits(path, headers_only, image_only, *args, **kwargs)

    return data


def read(path, ftype='fits', fits_type=None, walk=True, headers_only=False, image_only=False, *args, **kwargs):
    """
    Proper description will be written when implementation is more complete.

    Reads files from path.

    Parameters
    ----------
    path: str
        The path you want to read files from. Can be directory or file name. If path corresponds
        to a directory and 'walk' is true, it will walk the directory and its children, reading
        files as it goes along, otherwise it will simply read the files in the directory given.
        If file name then it will simply read the data form the given file.
    ftype: str, optional
        The file type/extension of the files you want to read data from. Default is 'fits'.
    fits_type: str, optional
        The type of FITS file you want to read. If not None, will filter out all path names not
        ending in "fits_type.FITS", i.e. if fits_type = 'bcd'

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
        reader function, where the reader used for each file type/extension is as specified above.
        (The specification will come later on. For now there's nothing more than fitsio.read())

    Returns
    -------
    FITS object
        If 'path' pointed to is a
            single file - returned 'data' will be a single FITS object,
            directory - returned 'data' will be a list of FITS objects,
            no valid files - returned 'data' will be None. "valid" is as specified by the
            ftype argument, which defaults to 'fits'.

        Note for a single file the returned 'data' will be only one FITS object, NOT a list
        as if the path is a directory.

        See fitsio.fitslib.FITS for implementation of FITS.

    FITSHDR object
        If 'headers_only' is not False it will return in the same manner as for the FITS object,
        but now the type of the files will be FITSHDR objects.

        See fitsio.fitslib.FITSHDR for implementation of FITSHDR.

    numpy.array
        If 'image_only' is not False it will return in the same manner as for the FITS object,
        but now the type of the tiles will be numpy.arrays.

    Raises
    ------
    OSError
        Raises OSError if the given path does not exist.
    """
    # Reads from whatever path the user inputs

    # Initialize variables
    data = list()

    # First check if path is valid, raise OSError() if invalid
    if not os.path.exists(path):
        raise OSError(path)

    # Check if file
    if os.path.isfile(path):
        # Read file
        data = read_file(path, ftype, fits_type, headers_only, image_only, *args, **kwargs)

    # Check if dir
    elif os.path.isdir(path):
        # If dir to be walked
        if walk:
            # Walk directory
            nodes = os.walk(path)

            # Iterate through the nodes:
            # node[0] is the current node
            # node[1] contains folders in current node
            # node[2] contains the file names in current node
            for node in nodes:
                for fname in node[2]:
                    # Create path for 'fname'
                    file_path = os.path.join(node[0], fname)
                    # Call read_file() on each 'fname'
                    file_data = read_file(file_path, ftype, fits_type, headers_only, image_only, *args, **kwargs)

                    # If read_file() was successful; that is returned not None,
                    # append returned value to 'data' list
                    if file_data is not None:
                        data.append(file_data)
        else:
            # Read files from top dir only
            for fname in os.listdir(path):
                # os.listdir() returns a list of paths as strings for each file in path
                file_data = read_file(fname, ftype, fits_type, headers_only, image_only, *args, **kwargs)

                # if read_file() was successful, append returned value to 'data' list
                if file_data is not None:
                    data.append(file_data)

    return data


def pixel_data(idx, hdus, zipped=False):
    """
    Functions as a wrapper for extracting data for a specific pixel for the
    different HDU formats (currently only using FITS).

    Parameters
    ----------
    idx: (int ... )
        The n-dimensional index of the pixel.
    hdus: FITS objects (no others for now)
        An iterable of HDUs which contains the relevant data.
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
        If no the file type/extension is not known.
    """
    if isinstance(hdus[0], fitsio.fitslib.FITS):
        # If the first entry is FITS object, then set pxl_data equal to
        # fits.pixel_data_single() called on each element of hdus together with idx.
        pxl_data = fits.pixel_data(idx, hdus)
    else:
        pxl_data = None

    if not zipped:
        # This unzips the list of (time, data)-tuples to return the lists times, pxl_values
        return zip(*pxl_data)
    else:
        # Or if zipped is untrue, return the (time, data)-tuples
        return pxl_data
