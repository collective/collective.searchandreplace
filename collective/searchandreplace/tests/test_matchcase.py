from collective.searchandreplace.interfaces import ISearchReplaceUtility
from collective.searchandreplace.testing import MAJOR_PLONE_VERSION
from collective.searchandreplace.testing import create_doc
from collective.searchandreplace.testing import edit_content
from collective.searchandreplace.testing import SEARCH_REPLACE_INTEGRATION_LAYER  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility

import unittest


class TestMatchCase(unittest.TestCase):
    """ Ensure that the match case flag works   """

    layer = SEARCH_REPLACE_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer["portal"]
        self.srutil = getUtility(ISearchReplaceUtility)

    def testNoMatchCase(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        create_doc(self.portal, id="doc1", title=u"Find Title", text=u"Find Case")
        doc1 = getattr(self.portal, "doc1")
        results = self.srutil.findObjects(doc1, "find case", matchCase=False)
        self.assertEqual(len(results), 1)

    def testMatchCase(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc2")
        doc2 = getattr(self.portal, "doc2")
        edit_content(doc2, title="find title", text="Find Case")
        results = self.srutil.findObjects(doc2, "find case", matchCase=True)
        self.assertEqual(len(results), 0)

    def testOneMatch(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(doc1, title="Find Title", text="Find Case")
        self.portal.invokeFactory("Document", "doc2")
        doc2 = getattr(self.portal, "doc2")
        edit_content(doc2, title="find title", text="find case")
        # path1 = '%s' %  '/'.join(doc1.getPhysicalPath())
        # path2 = '%s' % '/'.join(doc2.getPhysicalPath())
        # paths = {path1: {'body': [0]}, path2: {'body': [0]}}
        results = self.srutil.findObjects(
            self.portal,
            "find case",
            matchCase=True,
            # occurences=paths
        )
        self.assertEqual(len(results), 1)


class TestMultipleMatchCase(unittest.TestCase):
    """Ensure that multiple matches work."""

    layer = SEARCH_REPLACE_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer["portal"]
        self.srutil = getUtility(ISearchReplaceUtility)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        self.doc1 = getattr(self.portal, "doc1")
        edit_content(
            self.doc1, title="Find find Find find", text="Find find\nFind find"
        )

    def testSearchCase(self):
        results = self.srutil.findObjects(
            self.portal,
            "Find",
            matchCase=True,
        )
        self.assertEqual(len(results), 4)
        # title field, first match
        self.assertEqual(results[0]["linecol"], "Title")
        self.assertEqual(results[0]["line"], "title")
        self.assertEqual(results[0]["pos"], "0")
        # title field, second match
        self.assertEqual(results[1]["linecol"], "Title")
        self.assertEqual(results[1]["line"], "title")
        self.assertEqual(results[1]["pos"], "10")
        # text field, line 1
        if MAJOR_PLONE_VERSION >= 5:
            self.assertEqual(results[2]["linecol"], "Text 1")
        else:  # Plone 4
            self.assertEqual(results[2]["linecol"], "Body Text 1")
        self.assertEqual(results[2]["line"], "text 1")
        self.assertEqual(results[2]["pos"], "0")
        # text field, line 2
        if MAJOR_PLONE_VERSION >= 5:
            self.assertEqual(results[3]["linecol"], "Text 2")
        else:  # Plone 4
            self.assertEqual(results[3]["linecol"], "Body Text 2")
        self.assertEqual(results[3]["line"], "text 2")
        self.assertEqual(results[3]["pos"], "10")

    def testSearchNoCase(self):
        results = self.srutil.findObjects(
            self.portal,
            "Find",
            matchCase=False,
        )
        self.assertEqual(len(results), 8)

    def testReplaceAll(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        results = self.srutil.replaceAllMatches(
            self.portal,
            "Find",
            replaceWith="Bike",
            matchCase=True,
        )
        self.assertEqual(results, 4)
        self.assertEqual(self.doc1.Title(), "Bike find Bike find")
        self.assertEqual(getRawText(self.doc1), "Bike find\nBike find")

    def testReplacePaths(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        path = "/".join(self.doc1.getPhysicalPath())
        paths = {
            path: {
                # Replace two positions from title
                "title": [0, 10],
                # Replace two positions from text
                "text": [5, 15],
            }
        }
        results = self.srutil.replaceFilteredOccurences(
            self.portal,
            "Find",
            replaceWith="Bike",
            occurences=paths,
            matchCase=False,
        )
        self.assertEqual(results, 4)
        self.assertEqual(self.doc1.Title(), "Bike find Bike find")
        self.assertEqual(getRawText(self.doc1), "Find Bike\nFind Bike")
