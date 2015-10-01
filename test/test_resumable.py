import pytest # type: ignore

import os
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler # type: ignore
from tempfile import NamedTemporaryFile
from unittest.mock import patch # type: ignore
from functools import partial # type: ignore
from typing import NamedTuple

from RangeHTTPServer import RangeRequestHandler # type: ignore

from resumable import urlretrieve, sha256, DownloadError

FileStats = NamedTuple('FileStats', [('sha256sum', str), ('size', int)])

PORT = 8000

@pytest.fixture(scope='module')
def httpd():
    httpd = HTTPServer(('', PORT), RangeRequestHandler)
    Thread(target=httpd.serve_forever, daemon=True).start() # type: ignore


@pytest.fixture(scope='module')
def simple_httpd():
    port = PORT+1
    httpd = HTTPServer(('', port), SimpleHTTPRequestHandler)
    Thread(target=httpd.serve_forever, daemon=True).start() # type: ignore
    return port


@pytest.fixture(scope='module')
def testfile_stats():
    fname = 'test/trust.pdf'
    return FileStats(sha256(fname), os.stat(fname).st_size)


@pytest.yield_fixture()
def partial_download(httpd):
    with NamedTemporaryFile() as tempfile:
        urlretrieve('http://localhost:%s/test/trust.pdf.partial' % PORT, tempfile.name)
        yield tempfile


def test_urlretrieve(httpd, partial_download, testfile_stats):
    complete_downloader = partial(urlretrieve, 'http://localhost:%s/test/trust.pdf' % PORT, partial_download.name)
    headers = complete_downloader()
    assert int(headers['Content-Length']) < testfile_stats.size
    assert testfile_stats.sha256sum == sha256(partial_download.name)
    last_touched = os.stat(partial_download.name).st_mtime
    complete_downloader()
    assert last_touched == os.stat(partial_download.name).st_mtime
    with patch('socket.socket.__new__', side_effect=Exception):
        complete_downloader(sha256sum=testfile_stats.sha256sum)
        assert last_touched == os.stat(partial_download.name).st_mtime
        complete_downloader(filesize=testfile_stats.size)
        assert last_touched == os.stat(partial_download.name).st_mtime


def test_wrongsize(httpd, partial_download, testfile_stats):
    with pytest.raises(DownloadError):
        urlretrieve('http://localhost:%s/test/trust.pdf' % PORT,
                    partial_download.name,
                    filesize=testfile_stats.size-1)


def test_wronghash(httpd, partial_download):
    with pytest.raises(DownloadError):
        urlretrieve('http://localhost:%s/test/trust.pdf' % PORT,
                    partial_download.name,
                    sha256sum='')


def test_norange(simple_httpd, partial_download, testfile_stats):
    urlretrieve('http://localhost:%s/test/trust.pdf' % simple_httpd, partial_download.name)
    assert testfile_stats.sha256sum == sha256(partial_download.name)
