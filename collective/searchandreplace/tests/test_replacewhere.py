from collective.searchandreplace.interfaces import ISearchReplaceUtility
from collective.searchandreplace.testing import edit_content
from collective.searchandreplace.testing import SEARCH_REPLACE_INTEGRATION_LAYER  # noqa
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.component import getUtility

import unittest


class TestReplaceWhere(unittest.TestCase):
    """Ensure that we can replace in title, description and text."""

    layer = SEARCH_REPLACE_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer['portal']
        self.srutil = getUtility(ISearchReplaceUtility)

    def testReplaceText(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        edit_content(
            doc1,
            title='Test Title',
            description='Test Description',
            text='Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test case',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testReplaceTitle(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'doc2')
        doc1 = getattr(self.portal, 'doc2')
        edit_content(
            doc1,
            title='Test Title',
            description='Test Description',
            text='Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test title',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testReplaceDescription(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        edit_content(
            doc1,
            title='Test Title',
            description='Test Description',
            text='Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test desc',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testReplaceOnlyEditableContent(self):
        # setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.layer['app'], SITE_OWNER_NAME)
        # /mainfolder
        self.portal.invokeFactory('Folder', 'mainfolder')
        mainfolder = getattr(self.portal, 'mainfolder')
        edit_content(mainfolder, title='Test Title')

        # /mainfolder/maindoc
        mainfolder.invokeFactory('Document', 'maindoc')
        maindoc = getattr(mainfolder, 'maindoc')
        edit_content(maindoc, title='Test Title')

        # /mainfolder/subfolder
        mainfolder.invokeFactory('Folder', 'subfolder')
        subfolder = getattr(mainfolder, 'subfolder')
        edit_content(subfolder, title='Test Title')

        # /mainfolder/subfolder/subdoc
        subfolder.invokeFactory('Document', 'subdoc')
        subdoc = getattr(subfolder, 'subdoc')
        edit_content(subdoc, title='Test Title')

        # Give test user a local Editor role on the sub folder.
        subfolder.manage_addLocalRoles(TEST_USER_ID, ('Editor',))

        self.portal.portal_catalog.reindexObject(mainfolder)
        self.portal.portal_catalog.reindexObject(maindoc)
        self.portal.portal_catalog.reindexObject(subfolder)
        self.portal.portal_catalog.reindexObject(subdoc)

        # We are logged in as portal owner, so we can edit everything.
        results = self.srutil.searchObjects(
            mainfolder,
            'test title',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 4)

        # Login as the test user again.
        logout()
        login(self.portal, TEST_USER_NAME)
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
