from Products.CMFPlone.tests import PloneTestCase
from unittest import TestSuite, makeSuite
from Testing import ZopeTestCase
from Testing.ZopeTestCase import user_name
from AccessControl import Unauthorized
from base import SearchAndReplaceTestCase
from Products.Archetypes.tests.test_fields import FakeRequest


class testRegex(SearchAndReplaceTestCase):
    """ Ensure that the match case flag works   """

    def afterSetUp(self):
        self.srtool = self.portal.portal_search_and_replace
        self.request = FakeRequest()

    def testRegex(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setText('Test TestTest')
        path = ['/'.join(doc1.getPhysicalPath())]
        results = self.srtool.searchAndReplace(self.request,
                                               path,
                                               '\\bTest\\b',
                                               'text',
                                               'foo',
                                               useRegex='on',
                                               preview=True)
        assert(len(results) == 1)

    def testNoRegex(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setText('Test TestTest')
        path = ['/'.join(doc1.getPhysicalPath())]
        results = self.srtool.searchAndReplace(self.request,
                                               path,
                                               '\\bTest\\b',
                                               'text',
                                               'foo',
                                               useRegex=False,
                                               preview=True)
        
        assert(len(results) == 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testRegex))
    return suite
