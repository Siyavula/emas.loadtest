import datetime
import transaction
from five import grok
from zope.interface import Interface
from zope.component import queryUtility

from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from emas.theme.interfaces import IEmasServiceCost

grok.templatedir('templates')

class CreateUsers(grok.View):
    """ Create a whole lot of users.
    """
    
    grok.context(Interface)
    grok.require('zope2.View')

    def __call__(self):
        import pdb;pdb.set_trace()
        start = datetime.datetime.now()
        print 'Starting at:%s' % start.strftime('%H:%M:%S:%s')
        portal = self.context.restrictedTraverse('@@plone_portal_state').portal()
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
        prefix = self.request.get('prefix', 'funkload_testuser')
        start = self.request.get('start', 0)
        numofusers = self.request.get('numofusers', 50)

        for i in range(start, start+numofusers):
            username = '%s_%s' % (prefix, i)

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

                self.request[ac_name] = username
                self.request[ac_password] = pw
                mst.loginUser(REQUEST=self.request)
                mst.logoutUser(REQUEST=self.request)
            
            # commit every 10000 transactions
            if not i % 10000:
                transaction.commit()

        transaction.commit()
        end = datetime.datetime.now()
        print 'Done at:%s' % end.strftime('%H:%M:%S:%s')
        print 'Elapsed time=%s seconds.' % (end-start).seconds

    def render(self):
        return ''
