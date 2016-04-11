# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
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
from mock import MagicMock, patch, PropertyMock
from unittest import TestCase
from gs.groups.allgroups import (AllGroupsOnSite, AllGroupsOnSiteVocab, )


def create_group(gId, name=''):
    g = MagicMock(spec=['id', 'name'])
    g.id = gId
    g.name = name
    return g


class TestAllGroupsOnSite(TestCase):

    @patch.object(AllGroupsOnSite, 'groups', new_callable=PropertyMock)
    def test_groupDict(self, mock_groups):
        groups = [create_group(i) for i in 'abcde']
        mock_groups.return_value = groups

        a = AllGroupsOnSite(MagicMock())
        r = a.groupDict

        self.assertEqual(len(groups), len(r))
        self.assertEqual('abcde', ''.join(sorted(list(r.keys()))))

    @patch.object(AllGroupsOnSite, 'groups', new_callable=PropertyMock)
    def test_len(self, mock_groups):
        groups = [create_group(i) for i in 'abcde']
        mock_groups.return_value = groups

        a = AllGroupsOnSite(MagicMock())
        r = len(a)

        self.assertEqual(5, r)

    @patch.object(AllGroupsOnSite, 'groups', new_callable=PropertyMock)
    def test_in_id(self, mock_groups):
        'Test __contains__ with an ID'
        groups = [create_group(i) for i in 'abcde']
        mock_groups.return_value = groups

        a = AllGroupsOnSite(MagicMock())
        r = 'c' in a

        self.assertTrue(r)

    @patch.object(AllGroupsOnSite, 'groups', new_callable=PropertyMock)
    def test_in_group(self, mock_groups):
        'Test __contains__ with a group'
        groups = [create_group(i) for i in 'abcde']
        mock_groups.return_value = groups

        a = AllGroupsOnSite(MagicMock())
        r = groups[2] in a

        self.assertTrue(r)

    @patch.object(AllGroupsOnSite, 'groups', new_callable=PropertyMock)
    def test_not_in_id(self, mock_groups):
        'Test __contains__ with an ID'
        groups = [create_group(i) for i in 'abcde']
        mock_groups.return_value = groups

        a = AllGroupsOnSite(MagicMock())
        r = 'w' in a

        self.assertFalse(r)

    @patch.object(AllGroupsOnSite, 'groups', new_callable=PropertyMock)
    def test_not_in_group(self, mock_groups):
        'Test __contains__ with a group'
        groups = [create_group(i) for i in 'abcde']
        mock_groups.return_value = groups

        a = AllGroupsOnSite(MagicMock())
        r = create_group('w') in a

        self.assertFalse(r)

    @patch.object(AllGroupsOnSite, 'groups', new_callable=PropertyMock)
    def test_getItem(self, mock_groups):
        'Test __getItem__ with a group'
        groups = [create_group(i) for i in 'abcde']
        mock_groups.return_value = groups

        a = AllGroupsOnSite(MagicMock())
        r = a['c']

        self.assertEqual(groups[2], r)


class TestAllGroupsOnSiteVocab(TestCase):
    def test_make_term(self):
        v = AllGroupsOnSiteVocab(MagicMock())
        g = create_group('frog', 'Frog')
        r = v.make_term(g)

        self.assertEqual('Frog', r.title)
        self.assertEqual('frog', r.token)
        self.assertEqual('frog', r.value)

    @patch.object(AllGroupsOnSiteVocab, 'groups', new_callable=PropertyMock)
    def test_termDict(self, mock_groups):
        groups = [create_group(i, i.upper()) for i in 'abcde']
        mock_groups.return_value = groups
        v = AllGroupsOnSiteVocab(MagicMock())
        r = v.termDict

        self.assertEqual('c', r['c'].token)
        self.assertEqual('C', r['c'].title)
