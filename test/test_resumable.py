import pytest # type: ignore

import errno
import os
import random
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler # type: ignore
from tempfile import NamedTemporaryFile
from unittest.mock import patch # type: ignore
from functools import partial # type: ignore
from typing import NamedTuple

from RangeHTTPServer import RangeRequestHandler # type: ignore

from resumable import urlretrieve, sha256, DownloadError

FileStats = NamedTuple('FileStats', [('sha256sum', str), ('size', int)])


def get_port():
    return random.randint(1024, 65536)


def get_httpd(request_handler):
    while True:
        try:
            port = get_port()
            return HTTPServer(('', port), request_handler)

        except OSError as e:
            if e.errno != errno.EADDRINUSE:
                raise


@pytest.fixture(scope='module')
def httpd():
    httpd = get_httpd(RangeRequestHandler)
    Thread(target=httpd.serve_forever, daemon=True).start() # type: ignore
    return httpd


@pytest.fixture(scope='module')
def simple_httpd():
    httpd = get_httpd(SimpleHTTPRequestHandler)
    Thread(target=httpd.serve_forever, daemon=True).start() # type: ignore
    return httpd


@pytest.fixture(scope='module')
def testfile_stats():
    fname = 'test/trust.pdf'
    return FileStats(sha256(fname), os.stat(fname).st_size)


@pytest.yield_fixture()
def partial_download(httpd):
    port = httpd.server_port

    with NamedTemporaryFile() as tempfile:
        urlretrieve('http://localhost:%s/test/trust.pdf.partial' % port, tempfile.name)
        yield tempfile


def test_urlretrieve(httpd, partial_download, testfile_stats):
    port = httpd.server_port
    complete_downloader = partial(urlretrieve, 'http://localhost:%s/test/trust.pdf' % port, partial_download.name)
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
    port = httpd.server_port

    with pytest.raises(DownloadError):
        urlretrieve('http://localhost:%s/test/trust.pdf' % port,
                    partial_download.name,
                    filesize=testfile_stats.size-1)


def test_wronghash(httpd, partial_download):
    port = httpd.server_port

    with pytest.raises(DownloadError):
        urlretrieve('http://localhost:%s/test/trust.pdf' % port,
                    partial_download.name,
                    sha256sum='')


def test_norange(simple_httpd, partial_download, testfile_stats):
    urlretrieve('http://localhost:%s/test/trust.pdf' % simple_httpd.server_port, partial_download.name)
    assert testfile_stats.sha256sum == sha256(partial_download.name)
