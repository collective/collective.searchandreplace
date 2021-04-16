from pkg_resources import get_distribution
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from plone.testing import z2


PLONE_VERSION = get_distribution("Products.CMFPlone").version
MAJOR_PLONE_VERSION = int(PLONE_VERSION[0])


class SearchReplaceLayer(PloneSandboxLayer):
    def setUpZope(self, app, configurationContext):
        import collective.searchandreplace

        self.loadZCML(package=collective.searchandreplace)
        self.loadZCML("testing.zcml", package=collective.searchandreplace)
        if MAJOR_PLONE_VERSION >= 5:
            import plone.app.contenttypes

            self.loadZCML(package=plone.app.contenttypes)
            import collective.dexteritytextindexer

            self.loadZCML(package=collective.dexteritytextindexer)
        else:
            # Needed for our Archetypes SampleType.
            z2.installProduct(app, "collective.searchandreplace")

    def setUpPloneSite(self, portal):
        if MAJOR_PLONE_VERSION >= 5:
            applyProfile(portal, "plone.app.contenttypes:default")
            applyProfile(portal, "collective.searchandreplace:testing-dexterity")
        else:
            applyProfile(portal, "collective.searchandreplace:testing-archetypes")

        applyProfile(portal, "collective.searchandreplace:default")
        setRoles(portal, TEST_USER_ID, ["Manager"])
        create_doc(portal, text=u"Get Plone now", title=u"Plone", description=u"Plone")
        setRoles(portal, TEST_USER_ID, ["Member"])


SEARCH_REPLACE_FIXTURE = SearchReplaceLayer()
SEARCH_REPLACE_INTEGRATION_LAYER = IntegrationTesting(
    bases=(SEARCH_REPLACE_FIXTURE,), name="SearchReplaceLayer:Integration"
)
SEARCH_REPLACE_FUNCTIONAL_LAYER = FunctionalTesting(
    bases=(SEARCH_REPLACE_FIXTURE,), name="SearchReplaceLayer:Functional"
)


def rich_text(text):
    if MAJOR_PLONE_VERSION < 5:
        # Use standard Archetypes field.
        return text
    # Use dexterity text field.
    from plone.app.textfield.value import RichTextValue

    return RichTextValue(
        raw=text,
        mimeType="text/html",
        outputMimeType="text/html",
    )


def create_doc(container, id="page", title=u"Title of page", text=u"", description=u""):
    text = rich_text(text)
    api.content.create(container, "Document", id=id, title=title, text=text, description=description)


def edit_content(
    context,
    title=None,
    description=None,
    text=None,
    rich=None,
    plain=None,
    line=None,
    unsearchable=None,
    subject=None,
):
    if MAJOR_PLONE_VERSION >= 5:
        # Dexterity
        if title is not None:
            context.title = title
        if description is not None:
            context.description = description
        if text is not None:
            context.text = rich_text(text)
        if rich is not None:
            context.rich = rich_text(rich)
        if plain is not None:
            context.plain = plain
        if line is not None:
            context.line = line
        if unsearchable is not None:
            context.unsearchable = rich_text(unsearchable)
        if subject is not None:
            context.subject = subject
    else:
        # Archetypes
        if title is not None:
            context.setTitle(title)
        if description is not None:
            context.setDescription(description)
        if text is not None:
            context.setText(text)
        if rich is not None:
            context.setRich(rich)
        if plain is not None:
            context.setPlain(plain)
        if line is not None:
            context.setLine(line)
        if unsearchable is not None:
            context.setUnsearchable(unsearchable)
        if subject is not None:
            context.setSubject(subject)
    context.reindexObject()
