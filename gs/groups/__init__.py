# coding=utf-8
from AccessControl import ModuleSecurityInfo
from AccessControl import allow_class

groupsInfo_security = ModuleSecurityInfo('gs.groups.groupsInfo')
from groupsInfo import GSGroupsInfoFactory, GSGroupsInfo
allow_class(GSGroupsInfoFactory)
allow_class(GSGroupsInfo)

# --=mpj17=-- Do not import allgroups, because it is too general
from public import PublicGroups
from private import PrivateGroups
from secret import SecretGroups
