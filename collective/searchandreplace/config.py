##################################################################################
#    Copyright (c) 2009 Novell, All rights reserved.
#    Portions copyright 2009 Massachusetts Institute of Technology, All rights reserved.
#                                                                                 
#    This program is free software; you can redistribute it and/or modify         
#    it under the terms of the GNU General Public License as published by         
#    the Free Software Foundation, version 2.                                      
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
