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
