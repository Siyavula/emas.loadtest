# -*- coding: iso-8859-15 -*-
"""practice FunkLoad test

$Id: $
"""
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from funkload.utils import Data
#from funkload.utils import xmlrpc_get_credential

class Practice(FunkLoadTestCase):
    """XXX

    This test use a configuration file Practice.conf.
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
        # /tmp/tmpCz5DHd_funkload/watch0086.request
        self.post("http://safebrowsing.clients.google.com/safebrowsing/downloads?client=navclient-auto-ffox&appver=22.0&pver=2.2&wrkey=AKEgNitFmiyqCABfE19sA9qctohQ2Ca8tEbDi-xDcVzSqRmN5Sqw0ETDiSZ6nWuyes-ZzEH8LUs5gmnT_uAdABQOw053vA7uPg==", Data('text/plain', '''goog-phish-shavar;a:288853-294646:s:139003-143094:mac
goog-malware-shavar;a:113422-122391:s:107521-118823:mac
'''),
            description="Post /safebrowsing/downloads")
        # /tmp/tmpCz5DHd_funkload/watch0087.request
        self.get("http://safebrowsing-cache.google.com/safebrowsing/rd/ChNnb29nLW1hbHdhcmUtc2hhdmFyEAAYjbwHIKC8ByoGGd4BAP8AMgYN3gEA_w8",
            description="Get /safebrowsing/rd/Ch...Gd4BAP8AMgYN3gEA_w8")
        # /tmp/tmpCz5DHd_funkload/watch0088.request
        self.get("http://safebrowsing-cache.google.com/safebrowsing/rd/ChFnb29nLXBoaXNoLXNoYXZhchABGOndCCCQ3ggqCPguAgD___8BMgbpLgIA_38",
            description="Get /safebrowsing/rd/Ch...AgD___8BMgbpLgIA_38")
        # /tmp/tmpCz5DHd_funkload/watch0089.request
        self.get("http://safebrowsing-cache.google.com/safebrowsing/rd/ChFnb29nLXBoaXNoLXNoYXZhchAAGPb9ESD6_REqBfh-BAAHMgX2fgQAAw",
            description="Get /safebrowsing/rd/Ch...qBfh-BAAHMgX2fgQAAw")
        # /tmp/tmpCz5DHd_funkload/watch0090.request
        self.post(server_url + "/login_form", params=[
            ['came_from', 'http://qap.everythingmaths.co.za'],
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
            ['__ac_name', 'tester100'],
            ['__ac_password', '12345'],
            ['submit', 'Sign in']],
            description="Post /login_form")
        # /tmp/tmpCz5DHd_funkload/watch0101.request
        self.get(server_url + "/@@practice/dashboard",
            description="Get /@@practice/dashboard")
        # /tmp/tmpCz5DHd_funkload/watch0139.request
        self.get(server_url + "/@@practice/select_chapter/105",
            description="Get /@@practice/select_chapter/105")
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
        # /tmp/tmpCz5DHd_funkload/watch0157.request
        self.post(server_url + "/@@practice/submit_response", params=[
            ['question1a', '333333'],
            ['click1', 'Check answer']],
            description="Post /@@practice/submit_response")

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
