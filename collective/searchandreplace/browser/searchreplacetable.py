# -*- coding: us-ascii -*-
from collective.searchandreplace.interfaces import ISearchReplaceUtility
from collective.searchandreplace.interfaces import ISearchReplaceSettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.publisher.browser import BrowserView


class SearchReplaceTable(BrowserView):
    """ View class for search and replace preview table widget."""

    def maximum_text_characters(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchReplaceSettings, check=False)
        return settings.maximum_text_characters

    def getItems(self):
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

    def getRelativePath(self, path):
        """ Get a relative path """
        cpath = "/".join(self.context.getPhysicalPath())
        rpath = path[len(cpath) :]
        if rpath:
            rpath = "." + rpath
        else:
            rpath = "./"
        return rpath
