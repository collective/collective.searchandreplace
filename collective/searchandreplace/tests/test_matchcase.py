from collective.searchandreplace.interfaces import ISearchReplaceUtility
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
        self.portal = self.layer['portal']
        self.srutil = getUtility(ISearchReplaceUtility)

    def testNoMatchCase(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        create_doc(self.portal, id='doc1', title=u'Test Title',
                   text=u'Test Case')
        doc1 = getattr(self.portal, 'doc1')
        results = self.srutil.searchObjects(
            doc1,
            'test case',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testMatchCase(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'doc2')
        doc2 = getattr(self.portal, 'doc2')
        edit_content(doc2, title='test title', text='Test Case')
        results = self.srutil.searchObjects(
            doc2,
            'test case',
            replaceText='foo',
            matchCase=True)
        self.assertEqual(len(results), 0)

    def testOneMatch(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        edit_content(doc1, title='Test Title', text='Test Case')
        self.portal.invokeFactory('Document', 'doc2')
        doc2 = getattr(self.portal, 'doc2')
        edit_content(doc2, title='test title', text='test case')
        # path1 = '%s' %  '/'.join(doc1.getPhysicalPath())
        # path2 = '%s' % '/'.join(doc2.getPhysicalPath())
        # paths = {path1: {'body': [0]}, path2: {'body': [0]}}
        results = self.srutil.searchObjects(
            self.portal,
            'test case',
            replaceText='foo',
            matchCase=True,
            # searchItems=paths
        )
        self.assertEqual(len(results), 1)


class TestMultipleMatchCase(unittest.TestCase):
    """Ensure that multiple matches work."""

    layer = SEARCH_REPLACE_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer['portal']
        self.srutil = getUtility(ISearchReplaceUtility)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        self.doc1 = getattr(self.portal, 'doc1')
        edit_content(self.doc1,
                     title='Test test Test test',
                     text='Test test\nTest test')

    def testSearchCase(self):
        results = self.srutil.searchObjects(
            self.portal,
            'Test',
            replaceText='Bike',
            matchCase=True,
        )
        self.assertEqual(len(results), 4)
        # title field, first match
        self.assertEqual(results[0]['line'], 'title')
        self.assertEqual(results[0]['pos'], '0')
        # title field, second match
        self.assertEqual(results[1]['line'], 'title')
        self.assertEqual(results[1]['pos'], '10')
        # text field, line 1
        self.assertEqual(results[2]['line'], 'text 1')
        self.assertEqual(results[2]['pos'], '0')
        # text field, line 2
        self.assertEqual(results[3]['line'], 'text 2')
        self.assertEqual(results[3]['pos'], '10')

    def testSearchNoCase(self):
        results = self.srutil.searchObjects(
            self.portal,
            'Test',
            replaceText='Bike',
            matchCase=False,
        )
        self.assertEqual(len(results), 8)

    def testReplaceAll(self):
        from collective.searchandreplace.searchreplaceutility import getRawText
        results = self.srutil.searchObjects(
            self.portal,
            'Test',
            replaceText='Bike',
            matchCase=True,
            doReplace=True,
        )
        self.assertEqual(results, 4)
        self.assertEqual(self.doc1.Title(), 'Bike test Bike test')
        self.assertEqual(getRawText(self.doc1), 'Bike test\nBike test')

    def testReplacePaths(self):
        from collective.searchandreplace.searchreplaceutility import getRawText
        path = '/'.join(self.doc1.getPhysicalPath())
        paths = {
            path: {
                # Replace two positions from title
                'title': [0, 10],
                # Replace two positions from text
                'text': [5, 15],
            }
        }
        results = self.srutil.searchObjects(
            self.portal,
            'Test',
            replaceText='Bike',
            matchCase=False,
            doReplace=True,
            searchItems=paths,
        )
        self.assertEqual(results, 4)
        self.assertEqual(self.doc1.Title(), 'Bike test Bike test')
        self.assertEqual(getRawText(self.doc1), 'Test Bike\nTest Bike')
