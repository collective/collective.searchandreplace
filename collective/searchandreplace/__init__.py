#
# Initialise the product's module. There are three ways to inject custom code
# here:
#
#   - To set global configuration variables, create a file AppConfig.py. This
#       will be imported in config.py, which in turn is imported in each
#       generated class and in this file.
#   - To perform custom initialisation after types have been registered, use
#       the protected code section at the bottom of initialize().
#   - To register a customisation policy, create a file CustomizationPolicy.py
#       with a method register(context) to register the policy
#

import logging

LOG = logging.getLogger("__init__.py")

try:
    import CustomizationPolicy
except ImportError:
    CustomizationPolicy=None

from Globals import package_home
from AccessControl import allow_module
from Products.CMFCore import utils, DirectoryView
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore import permissions as CMFCorePermissions
from Products.CMFCore.utils import ToolInit
from collective.searchandreplace.config import PROJECTNAME

import os, os.path

from config import *

from Products.CMFCore.utils import getToolByName

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/SearchAndReplace',
                                    product_globals)

##code-section custom-init-head #fill in your manual code here
##/code-section custom-init-head

# Apply monkey patches
import patches

# Add permissions
import permissions

ADD_CONTENT_PERMISSIONS = 'Manage Portal'
GLOBALS = globals()
registerDirectory('skins', GLOBALS)

allow_module('collective.searchandreplace.getSearchandReplaceFiles')

PKG_NAME = 'SearchAndReplace'

from collective.searchandreplace.SearchAndReplaceTool import SearchAndReplaceTool
from Products.Archetypes.ClassGen import generateMethods

tools = (SearchAndReplaceTool,)

def initialize(context):
    ##code-section custom-init-top #fill in your manual code here
    ##/code-section custom-init-top

    # imports packages and types for registration

    # initialize portal content
    
    ToolInit('Search And Replace Tool',
             tools=tools,
             icon='tool.gif',
    ).initialize(context)
    


