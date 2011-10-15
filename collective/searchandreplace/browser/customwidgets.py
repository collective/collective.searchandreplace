# -*- coding: us-ascii -*-
# _______________________________________________________________________
#              __________                      .__        
#   ____   ____\______   \____________  ___  __|__| ______
# _/ __ \ /    \|     ___/\_  __ \__  \ \  \/  /  |/  ___/
# \  ___/|   |  \    |     |  | \// __ \_>    <|  |\___ \ 
#  \___  >___|  /____|     |__|  (____  /__/\_ \__/____  >
#      \/     \/                      \/      \/       \/ 
# _______________________________________________________________________
# 
#    This file is part of the eduCommons software package.
#
#    Copyright (c) 2011 enPraxis, LLC
#    http://enpraxis.net
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2.8  
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 
# _______________________________________________________________________

__author__ = 'Brent Lambert <brent@enpraxis.net>'
__version__ = '$ Revision 0.0 $'[11:-2]

from zope.app.form.browser import TextAreaWidget
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from zope.app.form.browser.widget import renderElement


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
       

