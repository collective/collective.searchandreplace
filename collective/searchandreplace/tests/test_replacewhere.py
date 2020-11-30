# -*- coding: utf-8 -*-
from collective.searchandreplace.interfaces import ISearchReplaceUtility
from collective.searchandreplace.interfaces import ISearchReplaceSettings
from collective.searchandreplace.testing import edit_content
from collective.searchandreplace.testing import SEARCH_REPLACE_INTEGRATION_LAYER  # noqa
from plone.registry.interfaces import IRegistry
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
import six

import unittest


class TestReplaceWhere(unittest.TestCase):
    """Ensure that we can replace in title, description and text."""

    layer = SEARCH_REPLACE_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer["portal"]
        self.srutil = getUtility(ISearchReplaceUtility)

    def testReplaceText(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(
            doc1, title="Find Title", description="Find Description", text="Find Case"
        )
        self.assertEqual(getRawText(doc1), "Find Case")
        # Search it.
        parameters = dict(context=doc1, findWhat="find case", matchCase=False)
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 1)
        self.assertEqual(getRawText(doc1), "Find Case")
        r_parameters = dict(
            replaceWith="replaced",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        # Note: replacing returns an int, not a list.
        self.assertEqual(results, 1)
        self.assertEqual(getRawText(doc1), "replaced")
        # Other fields are not changed.
        self.assertEqual(doc1.Title(), "Find Title")
        self.assertEqual(doc1.Description(), "Find Description")

    def testReplaceTitle(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc2")
        doc1 = getattr(self.portal, "doc2")
        edit_content(
            doc1, title="Find Title", description="Find Description", text="Find Case"
        )
        self.assertEqual(doc1.Title(), "Find Title")
        # Search it.
        parameters = dict(context=doc1, findWhat="find title", matchCase=False)
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 1)
        self.assertEqual(doc1.Title(), "Find Title")
        r_parameters = dict(
            replaceWith="replaced",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        self.assertEqual(results, 1)
        self.assertEqual(doc1.Title(), "replaced")
        # Other fields are not changed.
        self.assertEqual(doc1.Description(), "Find Description")
        self.assertEqual(getRawText(doc1), "Find Case")

    def testReplaceDescription(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(
            doc1, title="Find Title", description="Find Description", text="Find Case"
        )
        self.assertEqual(doc1.Description(), "Find Description")
        # Search it.
        parameters = dict(context=doc1, findWhat="find desc", matchCase=False)
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 1)
        self.assertEqual(doc1.Description(), "Find Description")

        r_parameters = dict(
            replaceWith="replaced",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        self.assertEqual(results, 1)
        # Note: we have replaced only part of the description.
        self.assertEqual(doc1.Description(), "replacedription")

        # Other fields are not changed.
        self.assertEqual(doc1.Title(), "Find Title")
        self.assertEqual(getRawText(doc1), "Find Case")

    def testReplaceOnlyEditableContent(self):
        # setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.layer["app"], SITE_OWNER_NAME)
        # /mainfolder
        self.portal.invokeFactory("Folder", "mainfolder")
        mainfolder = getattr(self.portal, "mainfolder")
        edit_content(mainfolder, title="Find Title")

        # /mainfolder/maindoc
        mainfolder.invokeFactory("Document", "maindoc")
        maindoc = getattr(mainfolder, "maindoc")
        edit_content(maindoc, title="Find Title")

        # /mainfolder/subfolder
        mainfolder.invokeFactory("Folder", "subfolder")
        subfolder = getattr(mainfolder, "subfolder")
        edit_content(subfolder, title="Find Title")

        # /mainfolder/subfolder/subdoc
        subfolder.invokeFactory("Document", "subdoc")
        subdoc = getattr(subfolder, "subdoc")
        edit_content(subdoc, title="Find Title")

        # Give test user a local Editor role on the sub folder.
        subfolder.manage_addLocalRoles(TEST_USER_ID, ("Editor",))

        self.portal.portal_catalog.reindexObject(mainfolder)
        self.portal.portal_catalog.reindexObject(maindoc)
        self.portal.portal_catalog.reindexObject(subfolder)
        self.portal.portal_catalog.reindexObject(subdoc)

        # We are logged in as portal owner, so we can edit everything.
        results = self.srutil.findObjects(mainfolder, "find title", matchCase=False)
        self.assertEqual(len(results), 4)

        # Login as the test user again.
        logout()
        login(self.portal, TEST_USER_NAME)
        # Now we can edit less: only the sub folder and sub doc.
        parameters = dict(context=mainfolder, findWhat="find title", matchCase=False)
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 2)
        paths = [x["path"] for x in results]
        self.assertIn("/".join(subfolder.getPhysicalPath()), paths)
        self.assertIn("/".join(subdoc.getPhysicalPath()), paths)
        self.assertNotIn("/".join(mainfolder.getPhysicalPath()), paths)
        self.assertNotIn("/".join(maindoc.getPhysicalPath()), paths)

        # Nothing has been changed, because we were only searching.
        self.assertEqual(mainfolder.Title(), "Find Title")
        self.assertEqual(maindoc.Title(), "Find Title")
        self.assertEqual(subfolder.Title(), "Find Title")
        self.assertEqual(subfolder.Title(), "Find Title")

        r_parameters = dict(
            replaceWith="replaced",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        self.assertEqual(results, 2)
        self.assertEqual(mainfolder.Title(), "Find Title")
        self.assertEqual(maindoc.Title(), "Find Title")
        self.assertEqual(subfolder.Title(), "replaced")
        self.assertEqual(subfolder.Title(), "replaced")

    def testReplaceTextFieldsButNotTextlineFields(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchReplaceSettings, check=False)
        settings.include_textline_fields = False

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # Note: we use our sample type here, which has extra fields.
        # This currently is Archetypes when testing on Plone 4,
        # and Dexterity when testing on Plone 5.
        self.portal.invokeFactory("SampleType", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(
            doc1,
            title="Find Title",
            description="Find Description",
            rich="Find Rich",
            plain="Find Plain",
            line="Find Line",
            unsearchable="Find Unsearchable",
        )

        # Test the initial values.
        self.assertEqual(doc1.Title(), "Find Title")
        self.assertEqual(doc1.Description(), "Find Description")
        self.assertEqual(getRawText(doc1, "rich"), "Find Rich")
        self.assertEqual(getRawText(doc1, "plain"), "Find Plain")
        self.assertEqual(getRawText(doc1, "line"), "Find Line")
        self.assertEqual(getRawText(doc1, "unsearchable"), "Find Unsearchable")

        # Search it.
        parameters = dict(context=doc1, findWhat="Find", matchCase=False)
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 5)

        # Nothing should have changed.
        self.assertEqual(doc1.Title(), "Find Title")
        self.assertEqual(doc1.Description(), "Find Description")
        self.assertEqual(getRawText(doc1, "rich"), "Find Rich")
        self.assertEqual(getRawText(doc1, "plain"), "Find Plain")
        self.assertEqual(getRawText(doc1, "line"), "Find Line")
        self.assertEqual(getRawText(doc1, "unsearchable"), "Find Unsearchable")

        r_parameters = dict(
            replaceWith="Foo",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        self.assertEqual(results, 5)

        # Most fields should have changed.
        self.assertEqual(doc1.Title(), "Foo Title")
        self.assertEqual(doc1.Description(), "Foo Description")
        self.assertEqual(getRawText(doc1, "rich"), "Foo Rich")
        self.assertEqual(getRawText(doc1, "plain"), "Foo Plain")
        self.assertEqual(getRawText(doc1, "unsearchable"), "Foo Unsearchable")

        # But not the textline field.
        self.assertEqual(getRawText(doc1, "line"), "Find Line")

    def testReplaceAllFields(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # Note: we use our sample type here, which has extra fields.
        # This currently is Archetypes when testing on Plone 4,
        # and Dexterity when testing on Plone 5.
        self.portal.invokeFactory("SampleType", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(
            doc1,
            title="Find Title",
            description="Find Description",
            rich="Find Rich",
            plain="Find Plain",
            line="Find Line",
            unsearchable="Find Unsearchable",
        )

        # Test the initial values.
        self.assertEqual(doc1.Title(), "Find Title")
        self.assertEqual(doc1.Description(), "Find Description")
        self.assertEqual(getRawText(doc1, "rich"), "Find Rich")
        self.assertEqual(getRawText(doc1, "plain"), "Find Plain")
        self.assertEqual(getRawText(doc1, "line"), "Find Line")
        self.assertEqual(getRawText(doc1, "unsearchable"), "Find Unsearchable")

        # Search it.
        parameters = dict(context=doc1, findWhat="Find", matchCase=False)
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 6)

        # Nothing should have changed.
        self.assertEqual(doc1.Title(), "Find Title")
        self.assertEqual(doc1.Description(), "Find Description")
        self.assertEqual(getRawText(doc1, "rich"), "Find Rich")
        self.assertEqual(getRawText(doc1, "plain"), "Find Plain")
        self.assertEqual(getRawText(doc1, "line"), "Find Line")
        self.assertEqual(getRawText(doc1, "unsearchable"), "Find Unsearchable")

        r_parameters = dict(
            replaceWith="Foo",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        self.assertEqual(results, 6)

        # All fields should have changed.
        self.assertEqual(doc1.Title(), "Foo Title")
        self.assertEqual(doc1.Description(), "Foo Description")
        self.assertEqual(getRawText(doc1, "rich"), "Foo Rich")
        self.assertEqual(getRawText(doc1, "plain"), "Foo Plain")
        self.assertEqual(getRawText(doc1, "unsearchable"), "Foo Unsearchable")

        # including the textline field.
        self.assertEqual(getRawText(doc1, "line"), "Foo Line")

    def testReplaceUnsearchableTextFields(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # Note: we use our sample type here, which has extra fields.
        # This currently is Archetypes when testing on Plone 4,
        # and Dexterity when testing on Plone 5.
        self.portal.invokeFactory("SampleType", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(
            doc1,
            title="Find Title",
            unsearchable="Find Unsearchable",
        )

        # Test the initial values.
        self.assertEqual(doc1.Title(), "Find Title")
        self.assertEqual(getRawText(doc1, "unsearchable"), "Find Unsearchable")

        # Search it with onlySearchableText true.
        parameters = dict(
            context=doc1,
            findWhat="Unsearchable",
            onlySearchableText=True,
            matchCase=False,
        )
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 0)

        # Replace it with onlySearchableText true.
        r_parameters = dict(
            replaceWith="Foo",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        self.assertEqual(results, 0)

        # Nothing should have changed.
        self.assertEqual(getRawText(doc1, "unsearchable"), "Find Unsearchable")

        # Now search everything, so onlySearchableText false.
        parameters["onlySearchableText"] = False
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 1)

        # Nothing should have changed.
        self.assertEqual(getRawText(doc1, "unsearchable"), "Find Unsearchable")

        # Replace it.
        r_parameters["onlySearchableText"] = False
        results = self.srutil.replaceAllMatches(**r_parameters)
        self.assertEqual(results, 1)
        self.assertEqual(getRawText(doc1, "unsearchable"), "Find Foo")

    def testReplaceRawHTML(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(doc1, title="Find Title", text="My <strong>Test</strong> Case")
        self.assertEqual(getRawText(doc1), "My <strong>Test</strong> Case")

        # Search only in SearchableText.
        parameters = dict(
            context=doc1,
            findWhat="<strong>Test</strong>",
            onlySearchableText=True,
            matchCase=False,
        )
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 0)

        # Search everywhere.
        parameters["onlySearchableText"] = False
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 1)
        self.assertEqual(getRawText(doc1), "My <strong>Test</strong> Case")

        r_parameters = dict(
            replaceWith="<em>Test</em>",
        )
        r_parameters.update(parameters)
        # Replace it.
        results = self.srutil.replaceAllMatches(**r_parameters)
        # Note: replacing returns an int, not a list.
        self.assertEqual(results, 1)
        self.assertEqual(getRawText(doc1), "My <em>Test</em> Case")

    def testDoNotFindSubject(self):

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(doc1, title="Find Title", subject=("Find subject", "Replace"))
        self.assertEqual(doc1.Subject(), ("Find subject", "Replace"))
        # Search it.
        parameters = dict(
            context=doc1,
            findWhat="find subject",
            matchCase=False,
            onlySearchableText=True,
        )
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 0)

    def testReplaceSubject(self):

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchReplaceSettings, check=False)
        settings.include_lines_fields = True

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(doc1, title="Find Title", subject=("Find subject", "Replace"))
        self.assertEqual(doc1.Subject(), ("Find subject", "Replace"))
        # Search it.
        parameters = dict(
            context=doc1,
            findWhat="find subject",
            matchCase=False,
            onlySearchableText=True,
        )
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 1)
        r_parameters = dict(
            replaceWith="replaced",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        # Note: replacing returns an int, not a list.
        self.assertEqual(results, 1)
        self.assertEqual(doc1.Subject(), ("replaced", "Replace"))
        # Other fields are not changed.
        self.assertEqual(doc1.Title(), "Find Title")

    def testReplaceSubjectSecondItem(self):

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchReplaceSettings, check=False)
        settings.include_lines_fields = True

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(
            doc1, title="Find Title", subject=("Replace", "Find subject", "Replace")
        )
        self.assertEqual(doc1.Subject(), ("Replace", "Find subject", "Replace"))
        # Search it.
        parameters = dict(
            context=doc1,
            findWhat="find subject",
            matchCase=False,
            onlySearchableText=True,
        )
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 1)
        r_parameters = dict(
            replaceWith="replaced",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        # Note: replacing returns an int, not a list.
        self.assertEqual(results, 1)
        self.assertEqual(doc1.Subject(), ("Replace", "replaced", "Replace"))
        # Other fields are not changed.
        self.assertEqual(doc1.Title(), "Find Title")

    def testReplaceSubjectTwiceInThirdItem(self):

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchReplaceSettings, check=False)
        settings.include_lines_fields = True

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(
            doc1,
            title="Find Title",
            subject=("Replace", "Replace", "Find subject find subject"),
        )
        self.assertEqual(
            doc1.Subject(), ("Replace", "Replace", "Find subject find subject")
        )
        # Search it.
        parameters = dict(
            context=doc1,
            findWhat="find subject",
            matchCase=False,
            onlySearchableText=True,
        )
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 2)
        r_parameters = dict(
            replaceWith="replaced",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        # Note: replacing returns an int, not a list.
        self.assertEqual(results, 2)
        self.assertEqual(doc1.Subject(), ("Replace", "Replace", "replaced replaced"))
        # Other fields are not changed.
        self.assertEqual(doc1.Title(), "Find Title")

    def testReplaceSubjectUnicode(self):

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchReplaceSettings, check=False)
        settings.include_lines_fields = True

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(
            doc1, title="Find Title", subject=("Find subject", "Remplac\xc3\xa9")
        )
        self.assertEqual(doc1.Subject(), ("Find subject", "Remplac\xc3\xa9"))
        # Search it.
        parameters = dict(
            context=doc1,
            findWhat="find subject",
            matchCase=False,
            onlySearchableText=True,
        )
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 1)
        r_parameters = dict(
            replaceWith="replaced",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        # Note: replacing returns an int, not a list.
        self.assertEqual(results, 1)
        self.assertEqual(doc1.Subject(), ("replaced", "Remplac\xc3\xa9"))
        # Other fields are not changed.
        self.assertEqual(doc1.Title(), "Find Title")

        edit_content(doc1, title="Find Title", subject=("Find subject", "Replaced"))
        self.assertEqual(doc1.Subject(), ("Find subject", "Replaced"))
        # Search it.
        parameters = dict(
            context=doc1,
            findWhat="find subject",
            matchCase=False,
            onlySearchableText=True,
        )
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 1)
        r_parameters = dict(
            replaceWith=u"Remplacé",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        self.assertEqual(results, 1)
        if six.PY3:
            self.assertEqual(doc1.Subject(), (u"Remplacé", "Replaced"))
        if six.PY2:
            self.assertEqual(doc1.Subject(), (u"Remplacé".encode("utf8"), "Replaced"))

    def testReplaceEmpty(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(
            doc1,
            title="Find My Title",
            description="Find My Description",
            text="Find My Text",
        )
        self.assertEqual(getRawText(doc1), "Find My Text")
        # Search it.
        parameters = dict(context=doc1, findWhat=" My", matchCase=False)
        results = self.srutil.findObjects(**parameters)
        self.assertEqual(len(results), 3)
        self.assertEqual(getRawText(doc1), "Find My Text")
        r_parameters = dict(
            replaceWith="",
        )
        r_parameters.update(parameters)
        results = self.srutil.replaceAllMatches(**r_parameters)
        # Note: replacing returns an int, not a list.
        self.assertEqual(results, 3)
        self.assertEqual(getRawText(doc1), "Find Text")
        self.assertEqual(doc1.Title(), "Find Title")
        self.assertEqual(doc1.Description(), "Find Description")


class TestModified(unittest.TestCase):
    """Test update_modified setting"""

    layer = SEARCH_REPLACE_INTEGRATION_LAYER

    def setUp(self):
        self.portal = self.layer["portal"]
        self.srutil = getUtility(ISearchReplaceUtility)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc1")
        doc1 = getattr(self.portal, "doc1")
        edit_content(
            doc1, title="Find Title", description="Find Description", text="Find Case"
        )
        # when an object has never been saved to repository
        # any call to save to repository, like in _afterReplace,
        # triggers a change in the modification date
        # for this reason, save the document to avoid noise when testing
        # modification date
        repository = getToolByName(self.portal, "portal_repository", None)
        repository.save(doc1)

    def test_update_modified(self):
        doc1 = getattr(self.portal, "doc1")
        modified = doc1.modified()
        self.replace()
        self.assertNotEqual(doc1.modified(), modified)

    def test_update_not_modified(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchReplaceSettings, check=False)
        settings.update_modified = False
        doc1 = getattr(self.portal, "doc1")
        modified = doc1.modified()
        self.replace()
        self.assertEqual(doc1.modified(), modified)

    def replace(self):
        from collective.searchandreplace.searchreplaceutility import getRawText

        doc1 = getattr(self.portal, "doc1")
        self.assertEqual(getRawText(doc1), "Find Case")
        # Replace it after 1 second to ensure different modified date
        import time

        time.sleep(1)
        replace_parameters = dict(
            context=doc1, findWhat="find case", replaceWith="replaced", matchCase=False
        )
        results = self.srutil.replaceAllMatches(**replace_parameters)
        self.assertEqual(results, 1)
        self.assertEqual(getRawText(doc1), "replaced")
