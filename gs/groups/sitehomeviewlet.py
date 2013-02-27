# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.viewlet.viewlet import SiteViewlet
from allgroups import AllGroupsOnSite
from membergroups import PublicGroups, PrivateGroups, SecretGroups


class ListVisible(SiteViewlet):

    @Lazy
    def allGroups(self):
        retval = AllGroupsOnSite(self.context)
        return retval

    @Lazy
    def publicGroups(self):
        return PublicGroups(self.context, self.allGroups.groups)

    @Lazy
    def privateGroups(self):
        return PrivateGroups(self.context, self.allGroups.groups)

    @Lazy
    def visiblePublic(self):
        return (len(self.publicGroups) > 0)

    @Lazy
    def visiblePrivate(self):
        return (len(self.privateGroups) > 0)

    @Lazy
    def show(self):
        retval = (self.visiblePublic or self.visiblePrivate)
        return retval


class NoListVisible(ListVisible):

    @Lazy
    def show(self):
        retval = (not(self.visiblePublic and self.visiblePrivate) and
                  self.loggedInUser.anonymous)
        return retval


class ListSecret(ListVisible):
    @Lazy
    def secretGroups(self):
        return SecretGroups(self.context, self.allGroups.groups)

    @Lazy
    def show(self):
        retval = self.loggedInUser.anonymous or (len(self.secretGroups) > 0)
        return retval
