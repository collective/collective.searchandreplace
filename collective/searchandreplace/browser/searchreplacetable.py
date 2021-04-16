# -*- coding: us-ascii -*-
from collective.searchandreplace.interfaces import ISearchReplaceUtility
from collective.searchandreplace.interfaces import ISearchReplaceSettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.publisher.browser import BrowserView
from collections import namedtuple
import six


Field = namedtuple('Field', ['label', 'value'])


class SearchReplaceTable(BrowserView):
    """ View class for search and replace preview table widget."""

    def __init__(self, context, request):
        super(SearchReplaceTable, self).__init__(context, request)
        self.results = self.findObjects()
        self.computeAffectedFields()
        self.filter_fields = self.getFilterFields()
        self.are_fields_filtered = self.filter_fields != self.fields

    def maximum_text_characters(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchReplaceSettings, check=False)
        return settings.maximum_text_characters

    def findObjects(self):
        """ Get preview items """
        results = []
        findWhat = self.request.get("form.findWhat", "")
        searchSubFolders = "form.searchSubfolders" in self.request
        matchCase = "form.matchCase" in self.request
        try:
            maxResults = int(self.request.get("form.maxResults", ""))
        except ValueError:
            maxResults = None
        onlySearchableText = "form.onlySearchableText" in self.request

        srutil = getUtility(ISearchReplaceUtility)
        if findWhat:
            results = srutil.findObjects(
                self.context,
                findWhat=findWhat,
                searchSubFolders=searchSubFolders,
                matchCase=matchCase,
                maxResults=maxResults,
                onlySearchableText=onlySearchableText,
            )
        return results

    def computeAffectedFields(self):
        self.fields = set()
        self.field_labels = set()
        for item in self.results:
            self.fields.add(item['field'])
            self.field_labels.add(Field(item['label'], item['field']))

    def getAffectedFields(self):
        results = list(self.field_labels)
        results.sort()
        return results

    def getFieldFilterClass(self):
        return '' if self.are_fields_filtered else 'hiddenStructure'

    def getFilterFields(self):
        fields = self.request.get("form.filterFields", None)
        if fields is None:
            # reset to all fields when no fields are selected
            return self.fields
        elif isinstance(fields, six.text_type) or isinstance(fields, six.binary_type):
            # take care of a single field being selected
            result = set()
            result.add(fields)
            return result
        else:
            return set(fields)

    def getItems(self):
        if not self.are_fields_filtered:
            return self.results
        else:
            return [item for item in self.results if item['field'] in self.filter_fields]

    def getRelativePath(self, path):
        """ Get a relative path """
        cpath = "/".join(self.context.getPhysicalPath())
        rpath = path[len(cpath):]
        if rpath:
            rpath = "." + rpath
        else:
            rpath = "./"
        return rpath
