# -*- coding: us-ascii -*-

from Acquisition import aq_base
from Acquisition import aq_parent
from collective.searchandreplace import SearchAndReplaceMessageFactory as _
from collective.searchandreplace.interfaces import ISearchReplaceSettings
from plone import api
from plone.app.layout.navigation.defaultpage import isDefaultPage
from plone.app.textfield import RichTextValue
from plone.app.textfield.interfaces import IRichText
from plone.registry.interfaces import IRegistry
from Products.CMFPlone import PloneMessageFactory
from Products.CMFPlone.utils import safe_unicode
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.i18n import translate
from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IText
from zope.schema.interfaces import ITextLine
from zope.schema.interfaces import ITuple

import logging
import pkg_resources
import re
import six

try:
    pkg_resources.get_distribution("plone.dexterity")
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    HAS_DEXTERITY = True
    from plone.dexterity.utils import iterSchemata

try:
    pkg_resources.get_distribution("Products.Archetypes")
except pkg_resources.DistributionNotFound:
    HAS_ARCHETYPES = False
else:
    HAS_ARCHETYPES = True
    from Products.Archetypes.interfaces import ITextField
    from Products.Archetypes.interfaces import ILinesField
    from Products.Archetypes.interfaces import IStringField

logger = logging.getLogger("collective.searchreplace")
searchflags = re.DOTALL | re.UNICODE | re.MULTILINE
# List of text fields that are handled separately, instead of together with all
# text fields.  Note that 'title' is a string field, so we handle it
# separately, being the only string field that we want to change.  But we list
# it here to be on the safe side.
CUSTOM_HANDLED_TEXT_FIELDS = [
    "title",
    "id",
]


def make_matcher(findWhat, matchCase):
    sflags = matchCase and searchflags or (searchflags | re.IGNORECASE)
    return re.compile(findWhat, sflags)


def make_catalog_query_args(context, findWhat, searchSubFolders, onlySearchableText):
    # Get items to search
    query = {"query": "/".join(context.getPhysicalPath())}
    if context.isPrincipiaFolderish and not searchSubFolders:
        query["depth"] = 1
    container = aq_parent(context)
    if isDefaultPage(container, context) and searchSubFolders:
        query["query"] = "/".join(container.getPhysicalPath())
    catalog_query_args = dict(path=query)
    if settings().restrict_searchable_types:
        catalog_query_args["portal_type"] = settings().enabled_types
    if onlySearchableText:
        catalog_query_args["SearchableText"] = u"*{0}*".format(findWhat)
    return catalog_query_args


def settings():
    registry = getUtility(IRegistry)
    return registry.forInterface(ISearchReplaceSettings, check=False)


class SearchReplaceUtility(object):
    """ Search and replace utility. """

    # Permission to check before modifying content.
    permission = ModifyPortalContent

    def replaceAllMatches(
        self,
        context,
        findWhat,
        replaceWith,
        matchCase=False,
        onlySearchableText=True,
        searchSubFolders=True,
    ):
        matcher = make_matcher(findWhat, matchCase)
        catalog = api.portal.get_tool("portal_catalog")
        catalog_query_args = make_catalog_query_args(
            context,
            findWhat,
            searchSubFolders,
            onlySearchableText,
        )
        brains = catalog(**catalog_query_args)
        repl_count = 0
        for b in brains:
            try:
                obj = b.getObject()
            except (KeyError, AttributeError):
                ipath = b.getPath()
                logger.warn("getObject failed for %s", ipath)
                continue
            mtool = api.portal.get_tool("portal_membership")
            if not mtool.checkPermission(self.permission, obj):
                continue
            count = replace_all_in_object(
                matcher,
                obj,
                replaceWith,
            )
            if count:
                reindexObject(obj)
                afterReplace(obj, findWhat, replaceWith)
                repl_count += count
        return repl_count

    def replaceFilteredOccurences(
        self,
        context,
        findWhat,
        replaceWith,
        occurences,
        matchCase=False,
        onlySearchableText=True,
        searchSubFolders=True,
    ):
        matcher = make_matcher(findWhat, matchCase)
        catalog = api.portal.get_tool("portal_catalog")
        catalog_query_args = make_catalog_query_args(
            context,
            findWhat,
            searchSubFolders,
            onlySearchableText,
        )
        brains = catalog(**catalog_query_args)
        repl_count = 0
        for b in brains:
            ipath = b.getPath()
            if ipath not in occurences:
                continue
            try:
                obj = b.getObject()
            except (KeyError, AttributeError):
                logger.warn("getObject failed for %s", ipath)
                continue
            mtool = api.portal.get_tool("portal_membership")
            if not mtool.checkPermission(self.permission, obj):
                continue
            count = replace_occurences_in_object(
                matcher,
                obj,
                replaceWith,
                occurences[ipath],
            )
            if count:
                reindexObject(obj)
                afterReplace(obj, findWhat, replaceWith)
                repl_count += count
        return repl_count

    def findObjects(
        self,
        context,
        findWhat,
        matchCase=False,
        onlySearchableText=True,
        searchSubFolders=True,
        maxResults=None,
    ):
        matcher = make_matcher(findWhat, matchCase)
        catalog = api.portal.get_tool("portal_catalog")
        catalog_query_args = make_catalog_query_args(
            context,
            findWhat,
            searchSubFolders,
            onlySearchableText,
        )
        brains = catalog(**catalog_query_args)
        matches = []
        for b in brains:
            try:
                obj = b.getObject()
            except (KeyError, AttributeError):
                ipath = b.getPath()
                logger.warn("getObject failed for %s", ipath)
                continue
            mtool = api.portal.get_tool("portal_membership")
            if not mtool.checkPermission(self.permission, obj):
                continue
            matches.extend(find_matches_in_object(matcher, obj))
            if maxResults is not None and len(matches) > maxResults:
                matches = matches[:maxResults]
                break
        return matches


def afterReplace(obj, found, rtext):
    """Hook for doing things after a text has been replaced.

    - obj is the changed object
    - found is the found text
    - rtext is the replacement text

    By default, we will store a version in the CMFEditions repository.
    """
    repository = getToolByName(obj, "portal_repository", None)
    if repository is None:
        return
    if obj.portal_type not in repository.getVersionableContentTypes():
        return
    comment = _(u"Replaced: ${old} -> ${new}", mapping={"old": found, "new": rtext})
    comment = translate(comment, context=obj.REQUEST)
    repository.save(obj, comment=comment)


def replace_all_in_object(matcher, obj, rtext):
    """ Replace text in objects """
    repl_count = 0
    base_obj = aq_base(obj)
    try:
        title = safe_unicode(base_obj.Title())
    except AttributeError:
        # Title might be acquired from parent for some types, which
        # breaks now that we have stripped away the acquisition chain
        # with aq_base.
        title = u""
    count, new_text = replaceText(matcher, title, rtext, None)
    if count:
        repl_count += count
        base_obj.setTitle(new_text)
    text_fields = getTextFields(obj)
    for field in text_fields:
        text = getRawTextField(obj, field)
        if not text:
            continue
        count, new_text = replaceText(matcher, text, rtext, None)
        if count:
            repl_count += count
            setTextField(obj, field.__name__, new_text)

    return repl_count


def replace_occurences_in_object(matcher, obj, rtext, mobjs):
    """ Replace text in objects """
    repl_count = 0
    title_positions = mobjs.pop("title", None)
    if title_positions is not None:
        base_obj = aq_base(obj)
        title = safe_unicode(base_obj.Title())
        count, new_text = replaceText(matcher, title, rtext, title_positions)
        if count:
            repl_count += count
            base_obj.setTitle(new_text)
    # Handle general text fields.
    for fieldname, positions in mobjs.items():
        text = getRawText(obj, fieldname)
        if text:
            count, new_text = replaceText(matcher, text, rtext, positions)
            if count:
                repl_count += count
                setTextField(obj, fieldname, new_text)
    return repl_count


def reindexObject(obj):
    if settings().update_modified:
        obj.reindexObject()
    else:
        catalog = api.portal.get_tool("portal_catalog")
        obj.reindexObject(idxs=catalog.indexes())


def replaceText(matcher, text, rtext, indexes):
    """ Replace instances """
    newtext = ""
    if not rtext:
        rtext = ""
    mindex = 0
    repl_count = 0
    mobj = matcher.finditer(text)
    for x in mobj:
        start, end = x.span()
        if not indexes or start in indexes:
            newtext += text[mindex:start]
            newtext += rtext
            mindex = end
            repl_count += 1
    newtext += text[mindex:]
    return repl_count, newtext


def find_matches_in_object(matcher, obj):
    """ Find location of search strings """
    results = []
    path = "/".join(obj.getPhysicalPath())
    base = aq_base(obj)
    try:
        title = safe_unicode(base.Title())
    except AttributeError:
        # Title might be acquired from parent for some types, which breaks
        # now that we have stripped away the acquisition chain with
        # aq_base.
        title = u""
    mobj = matcher.finditer(title)
    for x in mobj:
        start, end = x.span()
        label = translate(PloneMessageFactory(u"Title"), context=obj.REQUEST)
        results.append(
            {
                "path": path,
                "url": obj.absolute_url(),
                "field": "title",
                "label": label,
                "line": "title",
                "linecol": label,
                "pos": "%d" % start,
                "text": getLinePreview(title, start, end),
            }
        )
    text_fields = getTextFields(obj)
    if text_fields:
        for field in text_fields:
            if hasattr(field, "widget"):
                label = translate(field.widget.label, context=obj.REQUEST)
            else:
                label = translate(field.title, context=obj.REQUEST)
            text = getRawTextField(obj, field)
            if not text:
                continue
            mobj = matcher.finditer(text)
            for x in mobj:
                start, end = x.span()
                results.append(
                    {
                        "path": path,
                        "url": obj.absolute_url(),
                        "field": field.__name__,
                        "label": label,
                        "line": "%s %d" % (field.__name__, getLineNumber(text, start)),
                        "linecol": "%s %d" % (label, getLineNumber(text, start)),
                        "pos": "%d" % start,
                        "text": getLinePreview(text, start, end),
                    }
                )
    return results


def getTextFields(obj):
    include_textline_fields = settings().include_textline_fields
    include_lines_fields = settings().include_lines_fields
    text_fields = []
    if HAS_ARCHETYPES and getattr(aq_base(obj), "Schema", None):
        # Archetypes
        for field in obj.Schema().values():
            if field.__name__ in CUSTOM_HANDLED_TEXT_FIELDS:
                continue
            if include_textline_fields and IStringField.providedBy(field):
                text_fields.append(field)
                continue
            if ITextField.providedBy(field):
                text_fields.append(field)
            if include_lines_fields and ILinesField.providedBy(field):
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
                # That we want to replace in texts, but not textlines
                # is by configuration.
                if not include_textline_fields and ITextLine.providedBy(field):
                    continue
                if IText.providedBy(field):
                    text_fields.append(field)
                if (
                    include_lines_fields
                    and ITuple.providedBy(field)
                    and ITextLine.providedBy(field.value_type)
                ):
                    text_fields.append(field)
    return text_fields


def setTextField(obj, fieldname, text):
    text = six.text_type(text)
    obj_base = aq_base(obj)
    if getattr(obj_base, "Schema", None):
        # Archetypes
        field = obj_base.getField(fieldname)
        if field is None:
            logger.warn("Field %s not found for %s", fieldname, obj.getId())
            return
        field.set(obj, text)
    else:
        # Dexterity
        field = getField(obj_base, fieldname)
        if field is None:
            logger.warn("Field %s not found for %s", fieldname, obj.getId())
            return
        if IRichText.providedBy(field):
            # Get mimetype from old value.
            old = field.get(obj)
            if old is None:
                text = RichTextValue(text)
            else:
                text = RichTextValue(text, old.mimeType, old.outputMimeType)
        if ITuple.providedBy(field) and ITextLine.providedBy(field.value_type):
            text = tuple(text.split("\n"))
        setattr(field.interface(obj), field.__name__, text)


def getLineNumber(text, index):
    return text.count("\n", 0, index) + 1


def getLinePreview(text, start, end):
    sindex = text[:start].rfind("\n")
    if -1 == sindex:
        sindex = 0
    eindex = text[end:].find("\n")
    if -1 == eindex:
        eindex = None
    else:
        eindex += end
    return (text[sindex:start], text[start:end], text[end:eindex])


def getField(obj, fieldname):
    obj = aq_base(obj)
    if getattr(obj, "Schema", None):
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
    if hasattr(field, "getRaw"):
        # Archetypes
        baseunit = field.getRaw(obj, raw=True)
        if isinstance(baseunit, tuple):
            #  LinesField
            text = safe_unicode("\n".join(baseunit))
        elif hasattr(baseunit, "raw") and isinstance(baseunit.raw, six.text_type):
            text = baseunit.raw
        else:
            text = safe_unicode(field.getRaw(obj))
    else:
        # Dexterity
        baseunit = getattr(field.interface(obj), field.__name__)
        if baseunit is None:
            text = u""
        elif isinstance(baseunit, tuple):
            text = safe_unicode("\n".join(baseunit))
        else:
            # Rich text has a raw attribute, plain text simply has text
            # (unicode).
            text = getattr(baseunit, "raw", baseunit)
    return text


def getRawText(obj, fieldname="text"):
    field = getField(obj, fieldname)
    if field is None:
        return u""
    return getRawTextField(obj, field)
