Resumable urlretrieve
=====================

[![PyPi version](http://img.shields.io/pypi/v/resumable-urlretrieve.svg)](https://pypi.python.org/pypi/resumable-urlretrieve)
[![Build Status](https://travis-ci.org/berdario/resumable-urlretrieve.png)](https://travis-ci.org/berdario/resumable-urlretrieve)

This is a drop-in replacement for `urllib.request.urlretrieve` that will automatically resume a partially-downloaded file (if the remote HTTP server supports `Range` requests).

    def urlretrieve(url: str, filename: Union[str, Path], reporthook=None, method='GET',
                    sha256sum=None, filesize=None, headers=None,
                    **kwargs) -> Dict[str, str]

There are only a few differences:

- The `filename` argument is not optional
- It returns the headers of the HTTP requests
- It will raise `resumable.DownloadError` if needed
- It relies on `requests`, and can thus accept a `headers` dictionary, or an `auth` argument

The `sha256sum` and `filesize` will be used (if supplied) to check the downloaded file against it, and prevent making another HTTP request in case it would have been already completed (Otherwise it'll rely on the server returned `Content-Length` and `Content-Range`).

Tested on Python >= 3.4.

The [license](LICENSE) for this package is MIT.
