from collective.searchandreplace.interfaces import ISearchReplaceUtility
from collective.searchandreplace.tests.base import SearchAndReplaceTestCase
from zope.component import getUtility


class testMatchCase(SearchAndReplaceTestCase):
    """ Ensure that the match case flag works   """

    def afterSetUp(self):
        self.srutil = getUtility(ISearchReplaceUtility)

    def testNoMatchCase(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setText('Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test case',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testMatchCase(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc2')
        doc2 = getattr(self.portal, 'doc2')
        doc2.setTitle('test title')
        doc2.setText('Test Case')
        results = self.srutil.searchObjects(
            doc2,
            'test case',
            replaceText='foo',
            matchCase=True)
        self.assertEqual(len(results), 0)

    def testOneMatch(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setText('Test Case')
        self.portal.invokeFactory('Document', 'doc2')
        doc2 = getattr(self.portal, 'doc2')
        doc2.setTitle('test title')
        doc2.setText('test case')
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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMatchCase))
    return suite
