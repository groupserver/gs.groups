# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.privacy.visibility import GroupVisibility
from gs.group.member.base.utils import user_member_of_group
from allgroups import AllGroupsOnSite


class SecretGroups(AllGroupsOnSite):
    # --=mpj17=-- should this be moved to gs.group.member.base?

    @Lazy
    def loggedInUser(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        return retval

    @Lazy
    def groups(self):
        retval = []
        for g in self.get_all_groups():
            if GroupVisibility(g).isSecret:
                g.member = user_member_of_group(self.loggedInUser, g)
                retval.append(g)
        return retval
