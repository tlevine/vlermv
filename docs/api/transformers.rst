*****************
Key Transformers
*****************

The following transformers are included.

``magic``
    Magically figure out a reasonable file name.
``base64``
    File name is the base 64 encoding of the key.
``tuple``
    Key must be a tuple; the right most element becomes a file name,
    and the preceding elements are directories.
``simple``
    Key is used as the file name directory. It must be a string without slashes.
``slash``
    Like simple, except that slashes may be used to separate directories
``backslash``
    Like simple, except that backslashes may be used to separate directories

