# -*- coding: us-ascii -*-
from Acquisition import aq_parent
from collective.searchandreplace import SearchAndReplaceMessageFactory as _
from collective.searchandreplace.browser.customwidgets import TwoLineTextAreaWidget  # noqa
from collective.searchandreplace.interfaces import ISearchReplaceUtility
from five.formlib.formbase import AddForm
from plone.app.layout.navigation.defaultpage import isDefaultPage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getUtility
from zope.formlib.form import action
from zope.formlib.form import FormFields
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import Int
from zope.schema import Text


def validate_searchreplaceform(form, action, data):
    """ Validate the Search/Replace form. """


class ISearchReplaceForm(Interface):
    """ Interface for Search and Replace form """

    findWhat = Text(
        title=_(u'Find What'),
        description=_(u'Enter the text to find.'),
        required=True)

    replaceWith = Text(
        title=_(u'Replace With'),
        description=_(u'Enter the text to replace the original text with.'),
        required=False)

    maxResults = Int(
        title=_(u'Maximum Number of Results'),
        description=_(
            u'Maximum number of results to show. '
            'Warning: this has no effect on how many found texts are '
            'replaced when you use the Replace button directly without '
            'using the Preview.'),
        default=None,
        required=False)

    searchSubfolders = Bool(
        title=_(u'Search Subfolders'),
        description=_(
            u'If checked, this will recursively search '
            'through any selected folders and their '
            'children, replacing at each level.'),
        default=True,
        required=True)

    matchCase = Bool(
        title=_(u'Match Case'),
        description=_(u'Check the box for a case sensitive search.'),
        default=False,
        required=True)

    onlySearchableText = Bool(
        title=_(u'Fast search'),
        description=_(
            u'Use the catalog to search, just like the search form does. '
            'This only finds keywords, not html tags. '
            'You might have some text fields that are not found this way, '
            'so if not checked, you may find more content, '
            'but it will be slower. '
            'Regardless of this setting, when at least one match is found, '
            'text in all text fields may be replaced.'),
        required=False,
        default=True,
    )


class SearchReplaceForm(AddForm):
    """ """

    @property
    def form_fields(self):
        form_fields = FormFields(ISearchReplaceForm)
        container = aq_parent(self.context)
        if not self.context.isPrincipiaFolderish and not isDefaultPage(
                container, self.context):
            form_fields = form_fields.omit('searchSubfolders')
        form_fields['findWhat'].custom_widget = TwoLineTextAreaWidget
        form_fields['replaceWith'].custom_widget = TwoLineTextAreaWidget
        return form_fields

    label = _(u'Search and Replace')
    description = _(u'Search and replace text found in documents.')
    template = ViewPageTemplateFile('pageform.pt')

    @action(_(u'Preview'),
            validator=None,
            name=u'Preview')
    def action_preview(self, action, data):
        """ Preview files to be changed. """
        self.form_reset = False

    @action(_(u'Replace'),
            validator=validate_searchreplaceform,
            name=u'Replace')
    def action_replace(self, action, data):
        """ Replace text for all files. """
        self.form_reset = False
        srutil = getUtility(ISearchReplaceUtility)
        if 'form.affectedContent' in self.request:
            # Do only the selected items
            # nitems = len(self.request['form.affectedContent'])
            items = srutil.parseItems(self.request['form.affectedContent'])
            nitems = 0
            for page_url, page_result in items.items():
                for field, indexes in page_result.items():
                    nitems += len(indexes)
            replaced = srutil.searchObjects(
                self.context,
                data['findWhat'],
                searchSubFolders=data.get('searchSubfolders', False),
                matchCase=data['matchCase'],
                replaceText=data['replaceWith'],
                doReplace=True,
                searchItems=items,
                onlySearchableText=data['onlySearchableText'],
            )
            IStatusMessage(self.request).addStatusMessage(
                _(u'Search text replaced in ${replaced} of ${items} '
                  'instance(s).',
                  mapping={'replaced': replaced, 'items': nitems}),
                type='info')
        else:
            # Do everything you can find
            replaced = srutil.searchObjects(
                self.context,
                data['findWhat'],
                searchSubFolders=data.get('searchSubfolders', False),
                matchCase=data['matchCase'],
                replaceText=data['replaceWith'],
                onlySearchableText=data['onlySearchableText'],
                doReplace=True)
            IStatusMessage(self.request).addStatusMessage(
                _(u'Search text replaced in all ${items} instance(s).',
                  mapping={'items': replaced}),
                type='info')

    @action(_(u'Reset'),
            validator=None,
            name=u'Reset')
    def action_reset(self, action, data):
        """ Reset the form fields to their defaults. """
