# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.interface.common.mapping import IEnumerableMapping
from zope.interface import implements
from zope.schema.interfaces import IVocabulary, IVocabularyTokenized
from zope.schema.vocabulary import SimpleTerm
from gs.group.base.interfaces import IGSGroupMarker

FOLDER_TYPES = ('Folder', 'Folder (Ordered)')


# --=mpj17=-- This deliberately has an awkward name so people are less
# likely to use it
class AllGroupsOnSite(object):
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

    def get_all_groups(self):
        retval = [createObject('groupserver.GroupInfo', g)
                  for g in self.groupsFolder.objectValues(FOLDER_TYPES)
                  if IGSGroupMarker.providedBy(g)]
        return retval

    @Lazy
    def groups(self):
        return self.get_all_groups()

    @Lazy
    def groupIds(self):
        retval = [g.id for g in self.groups]
        assert len(retval) == len(self.groups)
        return retval

    @Lazy
    def groupDict(self):
        retval = dict([(g.id, g) for g in self.groups])
        return retval

    def __len__(self):
        return len(self.groups)

    def __iter__(self):
        return iter(self.groups)

    def __contains__(self, group):
        assert group, 'No group given'
        retval = ((group in self.groupIds) or (group in self.groups))
        return retval

    def __getitem__(self, key):
        retval = self.groupDict[key]
        return retval


class AllGroupsOnSiteVocab(AllGroupsOnSite):
    implements(IVocabulary, IVocabularyTokenized)
    __used_for__ = IEnumerableMapping

    def make_term(self, groupInfo):
        retval = SimpleTerm(groupInfo.id, groupInfo.id, groupInfo.name)
        return retval

    def __iter__(self):
        r = [self.make_term(g) for g in self.groups]
        retval = iter(r)
        return retval

    def __contains__(self, groupId):
        assert groupId, 'No groupId given'
        retval = (groupId in self.groupIds)
        return retval

    @Lazy
    def termDict(self):
        retval = dict([(g.id, self.make_term(g)) for g in self.groups])
        return retval

    def __getitem__(self, key):
        retval = self.termDict[key]
        return retval

    def getTerm(self, value):
        return self[value]

    def getTermByToken(self, value):
        return self[value]
