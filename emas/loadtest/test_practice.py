# -*- coding: utf-8 -*-
"""Practice System FunkLoad test"""

import unittest
from collective.funkload import testcase
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import xmlrpc_get_credential

class practice(FunkLoadTestCase):
    """Functional test for practice system

    This test use a configuration file practice.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        credential_host = self.conf_get('credential', 'host')
        credential_port = self.conf_getInt('credential', 'port')
        self.login, self.password = xmlrpc_get_credential(credential_host,
                                                          credential_port,
                                                          'members')

    def test_PracticeSystem(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        self.get("http://qa.everythingmaths.co.za/",
            description="Get /")
        self.get("http://qa.everythingmaths.co.za/login?ajax_load=1335182298146",
            description="Get /login")
        self.post("http://qa.everythingmaths.co.za/login_form", params=[
            ['came_from', 'http://qa.everythingmaths.co.za/'],
            ['next', ''],
            ['ajax_load', '1335182298146'],
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
            ['submit', 'Log in']],
            description="Post /login_form")
        self.get("http://qa.everythingmaths.co.za/",
            description="Get /")
        self.get("http://qa.everythingmaths.co.za/@@practice",
            description="Get /@@practice")
        self.get("http://qa.everythingmaths.co.za/@@practice/static/thumbs_up_24.png%27;",
            description="Get /@@practice/static/thumbs_up_24.png%27;")
        self.get("http://qa.everythingmaths.co.za/@@practice/static/please_wait_24.gif%27;",
            description="Get /@@practice/static/please_wait_24.gif%27;")
        self.get("http://qa.everythingmaths.co.za/acl_users/credentials_cookie_auth/require_login?came_from=http%3A//qa.everythingmaths.co.za/%40%40practice/static/thumbs_up_24.png%2527%253B",
            description="Get /acl_users/credenti..._auth/require_login")
        self.get("http://qa.everythingmaths.co.za/acl_users/credentials_cookie_auth/require_login?came_from=http%3A//qa.everythingmaths.co.za/%40%40practice/static/please_wait_24.gif%2527%253B",
            description="Get /acl_users/credenti..._auth/require_login")
        self.post("http://qa.everythingmaths.co.za/@@practice/set_filter", params=[
            ['selected1', 'on'],
            ['selected2', 'on']],
            description="Post /@@practice/set_filter")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['click1', 'Check']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['nextPage', 'Go to next question']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['click1', 'Check']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['nextPage', 'Go to next question']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['question1b', ''],
            ['click1', 'Check']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['question1b', ''],
            ['nextPage', 'Go to next question']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['click1', 'Check']],
            description="Post /@@practice/submit_response")
        self.get("http://qa.everythingmaths.co.za/@@practice/question",
            description="Get /@@practice/question")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['nextPage', 'Go to next question']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['click1', 'Check']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['nextPage', 'Go to next question']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['question1b', ''],
            ['click1', 'Check']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['question1b', ''],
            ['nextPage', 'Go to next question']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['question1b', ''],
            ['click1', 'Check']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['question1b', ''],
            ['nextPage', 'Go to next question']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['question1b', ''],
            ['click1', 'Check']],
            description="Post /@@practice/submit_response")
        self.post("http://qa.everythingmaths.co.za/@@practice/submit_response", params=[
            ['question1a', ''],
            ['question1b', ''],
            ['nextPage', 'Go to next question']],
            description="Post /@@practice/submit_response")
        self.get("http://qa.everythingmaths.co.za/@@practice/dashboard",
            description="Get /@@practice/dashboard")
        self.get("http://qa.everythingmaths.co.za/@@practice/chapter_vote/4?_=1335182470909",
            description="Get /@@practice/chapter_vote/4")

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")


def test_suite():
    return unittest.makeSuite(practice)

additional_tests = test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
