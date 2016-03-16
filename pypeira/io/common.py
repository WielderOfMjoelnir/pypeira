import os
import numpy as np

from pypeira.io.reader import _read_file
from pypeira.core.hdu import HDU


def read(path, ftype='fits', data_type=None, walk=True, headers_only=False, image_only=False, *args, **kwargs):
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
    data_type: str, optional
        The type of FITS file you want to read. If not None, will filter out all path names not
        ending in "data_type.FITS", i.e. if data_type = 'bcd'

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
        raise RuntimeError("{0} does not exists.".format(path))

    # Check if file
    if os.path.isfile(path):
        # Read file
        if headers_only or image_only:
            data = _read_file(path, ftype, data_type, headers_only, image_only, *args, **kwargs)
        else:
            data = HDU(path, ftype=ftype, dtype=data_type)

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

                    if headers_only or image_only:
                        file_data = _read_file(file_path, ftype, data_type, headers_only, image_only,
                                               *args, **kwargs)
                        # If read was successful, append to data
                        if file_data is not None:
                            data.append(file_data)
                    else:
                        # Create HDU instance which will call _read_file() itself
                        hdu = HDU(file_path, ftype=ftype, dtype=data_type, *args, **kwargs)

                        # If read was successful, append to data
                        if hdu.has_data:
                            data.append(hdu)
        else:
            # Read files from top dir only
            for fname in os.listdir(path):
                # os.listdir() returns a list of paths as strings for each file in path
                file_data = _read_file(fname, ftype, data_type, headers_only, image_only, *args, **kwargs)

                # if _read_file() was successful, append returned value to 'data' list
                if file_data is not None:
                    data.append(file_data)

    return data
