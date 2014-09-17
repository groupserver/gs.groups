=============
``gs.groups``
=============
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The list of groups on a site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-01-21
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

This module is concerned with the "groups" area of a site: the collection
of all the groups.

Lists
=====

The lists are viewlets, which appear in the
``gs.groups.interfaces.IGroupList`` manager. This manager, in turn, appears
in the main column of the site homepage (in the manager
``gs.site.home.interfaces.ISiteHomeMain``).

This product provides three group-list viewlets:

* The visible groups include the public and private groups, each separated
  out into a different list.

* If there are no visible groups, and the person is logged out then advice
  is given to login.

* Finally, the list of secret groups is shown. The list is shown to

  + The site administrators, who see **all** the secret groups, and
  + The members of the secret groups, who see **just** the secret groups
    that they are members of.

The ``groupserver.GroupListContent`` content provider displays the actual
list of groups.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.groups
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

..  LocalWords:  ISiteHomeMain groupserver GroupListContent nz
