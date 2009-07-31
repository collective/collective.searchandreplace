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

from AccessControl import ModuleSecurityInfo
import logging
import sys

logger = logging.getLogger("getSearchandReplace")
security = ModuleSecurityInfo('collective.searchandreplace.getSearchandReplaceFiles')

security.declarePublic('getFiles')
def getFiles(batch):
    
    lists = {}
    for o in batch:
        lists[o.getURL()] = o
        #logger.info("URL is %s" % str(o.getURL())) 
    batch = lists.values()
    #logger.info("list length is %d" % len(batch)) 
    from Products.CMFPlone import Batch
    batch = Batch(batch, sys.maxint, 0, orphan=0)
    return batch

