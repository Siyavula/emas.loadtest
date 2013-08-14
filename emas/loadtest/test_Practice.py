# -*- coding: iso-8859-15 -*-
"""practice FunkLoad test

$Id: $
"""
import cPickle
import unittest
from lxml import html
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from funkload.utils import Data, extract_token
from funkload.utils import xmlrpc_get_credential

class Practice(FunkLoadTestCase):
    """XXX

    This test use a configuration file Practice.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.answers = cPickle.load(
            open('monassis/oracular-answers.pickle','rb'))
        self.server_url = self.conf_get('main', 'url')
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
        # /tmp/tmpCz5DHd_funkload/watch0050.request
        self.get("http://themes.googleusercontent.com/static/fonts/montserrat/v3/zhcz-_WihjSQC0oHJ9TCYBsxEYwM7FgeyaSgU71cLG0.woff",
            description="Get /static/fonts/monts...FgeyaSgU71cLG0.woff")
        # /tmp/tmpCz5DHd_funkload/watch0090.request
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

        # /tmp/tmpCz5DHd_funkload/watch0101.request
        self.get(server_url + "/@@practice/grade-10",
            description="Get /@@practice/grade-10")

        # /tmp/tmpCz5DHd_funkload/watch0139.request
        self.get(server_url + "/@@practice/select_chapter/5",
            description="Get /@@practice/select_chapter/5")
        self._accept_invalid_links = True
        token = 'Random seed: </b>'
        end = '</div>'
        seed = int(extract_token(self.getBody(), token, end))
        token = 'Template id: </b>'
        template_id = int(extract_token(self.getBody(), token, end))
        answers = self.answers[template_id][seed]
        dom = html.fromstring(self.getBody())
        for node in dom.xpath('//*[@class="answer-input"]'):
            if (node.attrib.get('disabled') is None) and (node.attrib.get('readonly') is None):
                questionNumber= int(node.attrib['name'][8:-1])
                subQuestionIdx = questionNumber -1
                subanswers = answers[subQuestionIdx]
                postData = {}
                for idx, answer in enumerate(subanswers):
                    key = 'question%s%s' % (questionNumber, chr(ord('a')+idx))
                    postData[key] = answer
                self.post(server_url + "/@@practice/submit_response",
                          params=postData,
                          description="Post /@@practice/submit_response")
                self.assert_('Correct!' in self.getBody(), "Answer incorrect.")
                dom = html.fromstring(self.getBody())

        postData = {'nextPage': 'Go to next question'}
        self.post(server_url + "/@@practice/submit_response",
                  params=postData,
                  description="Post /@@practice/submit_response")

        # /tmp/tmpCz5DHd_funkload/watch0153.request
        self.get("http://cdn.mathjax.org/mathjax/latest/fonts/HTML-CSS/TeX/woff/MathJax_Size4-Regular.woff",
            description="Get /mathjax/latest/fon..._Size4-Regular.woff")
        # /tmp/tmpCz5DHd_funkload/watch0154.request
        self.get("http://cdn.mathjax.org/mathjax/latest/fonts/HTML-CSS/TeX/woff/MathJax_Main-Regular.woff",
            description="Get /mathjax/latest/fon...x_Main-Regular.woff")
        # /tmp/tmpCz5DHd_funkload/watch0155.request
        self.get("http://cdn.mathjax.org/mathjax/latest/fonts/HTML-CSS/TeX/woff/MathJax_Math-Italic.woff",
            description="Get /mathjax/latest/fon...ax_Math-Italic.woff")
        # /tmp/tmpCz5DHd_funkload/watch0156.request
        self.get("http://cdn.mathjax.org/mathjax/latest/fonts/HTML-CSS/TeX/woff/MathJax_Size1-Regular.woff",
            description="Get /mathjax/latest/fon..._Size1-Regular.woff")

	
        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
