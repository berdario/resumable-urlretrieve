Resumable urlretrieve
========================

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

It works on Python >= 3.5.

License
=======

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
