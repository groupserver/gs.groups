# This space intentionally left blank
import groupsInfo
from AccessControl import ModuleSecurityInfo
from AccessControl import allow_class

groupsInfo_security = ModuleSecurityInfo('gs.groups.groupsInfo')
from groupsInfo import GSGroupsInfoFactory, GSGroupsInfo
allow_class(GSGroupsInfoFactory)
allow_class(GSGroupsInfo)
