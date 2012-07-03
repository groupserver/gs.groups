Introduction
============

This module is concerned with the "groups" area of a site: the collection
of all the groups.


Lists
=====

The lists are viewlets, which appear in the
``gs.groups.interfaces.IGroupList`` manager. This manager, in turn, appears
in the left-hand column of the site homepage (in the manager
``gs.site.home.interfaces.ISiteHomeLeftColumn``).

This product provides three group-list viewlets:

* The visible groups include the public and private groups, each separated
  out into a different list.

* If there are no visible groups, and the person is logged out then advice
  is given to login.

* Finally, the site-administrator is shown a list of secret groups.
