from zope.interface import implements, implementedBy
from zope.component import adapts
from zope.app.folder.interfaces import IFolder
from zope.component.interfaces import IFactory

import AccessControl

from Products.GSGroup.queries import GroupQuery
from Products.XWFCore.cache import LRUCache
from Products.XWFCore.XWFUtils import get_group_by_siteId_and_groupId
from Products.CustomUserFolder.interfaces import ICustomUser
from Products.GSContent.interfaces import IGSSiteInfo
from gs.groups.interfaces import IGSGroupsInfo

import time
import logging
log = logging.getLogger('GSGroupsInfo')

class GSGroupsInfoFactory(object):
    implements(IFactory)
    
    title = u'GroupServer Groups Info Factory'
    descripton = u'Create a new GroupServer groups information instance'
    
    def __call__(self, context):
        retval = GSGroupsInfo(context)
        return retval
        
    def getInterfaces(self):
        retval = implementedBy(GSGroupsInfo)
        assert retval
        return retval

class GSGroupsInfo(object):
    implements( IGSGroupsInfo )
    adapts(IFolder)

    siteUserVisibleGroupsIds = LRUCache("siteUserVisibleGroupIds")
    siteUserVisibleGroupsIds.set_max_objects(256)

    def __init__(self, context):
        self.context=context
        self.siteInfo = IGSSiteInfo(context)
        self.groupsObj = self.__get_groups_object()
        
        self.folderTypes = ['Folder', 'Folder (Ordered)']

        self.da = context.zsqlalchemy
        self.groupQuery = GroupQuery(context, self.da)
        self.__allGroups = None
                
    def __get_groups_object(self):
        assert self.siteInfo, 'Site Info is set to %s' % self.siteInfo
        assert self.siteInfo.siteObj, \
          'Site Object is %s' % self.siteInfo.siteObj
        
        assert hasattr(self.siteInfo.siteObj, 'groups'), \
          'Site "%s" has not "groups" instance within "Content"' % \
          self.siteInfo.get_name()
        groupsObj = getattr(self.siteInfo.siteObj, 'groups')
        
        assert groupsObj.getProperty('is_groups' , False), \
          'Groups instance for "%s" exists, but the "is_groups" property '\
          'is not True' % self.siteInfo.get_name()
        
        assert groupsObj
        return groupsObj

    def get_all_groups(self):
        assert self.groupsObj
        if self.__allGroups == None:
            self.__allGroups = [g for g in \
                         self.groupsObj.objectValues(self.folderTypes)
                         if g.getProperty('is_group', False)]
            self.__allGroups.sort(groups_sorter)
        retval = self.__allGroups
        assert type(retval) == list
        return retval

    def get_visible_groups(self):
        # get the top level site ID to use with the cache
        site_root = self.context.site_root()
        top_level_site_id = site_root.getId()

        user = AccessControl.getSecurityManager().getUser()
        userId = user.getId()
        groups = '-'.join(user.getGroups())
        key = '-'.join((top_level_site_id, self.siteInfo.id, groups))

        if self.siteUserVisibleGroupsIds.has_key(key):
            visibleGroupsIds = self.siteUserVisibleGroupsIds.get(key)
            visibleGroups = []
            for groupId in visibleGroupsIds:
                try:
                    visibleGroups.append(getattr(self.groupsObj, groupId))
                except:
                    log.warn("trouble adding '%s' to visible groups" % groupId)
        else:
            top = time.time()
            visibleGroups = self.__visible_groups_for_current_user()
            visibleGroupsIds = [group.getId() for group in visibleGroups]
            self.siteUserVisibleGroupsIds.add(key, visibleGroupsIds)
            bottom = time.time()
            log.debug("Generated visible-groups for (%s) on %s (%s) in %.2fms" % 
                      (userId, self.siteInfo.name, self.siteInfo.id, (bottom-top)*1000.0))        
            
        assert self.siteUserVisibleGroupsIds.has_key(key)
        assert type(visibleGroups) == list
        

        return visibleGroups
        
    def __visible_groups_for_current_user(self):
        securityManager = AccessControl.getSecurityManager()
        allGroups = self.get_all_groups()
        # Quite a simple process, really: itterate through all the groups,
        #   checking to see if the "messages" instance is visible.
        visibleGroups = []
        for group in allGroups:
            # AM: "Visible groups" should really be: groups which a user
            #   is a member of, public groups, and private groups. Therefore,
            #   we should only be checking the visibility of the group, not
            #   of the messages. 
            #   A separate method ("visible messages" or similar) should be
            #   used to determine what messages and files should be included
            #   in search results (and in turn, latest topics and files on a 
            #   site homepage) should be shown to users.
            #   **HOWEVER** at this point in time, we do not make a distinction.
            #   Therefore, to preserve security, we define "visible groups"
            #   very restrictively.
            if (hasattr(group, 'messages')
              and securityManager.checkPermission('View', group)
              and securityManager.checkPermission('View', group.aq_explicit.messages)):
                visibleGroups.append(group)
        assert type(visibleGroups) == list
        return visibleGroups
        
    def get_visible_group_ids(self):
        retval = [g.getId() for g in self.get_visible_groups()]
        return retval

    def filter_visible_group_ids(self, gIds):
        visibleGroupIds = self.get_visible_group_ids()
        return [g for g in gIds if (g in visibleGroupIds)]

    def clear_groups_cache(self):
        m = u'Clearing visible-groups cache for %s (%s)' %\
          (self.siteInfo.name, self.siteInfo.id)
        log.info(m)
        self.siteUserVisibleGroupsIds.clear()

    def get_non_member_groups_for_user(self, user):
        '''List the visible groups that the user is not a member of.
        
        WARNING
            Listing the groups that the user is *not* a member of is
            as bad as listing the groups that the user *is* a member of.
        '''
        assert user
        # AM: The following assert prevents us getting the non-member
        #   groups for Anonymous users. This in turn prevents us
        #   getting the joinable groups for Anonymous users.
        #assert ICustomUser.providedBy(user), '%s is not a user' % user
        retval = [g for g in self.get_visible_groups()
                  if ('GroupMember' not in user.getRolesInContext(g))]
        assert type(retval) == list
        return retval
        
    def get_joinable_groups_for_user(self, user):
        assert user
        listManager = self.context.ListManager
        assert listManager
        nonMemberGroups = self.get_non_member_groups_for_user(user)
        retval = [g for g in nonMemberGroups if
                  listManager.get_listProperty(g.getId(), 'subscribe')]
        assert type(retval) == list
        return retval

    def get_joinable_group_ids_for_user(self, user):
        groups = self.get_joinable_groups_for_user(user)
        retval = [g.getId() for g in groups]
        assert type(retval) == list
        return retval

    def get_member_groups_for_user(self, user, authUsr=None):
        """Get a list of all groups that the user is a member of.
        
        ARGUMENTS
            user: A user instance to query.
            authenticatedUser: The instance of the user who is requesting 
                the information.
        
        RETURNS
            A list of groups the user is a member of. If "user" is the
            same as the "authenticatedUser", then the list will be of all
            groups that "user" is a member of. Otherwise only the groups
            that the user is a member of, and has posted to, will be 
            listed.
        
        SIDE EFFECTS
            None.
        """
        assert user
        retval = []
        if (authUsr and (user.getId() == authUsr.getId())):
            retval = self.__get_member_groups_for_user(user)
        else:
            retval = self.__get_visible_member_groups_for_user(user,authUsr)
        assert type(retval) == list
        return retval

    def __get_member_groups_for_user(self, user):
        """Get a list of all groups the user is currently a member of.
        
        WARNING
            Showing group-memberships to the wrong people may result in
            a privacy breach. It is safer to use 
            "get_member_groups_for_user"
            
        ARGUMENTS
            user: A user instance.
            
        RETURNS
            A list of all groups the user is currently a member of.
        
        SIDE EFFECTS
            None.
        """
        assert user
        visibleGroups = self.get_visible_groups()
        retval = [g for g in visibleGroups
                  if 'GroupMember' in user.getRolesInContext(g)]
        assert type(retval) == list
        return retval

    def __get_visible_member_groups_for_user(self, user, authUsr):
        """Get the publicly visible groups that the user is a member of,
           and the private groups that the viewing user (authUsr) is
           also a member of.
        
        ARGUMENTS
            user: A user instance.
            authUsr: The authenticated user (may be None)
            
        RETURNS
            A list of groups that the user is currently a member of, and
            has posted to. (Unless
        
        SIDE EFFECTS
            None.
        """
        assert user
        retval = []
        memberGroups = self.__get_member_groups_for_user(user)
        sId = self.siteInfo.get_id()
        uId = user.getId()
        q = self.groupQuery
        for g in memberGroups:
            if authUsr:
                authUsrRoles = authUsr.getRolesInContext(g)
                if (('GroupMember' in authUsrRoles)
                    or ('GroupAdmin' in authUsrRoles)
                    or ('DivisionAdmin' in authUsrRoles)):
                    retval.append(g)
            else:
                authors = [ar['user_id'] for ar in
                            q.authors_posts_in_group(sId, g.getId())]
                if (uId in authors):
                    retval.append(g)
        assert type(retval) == list
        return retval

def groups_sorter(a, b):
    at = a.title_or_id().lower()
    bt = b.title_or_id().lower()
    if at < bt:
        retval = -1
    elif at == bt:
        retval = 0
    else:
        retval = 1
    return retval

