# coding=utf-8
from Products.Five import BrowserView
from zope.component import createObject

import AccessControl
from Products.GSGroup.interfaces import IGSGroupInfo

class GroupsPage(BrowserView):
    def __init__(self, groups, request):
        BrowserView.__init__(self, groups, request)
        self.siteInfo = createObject('groupserver.SiteInfo', groups)
        self.groupsInfo = createObject('groupserver.GroupsInfo', groups)
        self.userInfo = createObject('groupserver.LoggedInUser', groups)
    
    @property
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
    
    @property
    def visible_groups_by_category(self):
        groupsByCategory = {}
        groups = self.visible_groups
        for group in groups:
            category = group.groupObj.getProperty('category', 'other')
            if groupsByCategory.has_key(category):
                groupsByCategory[category].append(group)
            else:
                groupsByCategory[category] = [group]

        return groupsByCategory

    @property
    def visible_groups(self):
        groups = map(IGSGroupInfo, self.groupsInfo.get_visible_groups())
        
        return groups

    @property
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

    @property
    def member_groups(self):
        user = AccessControl.getSecurityManager().getUser()
        groups = map(IGSGroupInfo, self.groupsInfo.get_member_groups_for_user(user, user))

        return groups
        
