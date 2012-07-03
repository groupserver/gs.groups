# coding=utf-8
from zope.contentprovider.interfaces import IContentProvider
from zope.interface.interface import Interface
from zope.schema import List, Text
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

class IGroupListContentProvider(IContentProvider):
    groups = List(title=u'Groups',
                  description=u'The groups to list.',
                  required=True)
    pageTemplateFileName = Text(title=u"Page Template File Name",
                                description=u'The name of the ZPT file that '\
                                    u'is used to render the list.',
                                required=False,
                                default=u"browser/templates/groupslistcontentprovider.pt")
