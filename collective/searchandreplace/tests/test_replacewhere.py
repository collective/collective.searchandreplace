from Products.CMFPlone.tests import PloneTestCase
from unittest import TestSuite, makeSuite
from Testing import ZopeTestCase
from Testing.ZopeTestCase import user_name
from AccessControl import Unauthorized
from base import SearchAndReplaceTestCase
from Products.Archetypes.tests.test_fields import FakeRequest


class testReplaceWhere(SearchAndReplaceTestCase):
    """ Ensure that the match case flag works   """

    def afterSetUp(self):
        self.srtool = self.portal.portal_search_and_replace
        self.request = FakeRequest()

    def testReplaceText(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setDescription('Test Description')
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

    def testReplaceTitle(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc2')
        doc1 = getattr(self.portal, 'doc2')
        doc1.setTitle('Test Title')
        doc1.setDescription('Test Description')
        doc1.setText('Test Case')
        path = ['/'.join(doc1.getPhysicalPath())]
        results = self.srtool.searchAndReplace(self.request,
                                               path,
                                               'test title',
                                               'title',
                                               'foo',
                                               matchCase=False,
                                               preview=True)
        assert(len(results) == 1)


    def testReplaceDescription(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setDescription('Test Description')
        doc1.setText('Test Case')
        path = ['/'.join(doc1.getPhysicalPath())]
        results = self.srtool.searchAndReplace(self.request,
                                               path,
                                               'test desc',
                                               'description',
                                               'foo',
                                               matchCase=False,
                                               preview=True)
        assert(len(results) == 1)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testReplaceWhere))
    return suite
