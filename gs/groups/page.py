# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from Products.Five import BrowserView
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
import AccessControl
from Products.GSGroup.interfaces import IGSGroupInfo
from gs.group.privacy.groupprivacycontentprovider import Views


class GroupsPage(BrowserView):
    def __init__(self, groups, request):
        BrowserView.__init__(self, groups, request)
        self.siteInfo = createObject('groupserver.SiteInfo', groups)
        self.groupsInfo = createObject('groupserver.GroupsInfo', groups)
        self.userInfo = createObject('groupserver.LoggedInUser', groups)

    @Lazy
    def categories(self):
        categories = self.groupsInfo.groupsObj.getProperty('categories', [])

        return categories

    def ordered_categories(self, allcategories):
        out_categories = []
        # if we have a categories property, we sort by those first, then alpha
        for category in self.categories:
            if category in allcategories:
                allcategories.remove(category)
                out_categories.append(category)

        allcategories.sort()
        out_categories += allcategories

        return out_categories

    @Lazy
    def joinable_groups_by_category(self):
        groupsByCategory = {}
        groups = self.joinable_groups
        for group in groups:
            category = group.groupObj.getProperty('category', 'other')
            if groupsByCategory.has_key(category):
                groupsByCategory[category].append(group)
            else:
                groupsByCategory[category] = [group]

        return groupsByCategory

    @Lazy
    def joinable_groups(self):
        u = self.loggedInUser.user
        groups = map(IGSGroupInfo,
                    self.groupsInfo.get_joinable_groups_for_user(u))
        return groups

    @Lazy
    def member_groups_by_category(self):
        groupsByCategory = {}
        groups = self.member_groups
        for group in groups:
            category = group.groupObj.getProperty('category', 'other')
            if groupsByCategory.has_key(category):
                groupsByCategory[category].append(group)
            else:
                groupsByCategory[category] = [group]

        return groupsByCategory

    @Lazy
    def member_groups(self):
        user = AccessControl.getSecurityManager().getUser()
        groups = map(IGSGroupInfo,
                    self.groupsInfo.get_member_groups_for_user(user, user))
        return groups

    @Lazy
    def loggedInUser(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        assert retval
        return retval

    @Lazy
    def privateGroups(self):
        # TODO: create an entirely new groups info that does not sux.
        #   See the comment by AM in groupsInfo.GSGroupsInfo for more.
        allGroups = self.groupsInfo.get_all_groups()
        jgIds = [g.id for g in self.joinable_groups]
        mgrps = [g.id for g in self.member_groups]
        securityManager = AccessControl.getSecurityManager()
        retval = [IGSGroupInfo(g) for g in allGroups if
                    securityManager.checkPermission('View', g)
                    and Views(g).anon
                    and (g.getId() not in jgIds)
                    and (g.getId() not in mgrps)]
        return retval

    @Lazy
    def secretGroups(self):
        allGroups = self.groupsInfo.get_all_groups()
        jgIds = [g.id for g in self.joinable_groups]
        mgrps = [g.id for g in self.member_groups]
        securityManager = AccessControl.getSecurityManager()
        retval = [IGSGroupInfo(g) for g in allGroups if
                    securityManager.checkPermission('View', g)
                    and not(Views(g).anon)  # Different from private
                    and (g.getId() not in jgIds)
                    and (g.getId() not in mgrps)]
        return retval
