#!python

import sys
import lxml.sax
from lxml import etree
from xml.sax.handler import ContentHandler
from tempfile import TemporaryFile
from xlwt import Workbook

"""
data example:

<funkload version="1.16.1" time="2013-09-13T02:00:47.717248">
<config key="sleep_time_min" value="0.0" />
<config key="node" value="siyavulap04" />
<config key="startup_delay" value="0.5" />
<config key="cycles" value="[50, 100, 200]" />
<config key="cycle_time" value="1.0" />
<config key="description" value="Test authenticated read of content." />
<config key="configuration_file" value="NNN.conf" />
<config key="class_title" value="NNN" />
<config key="server_url" value="http://example.com" />
<config key="module" value="test_NNN" />
<config key="id" value="test_NNN" />
<config key="class_description" value="Test reading of content." />
<config key="sleep_time" value="1.0" />
<config key="sleep_time_max" value="2.0" />
<config key="duration" value="180" />
<config key="method" value="test_NNN" />
<config key="log_xml" value="NNN-bench.xml" />
<config key="class" value="NNN" />
<config key="python_version" value="2.7.3" />
<response cycle="000" cvus="100" thread="057" suite="Practice"
    name="test_practice" step="001" number="011" type="link" result="Successful"
    url="/" code="200" description=""
    time="1377252663.41" duration="0.432377099991" />
<testResult cycle="000" cvus="050" thread="003" suite="NNN" name="test_NNN"  time="1379030449.23" result="Successful" steps="18" duration="47.1377151012" connection_duration="28.1033494473" requests="176" pages="18" xmlrpc="0" redirects="0" images="99" links="59" />
</funkload>

where:
    cycle       = the number of the current test cycle
    cvus        = the amount of concurrent users in this test cycle
    thread      = the id of the current thread
    suite       = the name of the test suite (the test's .__class__.__name__)
    name        = the method name of the test in the test suite
    step        = ?
    number      = the number of the response in this set (could be more than
                  one due to redirects)
    type        = HTTP request type (post, put, get, etc.)
    result      = A simple text representation of the result of this test
                  'Success', 'Failure', 'Error'
    url         = the HTTP response URL
    code        = HTTP response code (200, etc.)
    description = description of method? (rarely used)
    time        = the start time of the call
    duration    = the end time - the start time
"""


class MyContentHandler(ContentHandler):
    def __init__(self, workbook):
        self._workbook = workbook
        self._sheets = {}
        self._root = {}
        self._config = {}
        self._responses = {}
        self._testResults = {}

    def startElementNS(self, name, qname, attributes):
        uri, localname = name
        if localname == 'funkload':
            self.export_root(localname, qname, attributes)
        elif localname == 'config':
            self.export_config(localname, qname, attributes)
        elif localname == 'response':
            self.export_response(localname, qname, attributes)
        elif localname == 'testResult':
            self.export_testresult(localname, qname, attributes)

    def endElementNS(self, ns_name, qname):
        pass
   
    def export_root(self, localname, qname, attributes):
        attrs = self._getAttrs(attributes)
        name = self._worksheetName(localname, attrs)
        val = self._root.get(name, [])
        val.append(attrs)
        self._root[name] = val

    def export_config(self, localname, qname, attributes):
        attrs = self._getConfigAttrs(attributes)
        name = self._worksheetName(localname, attrs)
        val = self._config.get(name, [])
        val.append(attrs)
        self._config[name] = val

    def export_response(self, localname, qname, attributes):
        attrs = self._getAttrs(attributes)
        name = self._worksheetName(localname, attrs)
        val = self._responses.get(name, [])
        val.append(attrs)
        self._responses[name] = val

    def export_testresult(self, localname, qname, attributes):
        attrs = self._getAttrs(attributes)
        name = self._worksheetName(localname, attrs)
        val = self._testResults.get(name, [])
        val.append(attrs)
        self._testResults[name] = val

    def write_root(self):
        for ws_name, root_attrs in self._root.items():
            worksheet = self._getWorksheet(ws_name)
            for attrs in root_attrs:
                for idx, key in enumerate(['version', 'time']):
                    worksheet.write(idx, 0, key)
                    worksheet.write(idx, 1, attrs[key])

    def write_config(self):
        columns = ["sleep_time_min", "node", "startup_delay", "cycles",
                   "cycle_time", "description", "configuration_file",
                   "class_title", "server_url", "module", "id", 
                   "class_description", "sleep_time", "sleep_time_max",
                   "duration", "method", "log_xml", "class", "python_version"
                  ]
        for ws_name, config_attrs in self._config.items():
            worksheet = self._getWorksheet(ws_name)
            offset = worksheet.last_used_row +1
            for attrs in config_attrs:
                for idx, key in enumerate(columns):
                    value = attrs.get(key)
                    if value is not None:
                        worksheet.write(idx+offset, 0, key)
                        worksheet.write(idx+offset, 1, attrs.get(key))

    def write_responses(self):
        columns = ["cycle", "cvus", "thread", "suite", "name", "step", "number",
                   "type", "result", "url", "code", "description", "time",
                   "duration",]
        
        ws_names = self._responses.keys()
        ws_names.sort()
        for ws_count, ws_name in enumerate(ws_names):
            print 'Writing %s' % ws_name
            print '    %s of %s' % (ws_count, len(ws_names))
            worksheet = self._getWorksheet(ws_name)
            last_row = worksheet.last_used_row
            if last_row == 0:
                self._writeHeaders(worksheet, 0, columns)
            response_attrs = self._responses[ws_name]
            for response_count, attrs in enumerate(response_attrs):
                row_offset = last_row +1
                print 'Writing response number %s' % response_count
                for idx, col_name in enumerate(columns):
                    worksheet.write(row_offset, idx, attrs.get(col_name))
                last_row = worksheet.last_used_row
    
    def write_testresults(self):
        columns = ["cycle", "cvus", "thread", "suite", "name", "time", "result",
                   "steps", "duration", "connection_duration", "requests",
                   "pages", "xmlrpc", "redirects", "images", "links",]
        for ws_name, results_attrs in self._testResults.items():
            worksheet = self._getWorksheet(ws_name)
            row_offset = worksheet.last_used_row +2
            self._writeHeaders(worksheet, row_offset, columns)
            for attrs in results_attrs:
                for row_idx, col_name in enumerate(columns):
                    print 'Writing testResult %s to worksheet %s' % (row_idx+1, ws_name)
                    worksheet.write(row_offset+1, row_idx, attrs.get(col_name))

    def _worksheetName(self, localname, attrs):
        if localname in ['funkload', 'config']:
            return 'main'
        elif localname in ['response', 'testResult']:
            return 'cycle%(cycle)s cvus%(cvus)s thread%(thread)s' % attrs

    def _getWorksheet(self, name):
        ws = self._sheets.get(name)
        if ws is None:
            ws = self._workbook.add_sheet(name)
            self._sheets[name] = ws
        return ws

    def _getAttrs(self, attributes):    
        attrs = {}
        for name in attributes.getQNames():
            attrs[name] = attributes.getValueByQName(name)
        return attrs

    def _getConfigAttrs(self, attributes):
        attrs = {}
        for name in attributes.getQNames():
            if name == 'key':
                attrs[attributes.getValueByQName(name)] = ''
            if name == 'value':
                attrs[attrs.keys()[0]] = attributes.getValueByQName(name)
        return attrs

    def _writeHeaders(self, worksheet, row, columns):
        for idx, col_name in enumerate(columns):
            worksheet.write(row, idx, col_name)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Supply the input and output file.'
        sys.exit(1)

    criteria = dict([(c.split('=')[0], c.split('=')[1]) for c in sys.argv[3:]])

    tree = etree.parse(sys.argv[1])
    with open(sys.argv[2], 'wb') as outfile:
        workbook = Workbook()

        handler = MyContentHandler(workbook)
        lxml.sax.saxify(tree, handler)
        handler.write_root()
        handler.write_config()
        handler.write_responses()
        handler.write_testresults()

        workbook.save(outfile)
        workbook.save(TemporaryFile())
