#
# Product configuration. This contents of this module will be imported into
# __init__.py and every content type module.
#
# If you wish to perform custom configuration, you may put a file AppConfig.py
# in your product's root directory. This will be included in this file if
# found.
#
from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "SearchAndReplace"
EXTENSION_PROFILES = ('collective.searchandreplace:default', )
SKIN_DIR = 'skins'
TOOL_ICON = 'tool.gif'
TOOL_PORTAL_NAME = 'Search And Replace Tool'
TOOL_NAME = 'portal_search_and_replace'
TOOL_VERSION = 1



# Leave True if searches and folders should filter using geographies

DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Member'))

product_globals=globals()

##code-section config-bottom #fill in your manual code here
##/code-section config-bottom


try:
    from collective.searchandreplace.AppConfig import *
except ImportError:
    pass

# End of config.py
