# -*- coding: us-ascii -*-

import re
from Acquisition import aq_parent
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.defaultpage import isDefaultPage


searchflags = re.DOTALL | re.UNICODE | re.MULTILINE


def _to_unicode(s):
    assert isinstance(s, basestring)
    if not isinstance(s, unicode):
        s = s.decode('utf-8')
    return s


class SearchReplaceUtility(object):
    """ Search and replace utility. """

    def searchObjects(self, context, find, **kwargs):
        """ Search objects and optionally do a replace. """
        # Get search parameters
        cpath = context.getPhysicalPath()
        if 'searchSubFolders' in kwargs:
            ssf = kwargs['searchSubFolders']
        else:
            ssf = True
        if 'matchCase' in kwargs:
            mc = kwargs['matchCase']
        else:
            mc = False
        if 'replaceText' in kwargs:
            rtext = kwargs['replaceText']
        else:
            rtext = None
        if 'doReplace' in kwargs:
            replace = kwargs['doReplace']
        else:
            replace = False
        if 'searchItems' in kwargs:
            sitems = kwargs['searchItems']
        else:
            sitems = None
        # Get Regex matcher
        sflags = mc and searchflags or (searchflags | re.IGNORECASE)
        matcher = re.compile(find, sflags)
        # Get items to search
        query = {'query': '/'.join(cpath)}
        if context.isPrincipiaFolderish and not ssf:
            query['depth'] = 1
        container = aq_parent(context)
        if isDefaultPage(container, context) and ssf:
            query['query'] = '/'.join(container.getPhysicalPath())
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(path=query)
        memship = getToolByName(context, 'portal_membership')
        checkPermission = memship.checkPermission
        # Match objects
        results = []
        replaced = 0
        for b in brains:
            ipath = b.getPath()
            if not sitems or ipath in sitems:
                obj = b.getObject()
                # Does the user have the modify permission on this object?
                if not checkPermission(ModifyPortalContent, obj):
                    continue
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
                                              obj,
                                              cpath,
                                              rtext,
                                              sitem)
                    replaced += rep
                elif not replace:
                    # Just find the matches and return info
                    result = self._searchObject(matcher, obj)
                    if result:
                        results += result
        if replace:
            return replaced
        else:
            return results

    def _replaceObject(self, matcher, obj, cpath, rtext, mobjs):
        """ Replace text in objects """
        replaced = 0
        # rtext is already unicode
        if mobjs:
            # Replace only the objects specified in mobjs
            if 'title' in mobjs:
                title = _to_unicode(obj.aq_base.Title())
                result = self._replaceText(matcher,
                                           title,
                                           rtext,
                                           mobjs['title'])
                if result[0]:
                    replaced += result[0]
                    obj.aq_base.setTitle(result[1])
            if 'description' in mobjs:
                desc = _to_unicode(obj.aq_base.getRawDescription())
                if desc:
                    result = self._replaceText(matcher,
                                               desc,
                                               rtext,
                                               mobjs['description'])
                    if result[0]:
                        replaced += result[0]
                        obj.aq_base.setDescription(result[1])
            if 'body' in mobjs:
                baseunit = obj.getField('text').getRaw(obj, raw=True)
                if isinstance(baseunit.raw, unicode):
                    body = baseunit.raw
                else:
                    body = _to_unicode(obj.aq_base.getRawText())
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
            title = _to_unicode(obj.aq_base.Title())
            result = self._replaceText(matcher,
                                       title,
                                       rtext,
                                       None)
            if result[0]:
                replaced += result[0]
                obj.aq_base.setTitle(result[1])
            desc = _to_unicode(obj.aq_base.getRawDescription())
            if desc:
                result = self._replaceText(matcher,
                                           desc,
                                           rtext,
                                           None)
                if result[0]:
                    replaced += result[0]
                    obj.setDescription(result[1])
            if getattr(obj.aq_base, 'getText', None):
                baseunit = obj.getField('text').getRaw(obj, raw=True)
                if isinstance(baseunit.raw, unicode):
                    body = baseunit.raw
                else:
                    body = _to_unicode(obj.aq_base.getRawText())
                if body:
                    result = self._replaceText(matcher,
                                               body,
                                               rtext,
                                               None)
                    if result[0]:
                        replaced += result[0]
                        obj.aq_base.setText(result[1])
        # don't have to utf-8 encoding
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

    def _searchObject(self, matcher, obj):
        """ Find location of search strings """
        results = []
        path = '/'.join(obj.getPhysicalPath())
        title = _to_unicode(obj.aq_base.Title())
        mobj = matcher.finditer(title)
        for x in mobj:
            start, end = x.span()
            results.append({
                'path': path,
                'url': obj.absolute_url(),
                'line': 'title',
                'pos': '%d' % start,
                'text': self._getLinePreview(title,
                                             start,
                                             end), })
        desc = _to_unicode(obj.aq_base.getRawDescription())
        if desc:
            mobj = matcher.finditer(desc)
            for x in mobj:
                start, end = x.span()
                results.append({
                    'path': path,
                    'url': obj.absolute_url(),
                    'line': 'description',
                    'pos': '%d' % start,
                    'text': self._getLinePreview(desc,
                                                 start,
                                                 end), })
        if getattr(obj.aq_base, 'getText', None):
            baseunit = obj.getField('text').getRaw(obj, raw=True)
            if isinstance(baseunit.raw, unicode):
                text = baseunit.raw
            else:
                text = _to_unicode(obj.aq_base.getRawText())
            mobj = matcher.finditer(text)
            for x in mobj:
                start, end = x.span()
                results.append({
                    'path': path,
                    'url': obj.absolute_url(),
                    'line': '%d' % self._getLineNumber(text,
                                                       start),
                    'pos': '%d' % start,
                    'text': self._getLinePreview(text,
                                                 start,
                                                 end), })
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
        if not isinstance([], type(items)):
            items = [items]
        for x in items:
            try:
                line, pos, path = x.split(':')
            except ValueError:
                break
            if path not in itemd:
                itemd[path] = {}
            if 'title' == line:
                if 'title' not in itemd[path]:
                    itemd[path]['title'] = []
                itemd[path]['title'].append(int(pos))
            elif 'description' == line:
                if 'description' not in itemd[path]:
                    itemd[path]['description'] = []
                itemd[path]['description'].append(int(pos))
            else:
                if 'body' not in itemd[path]:
                    itemd[path]['body'] = []
                itemd[path]['body'].append(int(pos))
        return itemd
