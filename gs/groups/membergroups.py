# -*- coding: utf-8 -*-
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.privacy.visibility import GroupVisibility
from gs.group.member.base.utils import user_member_of_group


class MemberGroups(object):

    def __init__(self, context, groups):
        self.context = context
        self.origGroups = groups

    @Lazy
    def loggedInUser(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        return retval


class PublicGroups(MemberGroups):
    # --=mpj17=-- should this be moved to gs.group.member.base?

    @Lazy
    def groups(self):
        retval = []
        for g in self.origGroups:
            if GroupVisibility(g).isPublic:
                g.member = user_member_of_group(self.loggedInUser, g)
                retval.append(g)
        return retval

    def __len__(self):
        return len(self.groups)

    def __iter__(self):
        return iter(self.groups)


class PrivateGroups(MemberGroups):
    # --=mpj17=-- should this be moved to gs.group.member.base?

    @Lazy
    def groups(self):
        retval = []
        for g in self.origGroups:
            if GroupVisibility(g).isPrivate:
                g.member = user_member_of_group(self.loggedInUser, g)
                retval.append(g)
        return retval

    def __len__(self):
        return len(self.groups)

    def __iter__(self):
        return iter(self.groups)


class SecretGroups(MemberGroups):
    # --=mpj17=-- should this be moved to gs.group.member.base?

    @Lazy
    def groups(self):
        retval = []
        for g in self.origGroups:
            if GroupVisibility(g).isSecret:
                g.member = user_member_of_group(self.loggedInUser, g)
                retval.append(g)
        return retval

    def __len__(self):
        return len(self.groups)

    def __iter__(self):
        return iter(self.groups)
