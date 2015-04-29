from Products.CMFPlone.tests.PloneTestCase import default_user
from collective.searchandreplace.interfaces import ISearchReplaceUtility
from collective.searchandreplace.tests.base import SearchAndReplaceTestCase
from zope.component import getUtility


class testReplaceWhere(SearchAndReplaceTestCase):
    """Ensure that we can replace in title, description and text."""

    def afterSetUp(self):
        self.srutil = getUtility(ISearchReplaceUtility)

    def testReplaceText(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setDescription('Test Description')
        doc1.setText('Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test case',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testReplaceTitle(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc2')
        doc1 = getattr(self.portal, 'doc2')
        doc1.setTitle('Test Title')
        doc1.setDescription('Test Description')
        doc1.setText('Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test title',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testReplaceDescription(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setDescription('Test Description')
        doc1.setText('Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test desc',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testReplaceOnlyEditableContent(self):
        self.loginAsPortalOwner()
        # /mainfolder
        self.portal.invokeFactory('Folder', 'mainfolder')
        mainfolder = getattr(self.portal, 'mainfolder')
        mainfolder.setTitle('Test Title')

        # /mainfolder/maindoc
        mainfolder.invokeFactory('Document', 'maindoc')
        maindoc = getattr(mainfolder, 'maindoc')
        maindoc.setTitle('Test Title')

        # /mainfolder/subfolder
        mainfolder.invokeFactory('Folder', 'subfolder')
        subfolder = getattr(mainfolder, 'subfolder')
        subfolder.setTitle('Test Title')

        # /mainfolder/subfolder/subdoc
        subfolder.invokeFactory('Document', 'subdoc')
        subdoc = getattr(subfolder, 'subdoc')
        subdoc.setTitle('Test Title')

        # Give test user a local Editor role on the sub folder.
        subfolder.manage_addLocalRoles(default_user, ('Editor',))

        # We are logged in as portal owner, so we can edit everything.
        results = self.srutil.searchObjects(
            mainfolder,
            'test title',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 4)

        # Login as the test user again.
        self.logout()
        self.login()
        # Now we can edit less: only the sub folder and sub doc.
        results = self.srutil.searchObjects(
            mainfolder,
            'test title',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 2)
        paths = [x['path'] for x in results]
        self.assertIn('/'.join(subfolder.getPhysicalPath()), paths)
        self.assertIn('/'.join(subdoc.getPhysicalPath()), paths)
        self.assertNotIn('/'.join(mainfolder.getPhysicalPath()), paths)
        self.assertNotIn('/'.join(maindoc.getPhysicalPath()), paths)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testReplaceWhere))
    return suite
