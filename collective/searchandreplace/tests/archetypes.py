from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import add_documents_images_and_files
from App.class_init import InitializeClass
from Products.Archetypes.atapi import BaseContent
from Products.Archetypes.atapi import BaseSchema
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import MetadataSchema
from Products.Archetypes.atapi import process_types
from Products.Archetypes.atapi import registerType
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import TextAreaWidget
from Products.Archetypes.atapi import TextField
from Products.CMFCore.utils import ContentInit
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


PROJECTNAME = "collective.searchandreplace"

SampleTypeSchema = (
    BaseSchema.copy()
    + MetadataSchema(())
    + Schema(
        (
            TextField(
                "rich",
                required=False,
                searchable=True,
                default_output_type="text/x-html-safe",
                widget=RichWidget(description="", label=u"Rich Text"),
            ),
            TextField(
                "plain",
                required=False,
                searchable=True,
                widget=TextAreaWidget(description="", label=u"Plain Text"),
            ),
            StringField(
                "line",
                required=False,
                searchable=True,
                widget=StringWidget(description="", label=u"Text Line"),
            ),
            TextField(
                "unsearchable",
                required=False,
                searchable=False,
                default_output_type="text/x-html-safe",
                widget=RichWidget(description="", label=u"Unsearchable Text"),
            ),
        )
    )
)


class SampleType(BaseContent, BrowserDefaultMixin):

    schema = SampleTypeSchema
    portal_type = "SampleType"
    archetype_name = "SampleType"
    security = ClassSecurityInfo()


InitializeClass(SampleType)
registerType(SampleType, PROJECTNAME)


def initialize_archetypes_testing(context):
    """Initializer called when initializing with testing.zcml."""
    listOfTypes = listTypes(PROJECTNAME)

    content_types, constructors, ftis = process_types(listOfTypes, PROJECTNAME)

    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: %s" % (PROJECTNAME, atype.archetype_name)
        ContentInit(
            kind,
            content_types=(atype,),
            permission=add_documents_images_and_files,
            extra_constructors=(constructor,),
        ).initialize(context)
