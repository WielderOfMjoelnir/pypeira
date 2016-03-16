import os

from fits import read_fits

_readers = {
    'fits': read_fits
}


def _read_file(path, ftype=None, data_type=None, headers_only=False, image_only=False, *args, **kwargs):
    """
    Only reads one file. Main purpose is to be called by read() to read single
    files.

    Parameters
    ----------
    path: str
        The path of the file you want to read. Unlike read() it does not handle both
        files and directorys, only files.
    ftype: str, optional
        The file type/extension of the file you want to read data from. If specified
        the extension of the file will be checked to make sure it is as required.
    data_type: str, optional
        See read().
    headers_only: bool, optional
        See read().
    image_only: bool, optional
        See read().
    *args: optional
        Contains all arguments that will be passed on to the actual read function, where the
        reader function used for each file type/extension is as specified above.
    **kwargs: optional
        Same as for 'args'. Contains all keyword arguments that will be passed onto the actual
        reader function, where the reader used for each file type/extension is as specified above.

    Returns
    -------
    data: HDU object (See pypeira.core.hdu) or None
        Returns HDU object as read by the reader function for that specific file type.
        If no reader is found for the given file type, then the returned 'data' will be None.

    """
    data = None
    # Grab extension of file
    root, ext = os.path.splitext(path)

    # If ftype is not specified then set ftype to be the extension of the file to be read
    if ftype is None:
        ftype = ext[1:]

    # Type-check the file
    if ext[1:].lower() == ftype.lower():
        # Grab the reader used for this file type. _readers can be found at the start of this file.
        reader = _readers.get(ftype.lower())

        # Check if reader is available
        if reader is None:
            raise RuntimeError("No reader found for {0} file type.".format(ftype))

        # Check if data_type is specified, and if so, check that file satisfies this requirement.
        if data_type is not None:
            # Assuming files are of the form "filename_*_datatype.ext"
            # If this is not a standard, then this validity check will be changed in the future.
            if data_type == root.split('_')[-1]:
                data = reader(path, headers_only, image_only, *args, **kwargs)
        else:
            data = reader(path, headers_only, image_only, *args, **kwargs)

    return data