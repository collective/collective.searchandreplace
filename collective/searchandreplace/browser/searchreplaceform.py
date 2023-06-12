# -*- coding: us-ascii -*-
from Acquisition import aq_parent
from collective.searchandreplace import SearchAndReplaceMessageFactory as _
from collective.searchandreplace.interfaces import ISearchReplaceUtility


try:
    from plone.app.layout.navigation.defaultpage import isDefaultPage
except ImportError:
    from plone.base.defaultpage import is_default_page as isDefaultPage

from plone.autoform.form import AutoExtensibleForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import contentprovider
from z3c.form import form
from z3c.form import interfaces
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import Int
from zope.schema import Text


def validate_searchreplaceform(form, action, data):
    """ Validate the Search/Replace form. """


class ISearchReplaceForm(Interface):
    """ Interface for Search and Replace form """

    findWhat = Text(
        title=_(u"Find What"), description=_(u"Enter the text to find."), required=True
    )

    replaceWith = Text(
        title=_(u"Replace With"),
        description=_(u"Enter the text to replace the original text with."),
        required=False,
    )

    maxResults = Int(
        title=_(u"Maximum Number of Results"),
        description=_(
            u"Maximum number of results to show. "
            "Warning: this only affects how many preview results are shown. "
            "It has no effect on how many found texts are "
            "replaced when you use the Replace button."
        ),
        default=None,
        required=False,
    )

    searchSubfolders = Bool(
        title=_(u"Search Subfolders"),
        description=_(
            u"If checked, this will recursively search "
            "through any selected folders and their "
            "children, replacing at each level."
        ),
        default=True,
        required=False,
    )

    matchCase = Bool(
        title=_(u"Match Case"),
        description=_(u"Check the box for a case sensitive search."),
        default=False,
        required=False,
    )

    onlySearchableText = Bool(
        title=_(u"Fast search"),
        description=_(
            u"Use the catalog to search, just like the search form does. "
            "This only finds keywords, not html tags. "
            "You might have some text fields that are not found this way, "
            "so if not checked, you may find more content, "
            "but it will be slower. "
            "Regardless of this setting, when at least one match is found, "
            "text in all text fields may be replaced."
        ),
        required=False,
        default=True,
    )


@implementer(interfaces.IButtonForm, interfaces.IHandlerForm,
             interfaces.IFieldsAndContentProvidersForm)
class SearchReplaceForm(AutoExtensibleForm, form.AddForm):
    """ """
    schema = ISearchReplaceForm
    contentProviders = contentprovider.ContentProviders(['replacetable'])
    contentProviders['replacetable'].position = 0

    label = _(u"Search and Replace")
    description = _(u"Search and replace text found in documents.")

    @button.buttonAndHandler(_("Preview"), name="preview")
    def action_preview(self, action):
        """ Preview files to be changed. """
        self.form_reset = False

    def show_replace(self):
        return (
            "form.buttons.preview" in self.request.form
            or "form.buttons.replace" in self.request.form
        )

    @button.buttonAndHandler(
        _("Replace"), name="replace",
        condition=lambda form: form.show_replace()
    )
    def action_replace(self, action):
        """ Replace text for all files. """
        self.form_reset = False

    def must_replace(self):
        return "form.buttons.replace" in self.request.form

    def maybe_replace(self):
        if self.must_replace():
            data, errors = self.extractData()
            if "form.widgets.preview" not in self.request:
                self.replace_all(data)
            elif "form.affectedContent" in self.request:
                self.replace_filtered(data)
            else:
                pass

    def replace_filtered(self, data):
        occurences = parseItems(self.request["form.affectedContent"])
        occur_count = 0
        for page_url, page_result in occurences.items():
            for field, indexes in page_result.items():
                occur_count += len(indexes)
        srutil = getUtility(ISearchReplaceUtility)
        repl_count = srutil.replaceFilteredOccurences(
            self.context,
            data["findWhat"],
            replaceWith=data["replaceWith"],
            occurences=occurences,
            searchSubFolders=data.get("searchSubfolders", False),
            matchCase=data["matchCase"],
            onlySearchableText=data["onlySearchableText"],
        )
        IStatusMessage(self.request).addStatusMessage(
            _(
                u"Search text replaced in ${replaced} of ${items} " "instance(s).",
                mapping={"replaced": repl_count, "items": occur_count},
            ),
            type="info",
        )

    def replace_all(self, data):
        srutil = getUtility(ISearchReplaceUtility)
        repl_count = srutil.replaceAllMatches(
            self.context,
            data["findWhat"],
            replaceWith=data["replaceWith"],
            searchSubFolders=data.get("searchSubfolders", False),
            matchCase=data["matchCase"],
            onlySearchableText=data["onlySearchableText"],
        )
        IStatusMessage(self.request).addStatusMessage(
            _(
                u"Search text replaced in all ${items} instance(s).",
                mapping={"items": repl_count},
            ),
            type="info",
        )

    @button.buttonAndHandler(_("Reset"), name="reset")
    def action_reset(self, action):
        """ Reset the form fields to their defaults. """
        self.request.response.redirect('./@@searchreplaceform')


def parseItems(items):
    """ Get list of items from form values """
    itemd = {}
    if not isinstance([], type(items)):
        items = [items]
    for x in items:
        try:
            line, pos, path = x.split(":")
        except ValueError:
            continue
        if path not in itemd:
            itemd[path] = {}
        if "title" == line:
            if "title" not in itemd[path]:
                itemd[path]["title"] = []
            itemd[path]["title"].append(int(pos))
        elif " " in line:
            try:
                fieldname, line_number = line.split(" ")
            except ValueError:
                continue
            if fieldname not in itemd[path]:
                itemd[path][fieldname] = []
            itemd[path][fieldname].append(int(pos))
    return itemd
