from Products.CMFPlone.tests import PloneTestCase
from unittest import TestSuite, makeSuite
from Testing import ZopeTestCase
from Testing.ZopeTestCase import user_name
from AccessControl import Unauthorized
from base import SearchAndReplaceTestCase
from Products.Archetypes.tests.test_fields import FakeRequest


class testMatchCase(SearchAndReplaceTestCase):
    """ Ensure that the match case flag works   """

    def afterSetUp(self):
        self.srtool = self.portal.portal_search_and_replace
        self.request = FakeRequest()

    def testNoMatchCase(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setText('Test Case')
        path = ['/'.join(doc1.getPhysicalPath())]
        results = self.srtool.searchAndReplace(self.request,
                                               path,
                                               'test case',
                                               'text',
                                               'foo',
                                               matchCase=False,
                                               preview=True)
        assert(len(results) == 1)

    def testMatchCase(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc2')
        doc2 = getattr(self.portal, 'doc2')
        doc2.setTitle('test title')
        doc2.setText('Test Case')
        path = ['/'.join(doc2.getPhysicalPath())]
        results = self.srtool.searchAndReplace(self.request,
                                               path,
                                               'test case',
                                               'text',
                                               'foo',
                                               matchCase=True,
                                               preview=True)
        assert(len(results) == 0)


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
        path1 = '%s[0]' %  '/'.join(doc1.getPhysicalPath())
        path2 = '%s[0]' % '/'.join(doc2.getPhysicalPath())
        paths = [path1, path2]
        results = self.srtool.searchAndReplace(self.request,
                                               paths,
                                               'test case',
                                               'text',
                                               'foo',
                                               matchCase=True,
                                               preview=True)
        assert(len(results) == 1)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMatchCase))
    return suite
