""" zctl script to create test users
"""
import sys
import datetime
import transaction
import string
from random import choice
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.utils import getToolByName

from zope.app.component.hooks import setSite

try:
    portal_id = sys.argv[1]
except IndexError:
    portal_id = 'Plone' 

if not app.hasObject(portal_id):
    print "Please specify the id of your plone site as the first argument "
    print "to this script."
    print "Usage: <instancehome>/bin/instance run %s <id>" % sys.argv[0]
    sys.exit(1)


start = datetime.datetime.now()
print 'Starting at:%s' % start.strftime('%H:%M:%S:%s')

app = makerequest.makerequest(app)
portal = app[portal_id]
setSite(portal)

# we assume there is an admin user
user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))

mst = getToolByName(portal, 'portal_membership')
userids = mst.listMemberIds()
auth = portal.acl_users.credentials_cookie_auth
ac_name = getattr(auth, 'name_cookie', '__ac_name')
ac_password = getattr(auth, 'pw_cookie', '__ac_password')
pw = '12345'
roles = ('Member',)
domains = None
pr = portal.portal_registration
acl_users = getToolByName(portal, "acl_users")

for i in range(1000000):
    username = 'funkload_testuser_%s' % i

    # print in the format required by the credential server
    print "%s:%s" % (username, pw)

    if username in userids:
        user = acl_users.getUserById(username)
        if hasattr(user, 'changePassword'):
            user.changePassword(pw)
        else:
            acl_users._doChangeUser(username, pw, roles, domains)
    else:
        member = pr.addMember(username, pw, roles,
                              properties={'username': username,
                                          'email': 'devnull@upfrontsystems.co.za'})

        app.REQUEST[ac_name] = username
        app.REQUEST[ac_password] = pw
        mst.loginUser(REQUEST=app.REQUEST)
        mst.logoutUser(REQUEST=app.REQUEST)
    
    # commit every 10000 transactions
    if not i % 10000:
        transaction.commit()

transaction.commit()
end = datetime.datetime.now()
print 'Done at:%s' % end.strftime('%H:%M:%S:%s')
print 'Elapsed time=%s seconds.' % (end-start).seconds
