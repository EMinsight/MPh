﻿"""Tests the server class."""
__license__ = 'MIT'


########################################
# Dependencies                         #
########################################
import parent # noqa F401
import mph
import logging
from sys import argv


########################################
# Fixtures                             #
########################################
server = None


def setup_module():
    pass


def teardown_module():
    if server and server.running():
        try:
            server.stop()
        except Exception:
            pass


########################################
# Tests                                #
########################################

def test_start():
    global server
    server = mph.Server(cores=1, port=2035)
    assert server.running()
    assert server.port == 2035


def test_stop():
    server.stop()
    assert not server.running()


########################################
# Main                                 #
########################################

if __name__ == '__main__':

    arguments = argv[1:]
    if 'log' in arguments:
        logging.basicConfig(
            level   = logging.DEBUG if 'debug' in arguments else logging.INFO,
            format  = '[%(asctime)s.%(msecs)03d] %(message)s',
            datefmt = '%H:%M:%S')

    setup_module()
    try:
        test_start()
        test_stop()
    finally:
        teardown_module()
