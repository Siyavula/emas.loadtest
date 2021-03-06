# -*- coding: iso-8859-15 -*-
"""Login FunkLoad test

$Id: $
"""
import cPickle
import unittest
from lxml import html
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from funkload.utils import Data, extract_token
from funkload.utils import xmlrpc_get_credential

class Login(FunkLoadTestCase):
    """XXX

    This test use a configuration file Login.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self._accept_invalid_links = True
        self.server_url = self.conf_get('main', 'url')
        # XXX here you can setup the credential access like this
        credential_host = self.conf_get('credential', 'host')
        credential_port = self.conf_getInt('credential', 'port')
        self.login, self.password = xmlrpc_get_credential(credential_host,
                                                          credential_port,
                                                          'funkloadgroup')

    def test_login(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        self.get(server_url + "/",
            description="Get /")
        self.post(server_url + "/login_form", params=[
            ['came_from', self.server_url],
            ['next', ''],
            ['ajax_load', ''],
            ['ajax_include_head', ''],
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
            ['submit', 'Sign in']],
            description="Post /login_form")

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")


if __name__ in ('main', '__main__'):
    unittest.main()
