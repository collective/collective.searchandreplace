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
        from collective.searchandreplace.searchreplaceutility import getRawText
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        edit_content(
            doc1,
            title='Test Title',
            description='Test Description',
            text='Test Case')
        self.assertEqual(getRawText(doc1), 'Test Case')
        # Search it.
        parameters = dict(
            context=doc1,
            find='test case',
            replaceText='foo',
            matchCase=False)
        results = self.srutil.searchObjects(**parameters)
        self.assertEqual(len(results), 1)
        self.assertEqual(getRawText(doc1), 'Test Case')
        # Replace it.
        parameters['doReplace'] = True
        results = self.srutil.searchObjects(**parameters)
        # Note: replacing returns an int, not a list.
        self.assertEqual(results, 1)
        self.assertEqual(getRawText(doc1), 'foo')
        # Other fields are not changed.
        self.assertEqual(doc1.Title(), 'Test Title')
        self.assertEqual(doc1.Description(), 'Test Description')

    def testReplaceTitle(self):
        from collective.searchandreplace.searchreplaceutility import getRawText
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'doc2')
        doc1 = getattr(self.portal, 'doc2')
        edit_content(
            doc1,
            title='Test Title',
            description='Test Description',
            text='Test Case')
        self.assertEqual(doc1.Title(), 'Test Title')
        # Search it.
        parameters = dict(
            context=doc1,
            find='test title',
            replaceText='foo',
            matchCase=False)
        results = self.srutil.searchObjects(**parameters)
        self.assertEqual(len(results), 1)
        self.assertEqual(doc1.Title(), 'Test Title')
        # Replace it.
        parameters['doReplace'] = True
        results = self.srutil.searchObjects(**parameters)
        self.assertEqual(results, 1)
        self.assertEqual(doc1.Title(), 'foo')
        # Other fields are not changed.
        self.assertEqual(doc1.Description(), 'Test Description')
        self.assertEqual(getRawText(doc1), 'Test Case')

    def testReplaceDescription(self):
        from collective.searchandreplace.searchreplaceutility import getRawText
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        edit_content(
            doc1,
            title='Test Title',
            description='Test Description',
            text='Test Case')
        self.assertEqual(doc1.Description(), 'Test Description')
        # Search it.
        parameters = dict(
            context=doc1,
            find='test desc',
            replaceText='foo',
            matchCase=False)
        results = self.srutil.searchObjects(**parameters)
        self.assertEqual(len(results), 1)
        self.assertEqual(doc1.Description(), 'Test Description')

        # Replace it.
        parameters['doReplace'] = True
        results = self.srutil.searchObjects(**parameters)
        self.assertEqual(results, 1)
        # Note: we have replaced only part of the description.
        self.assertEqual(doc1.Description(), 'fooription')

        # Other fields are not changed.
        self.assertEqual(doc1.Title(), 'Test Title')
        self.assertEqual(getRawText(doc1), 'Test Case')

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
        parameters = dict(
            context=mainfolder,
            find='test title',
            replaceText='foo',
            matchCase=False)
        results = self.srutil.searchObjects(**parameters)
        self.assertEqual(len(results), 2)
        paths = [x['path'] for x in results]
        self.assertIn('/'.join(subfolder.getPhysicalPath()), paths)
        self.assertIn('/'.join(subdoc.getPhysicalPath()), paths)
        self.assertNotIn('/'.join(mainfolder.getPhysicalPath()), paths)
        self.assertNotIn('/'.join(maindoc.getPhysicalPath()), paths)

        # Nothing has been changed, because we were only searching.
        self.assertEqual(mainfolder.Title(), 'Test Title')
        self.assertEqual(maindoc.Title(), 'Test Title')
        self.assertEqual(subfolder.Title(), 'Test Title')
        self.assertEqual(subfolder.Title(), 'Test Title')

        # Now replace instead of only searching.
        parameters['doReplace'] = True
        results = self.srutil.searchObjects(**parameters)
        self.assertEqual(results, 2)
        self.assertEqual(mainfolder.Title(), 'Test Title')
        self.assertEqual(maindoc.Title(), 'Test Title')
        self.assertEqual(subfolder.Title(), 'foo')
        self.assertEqual(subfolder.Title(), 'foo')

    def testReplaceAllTextFields(self):
        from collective.searchandreplace.searchreplaceutility import getRawText
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Note: we use are sample type here, which has extra fields.
        # This currently is Archetypes when testing on Plone 4,
        # and Dexterity when testing on Plone 5.
        self.portal.invokeFactory('SampleType', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        edit_content(
            doc1,
            title='Test Title',
            description='Test Description',
            rich='Test Rich',
            plain='Test Plain',
            line='Test Line')

        # Test the initial values.
        self.assertEqual(doc1.Title(), 'Test Title')
        self.assertEqual(doc1.Description(), 'Test Description')
        self.assertEqual(getRawText(doc1, 'rich'), 'Test Rich')
        self.assertEqual(getRawText(doc1, 'plain'), 'Test Plain')
        self.assertEqual(getRawText(doc1, 'line'), 'Test Line')

        # Search it.
        parameters = dict(
            context=doc1,
            find='Test',
            replaceText='Foo',
            matchCase=False)
        results = self.srutil.searchObjects(**parameters)
        self.assertEqual(len(results), 4)

        # Nothing should have changed.
        self.assertEqual(doc1.Title(), 'Test Title')
        self.assertEqual(doc1.Description(), 'Test Description')
        self.assertEqual(getRawText(doc1, 'rich'), 'Test Rich')
        self.assertEqual(getRawText(doc1, 'plain'), 'Test Plain')
        self.assertEqual(getRawText(doc1, 'line'), 'Test Line')

        # Replace it.
        parameters['doReplace'] = True
        results = self.srutil.searchObjects(**parameters)
        self.assertEqual(results, 4)

        # Most fields should have changed.
        self.assertEqual(doc1.Title(), 'Foo Title')
        self.assertEqual(doc1.Description(), 'Foo Description')
        self.assertEqual(getRawText(doc1, 'rich'), 'Foo Rich')
        self.assertEqual(getRawText(doc1, 'plain'), 'Foo Plain')

        # But not the textline field.
        self.assertEqual(getRawText(doc1, 'line'), 'Test Line')
