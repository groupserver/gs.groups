# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.viewlet.viewlet import SiteViewlet
from public import PublicGroups
from private import PrivateGroups
from secret import SecretGroups

class ListVisible(SiteViewlet):
    @Lazy
    def privateGroups(self):
        return PrivateGroups(self.context)
    
    @Lazy
    def publicGroups(self):
        return PublicGroups(self.context)

class ListSecret(SiteViewlet):
    @Lazy
    def secretGroups(self):
        return SecretGroups(self.context)
