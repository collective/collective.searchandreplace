from collective.searchandreplace import SearchAndReplaceMessageFactory as _
from zope import schema
from zope.interface import Interface

import zope.deferredimport


zope.deferredimport.initialize()


zope.deferredimport.deprecated(
    (
        "The ISearchReplaceable marker interface is no longer used. "
        "All types are now searched by default. "
        "You can configure this in @@searchreplace-controlpanel if needed."
    ),
    ISearchReplaceable="zope.interface:Interface",
)


class ISearchReplaceUtility(Interface):
    """ Search and replace utility interface """

    def getItems():
        """ Get items for preview. """


class ISearchReplaceSettings(Interface):
    """Control panel settings for search and replace."""

    restrict_searchable_types = schema.Bool(
        title=_(u"Restrict the enabled types."),
        description=_(
            u"If checked, only the enabled types are searched, "
            "otherwise all types are searched."
        ),
        required=False,
        default=False,
    )

    enabled_types = schema.List(
        title=_(u"List of types that are searched."),
        description=_(
            u"When 'Restrict the enable types' is checked, "
            "only the selected types are searched. "
            "Otherwise this list is ignored."
        ),
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.PortalTypes",
        ),
        required=False,
        default=[
            "Collection",
            "Document",
            "Event",
            "File",
            "Folder",
            "Image",
            "News Item",
        ],
    )

    maximum_text_characters = schema.Int(
        title=_(u"Maximum text characters"),
        description=_(
            u"The maximum number of characters to show "
            "before and after the found text."
        ),
        required=False,
        default=50,
    )

    update_modified = schema.Bool(
        title=_(u"Update the modified datetime when replacing."),
        description=_(
            u"If checked, the modified index/metadata of the object "
            u"having text replaced will be updated."
        ),
        required=False,
        default=True,
    )

    include_textline_fields = schema.Bool(
        title=_(u"Search also textline fields"),
        description=_(
            u"If checked, single line fields "
            u"will also be searched and replaced, "
            u"not only title and text fields.",
        ),
        required=False,
        default=True,
    )

    include_lines_fields = schema.Bool(
        title=_(u"Search also lines fields"),
        description=_(
            u"If checked, multiple lines fields like subject "
            u"will also be searched and replaced, "
            u"not only title and text fields.",
        ),
        required=False,
        default=False,
    )
