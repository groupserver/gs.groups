# coding=utf-8
from zope.interface.interface import Interface
from zope.viewlet.interfaces import IViewletManager

class IGSGroupsInfo(Interface):
    def get_visible_group_ids(): #@NoSelf
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
