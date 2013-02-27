# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.group.privacy.visibility import GroupVisibility
from allgroups import AllGroupsOnSite


class PrivateGroups(AllGroupsOnSite):

    @Lazy
    def groups(self):
        retval = [g for g in self.get_all_groups()
                  if GroupVisibility(g).isPrivate]
        return retval

