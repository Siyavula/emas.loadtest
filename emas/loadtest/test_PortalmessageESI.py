# -*- coding: iso-8859-15 -*-
"""test_portalmessage_esi FunkLoad test

$Id: $
"""
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from funkload.utils import Data
#from funkload.utils import xmlrpc_get_credential

class PortalmessageESI(FunkLoadTestCase):
    """XXX

    This test use a configuration file PortalmessageESI.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        # XXX here you can setup the credential access like this
        # credential_host = self.conf_get('credential', 'host')
        # credential_port = self.conf_getInt('credential', 'port')
        # self.login, self.password = xmlrpc_get_credential(credential_host,
        #                                                   credential_port,
        # XXX replace with a valid group
        #                                                   'members')

    def test_portalmessage_esi(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        self.setHeader('X-ESI', 'esi')
        self.get(server_url + "/login",
            description="Get /login")

        self.setHeader('X-ESI', 'esi')
        self.post(server_url + "/login_form", params=[
            ['came_from', ''],
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
            ['__ac_name', 'tester1000'],
            ['__ac_password', '12345'],
            ['submit', 'Log in']],
            description="Post /login_form")

        self.setHeader('X-ESI', 'esi')
        self.get(server_url + "/",
            description="Get /")

        self.setHeader('X-ESI', 'esi')
        self.get(server_url + "/@@change-password",
            description="Get /@@change-password")

        self.setHeader('X-ESI', 'esi')
        self.post(server_url + "/@@change-password", params=[
            ['userid', ''],
            ['fieldset.current', ''],
            ['form.current_password', '12345'],
            ['form.new_password', '12345'],
            ['form.new_password_ctl', '12345'],
            ['form.actions.reset_passwd', 'Change Password'],
            ['_authenticator', 'f3be0edec80a3b0236b31d638edbbdcd1dfdd69e']],
            description="Post /@@change-password")

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
