from collective.searchandreplace import SearchAndReplaceMessageFactory as _
from collective.searchandreplace.interfaces import ISearchReplaceSettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from z3c.form import form


class SearchReplaceControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ISearchReplaceSettings


SearchReplaceControlPanelView = layout.wrap_form(
    SearchReplaceControlPanelForm, ControlPanelFormWrapper
)
SearchReplaceControlPanelView.label = _(u"Search and Replace settings")
