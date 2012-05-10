# -*- coding: utf-8 -*-
"""Mobile Site FunkLoad test"""

import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase

class mobile(FunkLoadTestCase):
    """Functional test for mobile site

    This test use a configuration file mobile.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')

    def test_MobileSites(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        self.get("http://m.qa.everythingmaths.co.za/",
            description="Get /")

        for path in open('maths_paths.txt').readlines():
            url = "http://m.qa.everythingmaths.co.za" + path
            self.get(path, description="Get " + path)

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")


def test_suite():
    return unittest.makeSuite(mobile)

additional_tests = test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
