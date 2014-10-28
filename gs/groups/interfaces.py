# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals
from zope.contentprovider.interfaces import IContentProvider
from zope.interface.interface import Interface
from zope.schema import List, Text
from zope.viewlet.interfaces import IViewletManager
from . import GSMessageFactory as _


class IGSGroupsInfo(Interface):
    def get_visible_group_ids():  # lint:ok
        """Get the IDs of Visible Groups

        ARGUMENTS
            None.

        RETURNS
            A list of strings, representing the IDs of visible groups.
        """


class IGSGroupsFolder(Interface):
    pass


class IGroupList(IViewletManager):
    '''The lists of groups on the site.'''


class IGroupListContentProvider(IContentProvider):
    groups = List(title=_('Groups'),
                  description='The groups to list.',
                  required=True)
    pageTemplateFileName = Text(
        title="Page Template File Name",
        description='The name of the ZPT file that  is used to render the '
                    'list.',
        required=False,
        default="browser/templates/groupslistcontentprovider.pt")
