#!/usr/bin/python3
"""
Official PEP list retrieval

Usage: just call the `urls` function of this module.

by Fede Bosio
Apr 20, 2020.
"""
import logging
from urllib import request as _request


log = logging.getLogger('PEP')


def urls():
    url_prefix = 'https://www.python.org/dev/peps/'
    req = _request.Request(url_prefix, headers={'User-Agent': 'Mozilla/5.0'})

    log.info('Retrieving web data...')
    data_pieces = _request.urlopen(req).read().decode()
    log.info('Successfully connected to ', url_prefix, '\n')

    data_pieces = data_pieces.split('id="numerical-index"')[1]
    data_pieces = data_pieces.split('</div>')[0]
    data_pieces = data_pieces.split('<td')
    _urls = [url_prefix + s.split('peps/')[1].split('>')[0][:-1]
             for s in data_pieces if 'peps' in s]

    log.info('Found something')
    for url in _urls:
        log.info(url)

    return _urls


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    urls()
