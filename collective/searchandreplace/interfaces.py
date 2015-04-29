from zope.interface import Interface


class ISearchReplaceable(Interface):
    """ Marker interface for searching and replacing """


class ISearchReplaceUtility(Interface):
    """ Search and replace utility interface """

    def getItems():
        """ Get items for preview. """
