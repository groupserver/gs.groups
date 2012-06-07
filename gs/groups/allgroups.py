# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.schema.interfaces import IVocabulary, IVocabularyTokenized, \
    ITitledTokenizedTerm
from zope.interface.common.mapping import IEnumerableMapping 

class AllGroupsOnSite(object):
    implements(IVocabulary, IVocabularyTokenized)
    __used_for__ = IEnumerableMapping

    def __init__(self, context):
        self.context = context

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)        
        return retval

    @Lazy
    def groupsFolder(self):
        retval = getattr(self.siteInfo.siteObj, 'groups', None)
        assert retval, 'Cannot find "groups" folder in %s' % \
            self.siteInfo.siteObj
        return retval
