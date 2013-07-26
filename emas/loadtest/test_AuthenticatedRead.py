# -*- coding: iso-8859-15 -*-
"""Test whole site funkLoad test

$Id: $
"""
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from funkload.utils import Data
from funkload.utils import xmlrpc_get_credential

class AuthenticatedRead(FunkLoadTestCase):
    """XXX

    This test use a configuration file AuthenticatedRead.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        self.paths_file = self.conf_get('main', 'paths_file')
        # XXX here you can setup the credential access like this
        credential_host = self.conf_get('credential', 'host')
        credential_port = self.conf_getInt('credential', 'port')
        self.login, self.password = xmlrpc_get_credential(credential_host,
                                                          credential_port,
                                                          'Member')

    def test_AuthenticatedRead(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        self.get(server_url + "/", description="Get /")
        self.get(server_url + "/login", description="Get /login")
        self.post(server_url + "/login_form", params=[
            ['came_from', ''],
            ['next', ''],
            ['target', ''],
            ['mail_password_url', ''],
            ['join_url', ''],
            ['form.submitted', '1'],
            ['js_enabled', '0'],
            ['cookies_enabled', ''],
            ['login_name', ''],
            ['pwd_empty', '0'],
            ['__ac_name', self.login],
            ['__ac_password', self.password],
            ['submit', 'Log in']],
            description="Post /login_form")

        for path in open(self.paths_file).readlines():
            path = path.rstrip('\n')
            url = '/'.join([server_url, path])
            print url
            self.get(url, description="Get " + path)

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
