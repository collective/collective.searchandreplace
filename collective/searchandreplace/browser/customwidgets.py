# -*- coding: us-ascii -*-
from zope.formlib.itemswidgets import MultiSelectWidget
from zope.formlib.widgets import TextAreaWidget


class TwoLineTextAreaWidget(TextAreaWidget):
    """ A two line text area widget. """

    height = 2


class MultiPreSelectCheckBoxWidget(MultiSelectWidget):
    """ A multi select check box widget that is pre selected. """

    def __init__(self, field, request):
        super(MultiPreSelectCheckBoxWidget, self).__init__(
            field, field.value_type.vocabulary, request
        )
        self.items = field.value_type.vocabulary.by_value.keys()

    def _getFormValue(self):
        return self.items

    def renderValue(self, value):
        rval = self.context.context.restrictedTraverse("@@searchreplacetable")
        return rval(self.context, self.request)
