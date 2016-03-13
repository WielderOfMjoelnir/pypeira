import os
import fitsio

import fits


def read_file(path, ftype, headers_only=False, image_only=False, *args, **kwargs):
    data = None
    # Reads a file
    root, ext = os.path.splitext(path)

    if ext[1:] == ftype:
        if ftype == "fits":
            # data will now be a list of FITS objects

            data = fits.read_fits(path, headers_only, image_only, *args, **kwargs)

    return data


def read(path, ftype='fits', fits_type='bcd', walk=True, headers_only=False, image_only=False, *args, **kwargs):
    # TODO: Need to account for the different types of FITS files, i.e. bcd, bimsk, bunc, cov2d, etc.
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

    print path

    # Check if file
    if os.path.isfile(path):
        # Read file
        data = read_file(path, ftype, headers_only, image_only, *args, **kwargs)

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
                    file_data = read_file(file_path, ftype, headers_only, image_only, *args, **kwargs)

                    # If read_file() was successful; that is returned not None,
                    # append returned value to 'data' list
                    if file_data is not None:
                        data.append(file_data)
        else:
            # Read files from top dir only
            for fname in os.listdir(path):
                # os.listdir() returns a list of paths as strings for each file in path
                file_data = read_file(fname, ftype, headers_only, image_only, *args, **kwargs)

                # if read_file() was successful, append returned value to 'data' list
                if file_data is not None:
                    data.append(file_data)

    return data
