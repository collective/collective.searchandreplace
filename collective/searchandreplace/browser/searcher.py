from zope.publisher.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter

class SearcherForm(BrowserView):

    __name__ = 'search_and_replace_form'

    def __init__(self, context, request):
        self.context = context
        self.request = request

        

