##################################################################################
#    Copyright (c) 2009 Novell, All rights reserved.
#    Portions copyright 2009 Massachusetts Institute of Technology, All rights reserved.
#                                                                                 
#    This program is free software; you can redistribute it and/or modify         
#    it under the terms of the GNU General Public License as published by         
#    the Free Software Foundation; either version 2 of the License, or            
#    (at your option) any later version.                                          
#                                                                                 
#    This program is distributed in the hope that it will be useful,              
#    but WITHOUT ANY WARRANTY; without even the implied warranty of               
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                
#    GNU General Public License for more details.                                 
#                                                                                 
#    You should have received a copy of the GNU General Public License            
#    along with this program; if not, write to the Free Software                  
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    
#                                                                                 
##################################################################################

__author__  = '''Brent Lambert, David Ray, Jon Thomas'''
__version__   = '$ Revision 0.0 $'[11:-2]


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
