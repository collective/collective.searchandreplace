from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
#from Products.GeoPlone import geo_globals
    
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.Archetypes.Extensions.utils import install_subskin

from Products.ATContentTypes.criteria import _criterionRegistry

from Products.ATContentTypes import criteria
#from Products.GeoPlone.criteria import ATCurrentGeographyCriterion

import logging

LOG = logging.getLogger("AppInstall.py")

try:
    from Products.CMFCore.permissions import ManagePortal
except ImportError:
    from Products.CMFCore.CMFCorePermissions import ManagePortal

def install(self):
    """
    Install method for SearchAndReplace
    """

    LOG.info('AppInstall.py executing')

    out = StringIO()
    #addSearchIndex(self, out)
    #addSmartFolderIndex(self, out);
    install_tools(self, out)
    #install_actions(self, out)
    #install_subskin(self, out, geo_globals)
    #addConfiglets(self, out)
    return out.getvalue()

_globals = globals()

def install_tools(self, out):
    LOG.info('install_tools executing')
#    if not hasattr(self, 'portal_geographies'):
#        LOG.info('no portal_geographies attr')
#        addTool = self.manage_addProduct['GeoPlone'].manage_addTool
#        addTool('Plone Geography Tool')
#        LOG.info('done installing geo tool')

def install_actions(self, out):
    at = getToolByName(self, 'portal_actions')
    at.manage_aproviders('portal_search_and_replace', add_provider=1)

def unregisterActionProvider(self, out):
    actionTool = getToolByName(self, 'portal_actions', None)
#    if actionTool:
#        actionTool.deleteActionProvider('portal_geographies')
#        out.write('Removed action provider\n')

def uninstall(self):
    out=StringIO()
    unregisterActionProvider(self, out)
    #removeConfiglets(self, out)
    return out.getvalue()
