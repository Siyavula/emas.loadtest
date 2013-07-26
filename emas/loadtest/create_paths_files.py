""" Script to create the paths files our test cases need.
"""
import sys
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName

from zope.app.component.hooks import setSite

try:
    portal_id = sys.argv[1]
except IndexError:
    portal_id = 'Plone' 

try:
    subject = sys.argv[2]
except IndexError:
    subject = None

try:
    grade = sys.argv[3]
except IndexError:
    grade = None

if not app.hasObject(portal_id):
    print "Please specify the id of your plone site as the first argument "
    print "to this script."
    print "Usage: <instancehome>/bin/instance run %s <id>" % sys.argv[0]
    sys.exit(1)


app = makerequest.makerequest(app)
portal = app[portal_id]
setSite(portal)

# we assume there is an admin user
user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))

paths = []
pc = getToolByName(portal, 'portal_catalog')
if grade and subject:
    search_path = '/'.join([portal_id, subject, grade])
elif subject:
    search_path = '/'.join([portal_id, subject])
else:
    search_path = '/'.join([portal_id])
    
query = {'portal_type': 'rhaptos.xmlfile.xmlfile',
         'path': search_path,
         'review_state': 'published'}
brains = pc(query)

for count, brain in enumerate(brains):
    print count
    path = brain.getPath()
    paths.append(path.lstrip('/'.join(['', portal_id, subject, ''])))

filename = '%s_paths.txt' % search_path.replace('/', '-').lstrip('-')
paths_file = open(filename, 'wb')
paths_file.write('\n'.join(paths))
paths_file.close()
