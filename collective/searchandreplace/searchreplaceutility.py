# -*- coding: us-ascii -*-

from Acquisition import aq_base
from Acquisition import aq_parent
from collective.searchandreplace import SearchAndReplaceMessageFactory as _
from collective.searchandreplace.interfaces import ISearchReplaceSettings
from plone.app.layout.navigation.defaultpage import isDefaultPage
from plone.app.textfield import RichTextValue
from plone.app.textfield.interfaces import IRichText
from plone.registry.interfaces import IRegistry
from Products.Archetypes.interfaces import ITextField
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.i18n import translate
from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IText
from zope.schema.interfaces import ITextLine

import logging
import pkg_resources
import re

try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    HAS_DEXTERITY = True
    from plone.dexterity.utils import iterSchemata

logger = logging.getLogger('collective.searchreplace')
searchflags = re.DOTALL | re.UNICODE | re.MULTILINE
# List of text fields that are handled separately, instead of together with all
# text fields.  Note that 'title' is a string field, so we handle it
# separately, being the only string field that we want to change.  But we list
# it here to be on the safe side.
CUSTOM_HANDLED_TEXT_FIELDS = [
    'title',
]


def _to_unicode(s):
    assert isinstance(s, basestring)
    if not isinstance(s, unicode):
        s = s.decode('utf-8')
    return s


class SearchReplaceUtility(object):
    """ Search and replace utility. """

    # Permission to check before modifying content.
    permission = ModifyPortalContent

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
        onlySearchableText = kwargs.get('onlySearchableText', True)
        if 'replaceText' in kwargs:
            rtext = kwargs['replaceText']
            if rtext is None:
                # Allow replacing by an empty string.
                rtext = u''
        else:
            rtext = u''
        if 'doReplace' in kwargs:
            replace = kwargs['doReplace']
        else:
            replace = False
        if 'searchItems' in kwargs:
            sitems = kwargs['searchItems']
        else:
            sitems = None
        if 'maxResults' in kwargs:
            maxResults = kwargs['maxResults']
        else:
            maxResults = None
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
        parameters = dict(path=query)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchReplaceSettings, check=False)
        if settings.restrict_searchable_types:
            parameters['portal_type'] = settings.enabled_types
        if onlySearchableText:
            parameters['SearchableText'] = u'*{0}*'.format(find)
        brains = catalog(**parameters)
        memship = getToolByName(context, 'portal_membership')
        checkPermission = memship.checkPermission
        # Match objects
        results = []
        replaced = 0
        for b in brains:
            ipath = b.getPath()
            if not sitems or ipath in sitems:
                try:
                    obj = b.getObject()
                except (KeyError, AttributeError):
                    logger.warn('getObject failed for %s', ipath)
                    continue
                # Does the user have the modify permission on this object?
                if not checkPermission(self.permission, obj):
                    continue
                # If there is a filtered list of items, and it
                # is in the list, or if there is no filter
                # then process the item
                if replace:
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
                    if rep:
                        self._afterReplace(obj, find, rtext)
                        replaced += rep
                elif not replace:
                    # Just find the matches and return info
                    result = self._searchObject(matcher, obj)
                    if result:
                        results += result
                    if maxResults is not None and len(results) > maxResults:
                        results = results[:maxResults]
                        break
        if replace:
            return replaced
        else:
            return results

    def _afterReplace(self, obj, find, rtext):
        """Hook for doing things after a text has been replaced.

        - obj is the changed object
        - find is the found text
        - rtext is the replacement text

        By default, we will store a version in the CMFEditions repository.
        """
        repository = getToolByName(obj, 'portal_repository', None)
        if repository is None:
            return
        if obj.portal_type not in repository.getVersionableContentTypes():
            return
        comment = _(u'Replaced: ${old} -> ${new}',
                    mapping={'old': find, 'new': rtext})
        comment = translate(comment, context=obj.REQUEST)
        repository.save(obj, comment=comment)

    def _replaceObject(self, matcher, obj, cpath, rtext, mobjs):
        """ Replace text in objects """
        replaced = 0
        # rtext is already unicode
        base_obj = aq_base(obj)
        if mobjs:
            # Replace only the objects specified in mobjs
            title_positions = mobjs.pop('title', None)
            if title_positions is not None:
                title = _to_unicode(base_obj.Title())
                result = self._replaceText(matcher,
                                           title,
                                           rtext,
                                           title_positions)
                if result[0]:
                    replaced += result[0]
                    base_obj.setTitle(result[1])
            # Handle general text fields.
            for fieldname, positions in mobjs.items():
                text = self._getRawText(obj, fieldname)
                if text:
                    result = self._replaceText(matcher,
                                               text,
                                               rtext,
                                               positions)
                    if result[0]:
                        replaced += result[0]
                        self._setTextField(obj, fieldname, result[1])
        else:
            # Replace all occurences
            try:
                title = _to_unicode(base_obj.Title())
            except AttributeError:
                # Title might be acquired from parent for some types, which
                # breaks now that we have stripped away the acquisition chain
                # with aq_base.
                title = u''
            result = self._replaceText(matcher,
                                       title,
                                       rtext,
                                       None)
            if result[0]:
                replaced += result[0]
                base_obj.setTitle(result[1])
            text_fields = self._getTextFields(obj)
            for field in text_fields:
                text = self._getRawTextField(obj, field)
                if not text:
                    continue
                result = self._replaceText(matcher,
                                           text,
                                           rtext,
                                           None)
                if result[0]:
                    replaced += result[0]
                    self._setTextField(obj, field.__name__, result[1])

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
        base = aq_base(obj)
        try:
            title = _to_unicode(base.Title())
        except AttributeError:
            # Title might be acquired from parent for some types, which breaks
            # now that we have stripped away the acquisition chain with
            # aq_base.
            title = u''
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
        text_fields = self._getTextFields(obj)
        if text_fields:
            for field in text_fields:
                text = self._getRawTextField(obj, field)
                if not text:
                    continue
                mobj = matcher.finditer(text)
                for x in mobj:
                    start, end = x.span()
                    results.append({
                        'path': path,
                        'url': obj.absolute_url(),
                        'line': '%s %d' % (field.__name__,
                                           self._getLineNumber(text, start)),
                        'pos': '%d' % start,
                        'text': self._getLinePreview(text,
                                                     start,
                                                     end), })
        return results

    def _getTextFields(self, obj):
        # Get all text fields, except ones that are handled separately.
        text_fields = []
        if getattr(aq_base(obj), 'Schema', None):
            # Archetypes
            for field in obj.Schema().values():
                if field.__name__ in CUSTOM_HANDLED_TEXT_FIELDS:
                    continue
                if not ITextField.providedBy(field):
                    continue
                text_fields.append(field)
        elif HAS_DEXTERITY:
            # Dexterity
            for schemata in iterSchemata(obj):
                fields = getFieldsInOrder(schemata)
                for name, field in fields:
                    if name in CUSTOM_HANDLED_TEXT_FIELDS:
                        continue
                    if IRichText.providedBy(field):
                        text_fields.append(field)
                        continue
                    # ITextLine inherits from IText.
                    # We want to replace in texts, but not textlines.
                    # Maybe this can be made configurable.
                    if ITextLine.providedBy(field):
                        continue
                    if not IText.providedBy(field):
                        continue
                    text_fields.append(field)
        return text_fields

    def _getField(self, obj, fieldname):
        return getField(obj, fieldname)

    def _getRawTextField(self, obj, field):
        return getRawTextField(obj, field)

    def _getRawText(self, obj, fieldname):
        return getRawText(obj, fieldname)

    def _setTextField(self, obj, fieldname, text):
        obj_base = aq_base(obj)
        if getattr(obj_base, 'Schema', None):
            # Archetypes
            field = obj_base.getField(fieldname)
            if field is None:
                logger.warn('Field %s not found for %s',
                            fieldname, obj.getId())
                return
            field.set(obj, text)
        else:
            # Dexterity
            field = self._getField(obj_base, fieldname)
            if field is None:
                logger.warn('Field %s not found for %s',
                            fieldname, obj.getId())
                return
            if IRichText.providedBy(field):
                # Get mimetype from old value.
                old = field.get(obj)
                if old is None:
                    text = RichTextValue(text)
                else:
                    text = RichTextValue(
                        text, old.mimeType, old.outputMimeType)
            field.set(obj, text)

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
                continue
            if path not in itemd:
                itemd[path] = {}
            if 'title' == line:
                if 'title' not in itemd[path]:
                    itemd[path]['title'] = []
                itemd[path]['title'].append(int(pos))
            elif ' ' in line:
                try:
                    fieldname, line_number = line.split(' ')
                except ValueError:
                    continue
                if fieldname not in itemd[path]:
                    itemd[path][fieldname] = []
                itemd[path][fieldname].append(int(pos))
        return itemd


def getField(obj, fieldname):
    obj = aq_base(obj)
    if getattr(obj, 'Schema', None):
        # Archetypes
        return obj.getField(fieldname)
    # Dexterity
    for schemata in iterSchemata(obj):
        fields = getFieldsInOrder(schemata)
        for name, field in fields:
            if name == fieldname:
                return field


def getRawTextField(obj, field):
    text = None
    obj = aq_base(obj)
    if hasattr(field, 'getRaw'):
        # Archetypes
        baseunit = field.getRaw(obj, raw=True)
        if isinstance(baseunit, tuple):
            #  LinesField
            text = '\n'.join(baseunit)
        elif isinstance(baseunit.raw, unicode):
            text = baseunit.raw
        else:
            text = _to_unicode(field.getRaw(obj))
    else:
        # Dexterity
        baseunit = field.get(obj)
        if baseunit is None:
            text = u''
        else:
            # Rich text has a raw attribute, plain text simply has text
            # (unicode).
            text = getattr(baseunit, 'raw', baseunit)
    return text


def getRawText(obj, fieldname='text'):
    field = getField(obj, fieldname)
    if field is None:
        return u''
    return getRawTextField(obj, field)
