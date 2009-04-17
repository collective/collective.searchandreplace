# This file is Copyright (c) Adesium and was written by Pilot Systems
# It is available under the GNU General Public License version 2.
# See COPYING at the root of the project for the license text.

from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.ActionInformation import ActionInformation
from Globals import  InitializeClass
from OFS.SimpleItem import SimpleItem
from OFS.Folder import Folder, ObjectManager
from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from Products.CMFCore.utils import UniqueObject,SimpleItemWithProperties,getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.Expression import Expression
import os.path, string
from Acquisition import aq_base
from permissions import *
import sys
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter

from PreviewBrain import PreviewBrain

from config import TOOL_NAME, TOOL_PORTAL_NAME, TOOL_VERSION
    
from zope.interface import implements
 
# NLS
import transaction
from Persistence import PersistentMapping
from copy import copy

import os
import sys
import traceback
import re

#import logging
#logger = logging.getLogger("SearchAndReplaceTool")
#logger.info("***********  Inside of search and replace *********")

pathIndexMatcher = re.compile(r'^(.*)\[([\d]+)\]$')

class SearchAndReplaceTool(UniqueObject, Folder):
    """
    Search for and replace strings in plone objects
    """


    id = TOOL_NAME
    portal_type = meta_type = TOOL_PORTAL_NAME
    title = TOOL_PORTAL_NAME
    version = TOOL_VERSION

    security = ClassSecurityInfo()

    manage_options = (
        (Folder.manage_options[0],)
        + Folder.manage_options[2:]
        )


    def __init__(self):
        """
        """
        pass

    #
    # Tool methods
    #

    security.declarePublic('getToolVersion')
    def getToolVersion(self):
        """
        Return the actual tool version.
        """
        return self.version
        
    def isValidRegex(self, text):
        try:
            re.compile(text)
            return True
        except:
            return False
            
    def getBrainsByPaths(self, paths, includeChildren=True, fileExtensions=None, language='all', geo='all'):  
        """ returns a generator which returns each file represented by the given paths.
            Searches recursively if includeChildren is true"""
        catalog = getToolByName(self, 'portal_catalog')
        for path in paths:
            query = {
                'path' : {'query' : path},
            }
            if not includeChildren:
                query['path']['depth'] = 0

            #print "query: %s" % str(query)
            
            for brain in catalog(query):
                #print "should i yield %s?" % brain.id
                if fileExtensions:
                    id = brain.id
                    (file, ext) = os.path.splitext(id)
                    if ext not in fileExtensions:
                        continue
                yield brain
                   
    def getPagesByPaths(self, paths, *args, **kwargs):  
        brains = self.getBrainsByPaths(paths, *args, **kwargs)
        for brain in brains:
            obj = brain.getObject()
#            if hasattr(obj, 'getFile') and callable(obj.getFile):
            if hasattr(obj, 'getText') and callable(obj.getText):
                yield (brain, obj)
                    
    def getFileExtensions(self, paths, *args, **kwargs):
        extensions = []
        brains = self.getBrainsByPaths(self.splitPathsAndIndexes(paths).keys(), *args, **kwargs)
        for brain in brains:
            id = brain.id
            #print "evaluating %s" % id
            (file, ext) = os.path.splitext(id)
            if ext and ext not in extensions:
                extensions.append(ext)
        extensions.sort()
        #print "extensions: %s" % str(extensions)
        return extensions
    
    def splitPathsAndIndexes(self, paths):
        """ if paths were passed in from a preview screen, they will be of the form
            "my/folder/path/file.txt[4]", where the "[4]" indicates that this represents
            the fourth match in file.txt.  We need to split out the 4 (or the "index") from
            the path."""

        pathsAndIndexes = {}
        for path in paths:
            mo = pathIndexMatcher.match(path)
            pathIndex = None
            if mo:
                path = mo.group(1)
                pathIndex = int(mo.group(2))
                if path in pathsAndIndexes:
                    indexList = pathsAndIndexes[path]
                else:
                    indexList = []
                indexList.append(pathIndex)
                pathsAndIndexes[path] = indexList
            else:
                pathsAndIndexes[path] = None
        #print "%s, %s" %(paths, pathsAndIndexes)
        return pathsAndIndexes
        
    def getPageContents(self, obj):
        return str(obj.getText())
    
    def setPageContents(self, obj, contents):
        obj.setText(contents)

    def searchAndReplace(self, request, paths, searchText, replaceField, replaceText, useRegex=True, matchCase=True,
                         includeChildren=True, fileExtensions=None, language='all', geo='all',
                         batch=False,b_size=sys.maxint, preview=False):
        #logger.info("batch = %s preview = %s" % (batch, preview))
        user = getSecurityManager().getUser()

        if not searchText:
            IStatusMessage(request).addStatusMessage(u'Search text is required.',type='error')
            url = getMultiAdapter((self.aq_parent, request), name='absolute_url')()
            request.response.redirect('%s/@@search_and_replace' %url)
            return

        previewBrains = []

        # make regex matcher for search text
        if not useRegex:
            searchText = re.escape(searchText)    
        matcher = re.compile(searchText, re.DOTALL | re.UNICODE | re.MULTILINE | (not matchCase and re.IGNORECASE or 0))

        # separate paths from indexes
        pathsAndIndexes = self.splitPathsAndIndexes(paths)
        # get all files
        fileGenerator = self.getPagesByPaths(pathsAndIndexes.keys(), includeChildren, fileExtensions, language, geo)
        for (brain, obj) in fileGenerator:
            #ensure that user has modify portal content permissions on objs, else do not include in batch
            if not user.has_permission('Modify portal content', obj):
                continue
            if replaceField == 'text':
                otext = self.getPageContents(obj)
                matchObject = matcher.search(otext)
            elif replaceField == 'title':
                otext = obj.title
                matchObject = matcher.search(otext)
            elif replaceField == 'description':
                otext = obj.getRawDescription()
                matchObject = matcher.search(otext) 
            matchIndex = 0
            replaced = False
            path = '/'.join(obj.getPhysicalPath())
            pathIndexes = path in pathsAndIndexes and pathsAndIndexes[path] or None
            while matchObject:
                matchEndPosition = matchObject.end()
                if pathIndexes is None or matchIndex in pathIndexes:
                    # create preview object
                    if not preview:
                        previewBrains.append(brain)
                    else:
                        previewBrains.append(PreviewBrain(request, brain, matchIndex, matchObject, replaceText, afterInContext=(replaceField=='file')))
                    # do replacement
                    if not preview:
                        thisReplaceText = matchObject.expand(replaceText)
                        if replaceField in ['text','description','title']:
                            beginIndex, beforeEndIndex = matchObject.span()
                            otext = otext[:beginIndex] + thisReplaceText + otext[beforeEndIndex:]
                            matchEndPosition = beginIndex + len(thisReplaceText)  
                        elif hasattr(obj, replaceField):
                            if not 'description':
                                setattr(obj, replaceField, thisReplaceText)
                            else:
                                obj.setDescription(thisReplaceText)

                        replaced = True
                if replaceField in ['text','title','description']:
                    matchObject = matcher.search(otext, matchEndPosition)
                    matchIndex += 1
                else:
                    # if we're replacing title or description, don't bother to
                    # find multiple matches in the file, just use the first
                    matchObject = None
            if replaced:
                if replaceField == 'text':
                    self.setPageContents(obj, otext)
                elif replaceField == 'description':
                    obj.setDescription(otext)
                elif replaceField == 'title':
                    obj.setTitle(otext)
                #obj.reindexObject()
                  
        if batch:
            #logger.info("batch is true!!!!")
            from Products.CMFPlone import Batch
            b_start = self.REQUEST.get('b_start', 0)
            previewBrains = Batch(previewBrains, b_size, int(b_start), orphan=0)

        return previewBrains

        

InitializeClass(SearchAndReplaceTool)
