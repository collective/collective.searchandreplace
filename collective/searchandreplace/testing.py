from pkg_resources import get_distribution
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from plone.testing import z2


PLONE_VERSION = get_distribution('Products.CMFPlone').version
MAJOR_PLONE_VERSION = int(PLONE_VERSION[0])


class SearchReplaceLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import collective.searchandreplace
        self.loadZCML(package=collective.searchandreplace)
        z2.installProduct(app, 'collective.searchandreplace')
        if MAJOR_PLONE_VERSION >= 5:
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)

    def setUpPloneSite(self, portal):
        if MAJOR_PLONE_VERSION >= 5:
            applyProfile(portal, 'plone.app.contenttypes:default')
            # Ah we need to apply our dexterity profile!
            applyProfile(portal, 'collective.searchandreplace:dexterity')
        applyProfile(portal, 'collective.searchandreplace:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        create_doc(portal, text=u'Get Plone now')
        setRoles(portal, TEST_USER_ID, ['Member'])


SEARCH_REPLACE_FIXTURE = SearchReplaceLayer()
SEARCH_REPLACE_INTEGRATION_LAYER = IntegrationTesting(
    bases=(SEARCH_REPLACE_FIXTURE, ),
    name='SearchReplaceLayer:Integration')
SEARCH_REPLACE_FUNCTIONAL_LAYER = FunctionalTesting(
    bases=(SEARCH_REPLACE_FIXTURE, ),
    name='SearchReplaceLayer:Functional')


def create_doc(container, id='page', title=u'Title of page', text=u''):
    if MAJOR_PLONE_VERSION >= 5:
        # dexterity text field
        from plone.app.textfield.value import RichTextValue
        text = RichTextValue(
            raw=text,
            mimeType='text/html',
            outputMimeType='text/html',
        )
    api.content.create(container, 'Document', id=id, title=title,
                       text=text)


def edit_content(context, title=None, description=None, text=None):
    if MAJOR_PLONE_VERSION >= 5:
        if title is not None:
            context.title = title
        if description is not None:
            context.description = description
        if text is not None:
            # dexterity text field
            from plone.app.textfield.value import RichTextValue
            text = RichTextValue(
                raw=text,
                mimeType='text/html',
                outputMimeType='text/html',
            )
            context.text = text
    else:
        if title is not None:
            context.setTitle(title)
        if description is not None:
            context.setDescription(description)
        if text is not None:
            context.setText(text)
