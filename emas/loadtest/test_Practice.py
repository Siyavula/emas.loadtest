# -*- coding: iso-8859-15 -*-
"""practice FunkLoad test

$Id: $
"""
import cPickle
import unittest
import socket
import requests
from lxml import html
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from funkload.utils import Data, extract_token
from funkload.utils import xmlrpc_get_credential

socket.setdefaulttimeout(30)

class Practice(FunkLoadTestCase):
    """XXX

    This test use a configuration file Practice.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        self.answer_server_url = self.conf_get('main', 'answer_server_url')
        # XXX here you can setup the credential access like this
        credential_host = self.conf_get('credential', 'host')
        credential_port = self.conf_getInt('credential', 'port')
        self.login, self.password = xmlrpc_get_credential(credential_host,
                                                          credential_port,
                                                          'funkloadgroup')

    def test_practice(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        # /tmp/tmpCz5DHd_funkload/watch0001.request
        self.get(server_url + "/",
            description="Get /")
        # /tmp/tmpCz5DHd_funkload/watch0090.request
        self.logd("Getting login form.")
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

        self.logd("Getting practice page.")
        self._accept_invalid_links = True
        self.get(server_url + "/@@practice/grade-10",
            description="Get /@@practice/grade-10")

        self.logd("Getting practice chapter.")
        self.get(server_url + "/@@practice/select_chapter/5",
            description="Get /@@practice/select_chapter/5")
        rtoken = 'Random seed: </b>'
        ttoken = 'Template id: </b>'
        end = '</div>'

        for count in range(0,9):
            self.logd("Getting questions.")
            seed = int(extract_token(self.getBody(), rtoken, end))
            template_id = int(extract_token(self.getBody(), ttoken, end))
            answers_url = '%s/?templateId=%s&seed=%s' % (self.answer_server_url,
                                                         template_id,
                                                         seed)
            response = requests.get(answers_url)

            answers = eval(response.text)
            postData = {}
            for questionIdx, subanswers in enumerate(answers):
                questionNumber = questionIdx +1
                for answerIdx, answer in enumerate(subanswers):
                    answerNumber = chr(ord('a')+answerIdx)
                    key = 'question%s%s' % (questionNumber, answerNumber)
                    postData[key] = answer

            self.post(server_url + "/@@practice/submit_response",
                      params=postData,
                      description="Post /@@practice/submit_response")
            self.assert_('Correct!' in self.getBody(), "Answer incorrect.")

            postData = {'nextPage': 'Go to next question'}
            self.post(server_url + "/@@practice/submit_response",
                      params=postData,
                      description="Post /@@practice/submit_response")

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
