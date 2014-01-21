# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import
from zope.cachedescriptors.property import Lazy
from gs.viewlet.viewlet import SiteViewlet
from .allgroups import AllGroupsOnSite
from .membergroups import PublicGroups, PrivateGroups, SecretGroups


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
    def isSiteAdmin(self):
        adminIds = [a.id for a in self.siteInfo.site_admins]
        retval = ((not self.loggedInUser.anonymous)
                    and (self.loggedInUser.id in adminIds))
        return retval

    @Lazy
    def secretGroups(self):
        return SecretGroups(self.context, self.allGroups.groups)

    @Lazy
    def memberGroups(self):
        retval = [g for g in self.secretGroups if g.member]
        return retval

    @Lazy
    def show(self):
        # --=mpj17=-- Bare with me, this is a little tricky.
        # The *site* administrator should see all the secret groups, so he or
        #     she can administer them
        # A *member* of a secret group should see the group, but only that
        #     group.
        # The list of secret groups should be hidden from everyone else.
        #
        # This property determines if the list should be seen *at* *all*. The
        # page template for the viewlet determines *what* is seen.
        retval = ((self.isSiteAdmin and (len(self.secretGroups) > 0))
                or ((not self.isSiteAdmin) and (len(self.memberGroups) > 0)))
        return retval
