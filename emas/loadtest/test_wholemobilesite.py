# -*- coding: utf-8 -*-
"""FunkLoad test to read the whole mobile site - all pages."""

import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase

class WholeMobileSite(FunkLoadTestCase):
    """Functional test for whole mobile site

    This test uses a configuration file WholeMobileSite.conf
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        self.paths_file = self.conf_get('main', 'paths_file')

    def test_WholeMobileSite(self):
        server_url = self.server_url

        self.get(server_url, description="Get /")

        for path in open(self.paths_file).readlines():
            path = path.rstrip('\n')
            url = '/'.join([server_url, path])
            print url
            self.get(url, description="Get " + path)

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")


def test_suite():
    return unittest.makeSuite(WholeMobileSite)

additional_tests = test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
