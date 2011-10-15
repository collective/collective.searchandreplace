# -*- coding: us-ascii -*-
# _______________________________________________________________________
#              __________                      .__        
#   ____   ____\______   \____________  ___  __|__| ______
# _/ __ \ /    \|     ___/\_  __ \__  \ \  \/  /  |/  ___/
# \  ___/|   |  \    |     |  | \// __ \_>    <|  |\___ \ 
#  \___  >___|  /____|     |__|  (____  /__/\_ \__/____  >
#      \/     \/                      \/      \/       \/ 
# _______________________________________________________________________
# 
#    This file is part of the eduCommons software package.
#
#    Copyright (c) 2011 enPraxis, LLC
#    http://enpraxis.net
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2.8  
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 
# _______________________________________________________________________

__author__ = 'Brent Lambert <brent@enpraxis.net>'
__version__ = '$ Revision 0.0 $'[11:-2]

from zope.publisher.browser import BrowserView
from zope.component import getUtility
from collective.searchandreplace.interfaces import ISearchReplaceUtility


class SearchReplaceTable(BrowserView):
    """ View class for search and replace preivew table widget."""

    def getItems(self):
        """ Get preview items """
        # Set search parameters
        srutil = getUtility(ISearchReplaceUtility)
        stext = None
        if self.request.has_key('form.findWhat'):
            stext = self.request['form.findWhat']
        if not stext:
            return []
        if self.request.has_key('form.searchSubfolders'):
            subfolders = True
        else:
            subfolders = False
        if self.request.has_key('form.matchCase'):
            mcase = True
        else:
            mcase = False
        # Get search results
        results =  srutil.searchObjects(
            self.context,
            stext,
            searchSubFolders=subfolders,
            matchCase=mcase)
        return results

    def getRelativePath(self, path):
        """ Get a relative path """
        cpath = '/'.join(self.context.getPhysicalPath())
        rpath = path[len(cpath):]
        if rpath:
            rpath = '.' + rpath
        else:
            rpath = './'
        return rpath
            
