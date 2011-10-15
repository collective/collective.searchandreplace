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

import re


searchflags = re.DOTALL | re.UNICODE | re.MULTILINE 


class SearchReplaceUtility(object):
    """ Search and replace utility. """

    def searchObjects(self, context, find, **kwargs):
        """ Search objects and optionally do a replace. """
        # Get search parameters
        cpath = context.getPhysicalPath()
        if kwargs.has_key('searchSubFolders'):
            ssf = kwargs['searchSubFolders']
        else:
            ssf = True
        if kwargs.has_key('matchCase'):
            mc = kwargs['matchCase']
        else:
            mc = False
        if kwargs.has_key('replaceText'):
            rtext = kwargs['replaceText']
        else:
            rtext = None
        if kwargs.has_key('doReplace'):
            replace = kwargs['doReplace']
        else:
            replace = False
        if kwargs.has_key('searchItems'):
            sitems = kwargs['searchItems']
        else:
            sitems = None
        # Get Regex matcher
        sflags = mc and searchflags or (searchflags|re.IGNORECASE)
        matcher = re.compile(find, sflags)
        # Get items to search
        query = {'query':'/'.join(cpath)}
        if context.isPrincipiaFolderish and not ssf:
            query['depth'] = 1
        brains = context.portal_catalog(path=query)
        # Match objects
        results = []
        replaced = 0
        for b in brains:
            ipath = b.getPath()
            if not sitems or sitems.has_key(ipath):
                # If there is a filtered list of items, and it
                # is in the list, or if there is no filter
                # then process the item
                if replace and rtext:
                    # Do a replace
                    if sitems:
                        sitem = sitems[ipath]
                    else:
                        sitem = None
                    rep = self._replaceObject(matcher, 
                                              b, 
                                              cpath, 
                                              rtext,
                                              sitem)
                    replaced += rep
                elif not replace:
                    # Just find the matches and return info
                    result = self._searchObject(matcher, b) 
                    if result:
                        results += result
        if replace:
            return replaced
        else:
            return results

    def _replaceObject(self, matcher, brain, cpath, rtext, mobjs):
        """ Replace text in objects """
        replaced = 0
        obj = brain.getObject()
        if mobjs:
            # Replace only the objects specified in mobjs
            if mobjs.has_key('title'):
                title = obj.aq_base.Title()
                result = self._replaceText(matcher, 
                                           title, 
                                           rtext, 
                                           mobjs['title'])
                if result[0]:
                    replaced += result[0]
                    obj.aq_base.setTitle(result[1])
            if mobjs.has_key('description'):
                desc = obj.aq_base.getRawDescription()
                if desc:
                    result = self._replaceText(matcher,
                                               desc,
                                               rtext,
                                               mobjs['description'])
                    if result[0]:
                        replaced += result[0]
                        obj.aq_base.setDescription(result[1])
            if mobjs.has_key('body'):
                body = obj.aq_base.getText()
                if body:
                    result = self._replaceText(matcher,
                                               body,
                                               rtext,
                                               mobjs['body'])
                    if result[0]:
                        replaced += result[0]
                        obj.aq_base.setText(result[1])
        else:
            # Replace all occurences
            title = obj.aq_base.Title()
            result = self._replaceText(matcher,
                                       title,
                                       rtext,
                                       None)
            if result[0]:
                replaced += result[0]
                obj.aq_base.setTitle(result[1])
            desc = obj.getRawDescription()
            if desc:
                result = self._replaceText(matcher,
                                           desc,
                                           rtext,
                                           None)
                if result[0]:
                    replaced += result[0]
                    obj.setDescription(result[1])
            body = obj.aq_base.getText()
            if body:
                result = self._replaceText(matcher,
                                           body,
                                           rtext,
                                           None)
                if result[0]:
                    replaced += result[0]
                    obj.aq_base.setText(result[1])
        if replaced:
            obj.reindexObject()                
        return replaced

    def _replaceText(self, matcher, text, rtext, indexes):
        """ Replace instances """
        newtext = ''
        mindex = 0
        replaced = 0
        mobj = matcher.finditer(text)
        for x in mobj:
            start, end = x.span()
            if not indexes or start in indexes:
                newtext += text[mindex:start]
                newtext += rtext
                mindex = end
                replaced += 1
        newtext += text[mindex:]
        return replaced, newtext

    def _searchObject(self, matcher, brain):
        """ Find location of search strings """
        results = []
        obj = brain.getObject()
        path = '/'.join(obj.getPhysicalPath())
        title = obj.aq_base.Title()
        mobj = matcher.finditer(title)
        for x in mobj:
            start, end = x.span()
            results.append({
                    'path':path,
                    'url':obj.absolute_url(),
                    'line':'title',
                    'pos':'%d' %start,
                    'text':self._getLinePreview(title, 
                                                start, 
                                                end),})
        desc = obj.aq_base.getRawDescription()
        if desc:
            mobj = matcher.finditer(desc)
            for x in mobj:
                start, end = x.span()
                results.append({
                        'path':path,
                        'url':obj.absolute_url(),
                        'line':'description', 
                        'pos':'%d' %start,
                        'text':self._getLinePreview(desc, 
                                                    start, 
                                                    end),})
        if getattr(obj.aq_base, 'getText', None):
            text = obj.aq_base.getText()
            mobj = matcher.finditer(text)
            for x in mobj:
                start, end = x.span()
                results.append({
                        'path':path,
                        'url':obj.absolute_url(),
                        'line':'%d' %self._getLineNumber(text, 
                                                         start),
                        'pos':'%d' %start,
                        'text':self._getLinePreview(text, 
                                                    start, 
                                                    end),})
        return results

    def _getLineNumber(self, text, index):
        return text.count('\n', 0, index) + 1

    def _getLinePreview(self, text, start, end):
        sindex = text[:start].rfind('\n')
        if -1 == sindex:
            sindex = 0
        eindex = text[end:].find('\n')
        if -1 == eindex:
            eindex = None
        else:
            eindex += end
        return (text[sindex:start],
                text[start:end],
                text[end:eindex])

    def parseItems(self, items):
        """ Get list of items from form values """
        itemd = {}
        if type([]) != type(items):
            items = [items]
        for x in items:
            try:
                line, pos, path = x.split(':')
            except ValueError:
                break
            if not itemd.has_key(path):
                itemd[path] = {}
            if 'title' == line:
                if not itemd[path].has_key('title'):
                    itemd[path]['title'] = []
                itemd[path]['title'].append(int(pos))
            elif 'description' == line:
                if not itemd[path].has_key('description'):
                    itemd[path]['description'] = []
                itemd[path]['description'].append(int(pos))
            else:
                if not itemd[path].has_key('body'):
                    itemd[path]['body'] = []
                itemd[path]['body'].append(int(pos))
        return itemd
