# -*- coding: iso-8859-15 -*-
"""PracticeDashboard FunkLoad test

$Id: $
"""
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from funkload.utils import Data
from funkload.utils import xmlrpc_get_credential

class Practicedashboard(FunkLoadTestCase):
    """XXX

    This test use a configuration file Practicedashboard.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        # XXX here you can setup the credential access like this
        credential_host = self.conf_get('credential', 'host')
        credential_port = self.conf_getInt('credential', 'port')
        self.login, self.password = xmlrpc_get_credential(credential_host,
                                                          credential_port,
                                                          'Member')

    def test_PracticeDashboard(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        # /tmp/tmphgMJEf_funkload/watch0001.request
        self.get(server_url + "/logout",
            description="Get /logout")
        # /tmp/tmphgMJEf_funkload/watch0007.request
        self.get(server_url + "/",
            description="Get /")
        # /tmp/tmphgMJEf_funkload/watch0009.request
        self.get(server_url + "/",
            description="Get /")

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
