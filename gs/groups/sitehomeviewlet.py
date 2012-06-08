# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.viewlet.viewlet import SiteViewlet
from private import PrivateGroups

class GroupsList(SiteViewlet):
    @Lazy
    def privateGroups(self):
        return PrivateGroups(self.context)
