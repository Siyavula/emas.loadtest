# -*- coding: utf-8 -*-
"""Exam Zone FunkLoad test"""

import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import xmlrpc_get_credential
from funkload.utils import xmlrpc_list_credentials


class past_exam_papers(FunkLoadTestCase):
    """Functional test for past_examp_papers

    This test use a configuration file past_exam_papers.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        self.credential_host = self.conf_get('credential', 'host')
        self.credential_port = self.conf_getInt('credential', 'port')

        # better set the HTTP_USER_AGENT header to inform the theme that this
        # is a mxit request.
        self.addHeader('USER_AGENT', 'MXit WebBot')
        self.debugHeaders()

    def test_ExamZone(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------
        
        base_url = "http://m.qa.everythingmaths.co.za/grade-10"
        examzone_url = base_url + "/past-exam-papers"

        self.get(base_url, description="Get /maths/grade-10")
        
        # prep response params and headers
        url = base_url + "/@@mxitpaymentresponse"
        params = {
            "mxit_transaction_res": "0"
        }
        description = "MXit response"

        creds = xmlrpc_list_credentials(self.credential_host,
                                        self.credential_port,
                                        group='examzonegroup')
        for login, pwd in creds:
            self.delHeader("X_MXIT_USERID_R")
            self.addHeader("X_MXIT_USERID_R", login)
            self.post(url, params, description)

            self.get(examzone_url,
                     description="Get /maths/grade-10/past-exam-papers")
            body = self.getBody()

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")


def test_suite():
    return unittest.makeSuite(past_exam_papers)

additional_tests = test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
