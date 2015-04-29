# -*- coding: us-ascii -*-
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from zope.app.form.browser import TextAreaWidget


class TwoLineTextAreaWidget(TextAreaWidget):
    """ A two line text area widget. """

    height = 2


class MultiPreSelectCheckBoxWidget(MultiCheckBoxVocabularyWidget):
    """ A multi select check box widget that is pre selected. """

    def __init__(self, field, request):
        super(MultiPreSelectCheckBoxWidget, self).__init__(field, request)
        self.items = field.value_type.vocabulary.by_value.keys()

    def _getFormValue(self):
        return self.items

    def renderValue(self, value):
        rval = self.context.context.restrictedTraverse('@@searchreplacetable')
        return rval(self.context, self.request)
