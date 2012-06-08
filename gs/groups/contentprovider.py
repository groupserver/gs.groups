# coding=utf-8
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.app.pagetemplate import ViewPageTemplateFile
from gs.viewlet.contentprovider import SiteContentProvider

class GroupsListContentProvider(SiteContentProvider):
    def update(self):
        self.__updated=True

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled
        pageTemplate = ViewPageTemplateFile(self.pageTemplateFileName)
        return pageTemplate(self)
