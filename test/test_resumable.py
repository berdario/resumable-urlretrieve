import pytest

import os
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from tempfile import NamedTemporaryFile
from unittest.mock import patch
from functools import partial
from collections import namedtuple

from RangeHTTPServer import RangeRequestHandler

from resumable import urlretrieve, sha256, DownloadError

FileStats = namedtuple('FileStats', 'sha256sum size')

PORT = 8000

@pytest.fixture(scope='module')
def httpd():
    httpd = HTTPServer(('', PORT), RangeRequestHandler)
    Thread(target=httpd.serve_forever, daemon=True).start()


@pytest.fixture(scope='module')
def simple_httpd():
    port = PORT+1
    httpd = HTTPServer(('', port), SimpleHTTPRequestHandler)
    Thread(target=httpd.serve_forever, daemon=True).start()
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
    retrieval = complete_downloader()
    assert retrieval.headers['Content-Length'] < testfile_stats.size
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
    last_touched = os.stat(partial_download.name).st_mtime
    with pytest.raises(DownloadError):
        urlretrieve('http://localhost:%s/test/trust.pdf' % PORT,
                    partial_download.name,
                    filesize=testfile_stats.size-1)
    assert last_touched == os.stat(partial_download.name).st_mtime


def test_wronghash(httpd, partial_download):
    with pytest.raises(DownloadError):
        urlretrieve('http://localhost:%s/test/trust.pdf' % PORT,
                    partial_download.name,
                    sha256sum='')


def test_norange(simple_httpd, partial_download, testfile_stats):
    urlretrieve('http://localhost:%s/test/trust.pdf' % simple_httpd, partial_download.name)
    assert testfile_stats.sha256sum == sha256(partial_download.name)
