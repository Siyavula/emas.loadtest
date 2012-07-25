# -*- coding: utf-8 -*-
"""Exam Zone FunkLoad test"""

import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase


class examzone(FunkLoadTestCase):
    """Functional test for examzone site

    This test use a configuration file examezone.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')

        # better set the HTTP_USER_AGENT header to inform the theme that this
        # is a mxit request.
        self.addHeader('USER_AGENT', 'MXit WebBot')
        self.debugHeaders()

    def test_ExamZone(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------
        
        base_url = "http://m.qa.everythingmaths.co.za/grade-10"
        examzone_url = base_url + "/exam-zone"

        self.get(base_url, description="Get /maths/grade-10")
        
        # prep response params and headers
        url = base_url + "/@@mxitpaymentresponse"
        self.addHeader("X_MXIT_USERID_R", "m1")
        params = {
            "mxit_transaction_res": "0"
        }
        description = "MXit response"
        self.post(url, params, description)

        self.get(examzone_url, description="Get /maths/grade-10")
        body = self.getBody()

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")


def test_suite():
    return unittest.makeSuite(examzone)

additional_tests = test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
