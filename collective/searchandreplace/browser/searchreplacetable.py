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
            
