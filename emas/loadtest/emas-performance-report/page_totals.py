#!python

import sys
from xml.dom.minidom import parseString

"""
data example:
<response cycle="000" cvus="100" thread="057" suite="Practice"
    name="test_practice" step="001" number="011" type="link" result="Successful"
    url="/" code="200" description=""
    time="1377252663.41" duration="0.432377099991" />

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


NAMES = [
    'cycle',
    'cvus',
    'thread',
    'suite',
    'name',
    'step',
    'number',
    'type',
    'result',
    'url',
    'code',
    'description',
    'time',
    'duration',]


class Response(object):
    
    def __init__(self, element=None, kwargs={}):
        self.xml = None
        if element:
            self.xml = element.toxml()
            for name in NAMES:
                value = element.getAttribute(name)
                setattr(self, name, value)
        for name, value in kwargs.items():
            setattr(self, name, value)
    
    def __repr__(self):
        representation = []
        for name in NAMES:
            value = getattr(self, name, '')
            representation.append(value) 
        return ','.join(representation) + '\n'
    
    def __eq__(self, other):
        for name in NAMES:
            other_val = getattr(other, name, '')
            if other_val:
                self_val = getattr(self, name, '')
                if self_val != other_val:
                    return False
        return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Supply the input and output file.'
        sys.exit(1)

    criteria = dict([(c.split('=')[0], c.split('=')[1]) for c in sys.argv[3:]])
    other = Response(None, criteria)

    with open(sys.argv[1], 'rb') as xml:
        dom = parseString(xml.read())
        elements = dom.getElementsByTagName('response')
        with open(sys.argv[2], 'wb') as outfile:
            # write some headings
            outfile.write(','.join(NAMES) + '\n')
            # now write the data 
            for idx, element in enumerate(elements):
                print 'Processing element %s of %s' % (idx+1, len(elements))
                response = Response(element)
                if response == other:
                    outfile.write(response.__repr__())

