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

from zope.interface import Interface, implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema import Text, Bool, Choice, Tuple, Set
from collective.searchandreplace import SearchAndReplaceMessageFactory as _
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from zope.component import adapts
from collective.searchandreplace.interfaces import ISearchReplaceable
from five.formlib.formbase import AddForm
from zope.formlib.form import FormFields, action
from customwidgets import TwoLineTextAreaWidget, MultiPreSelectCheckBoxWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from collective.searchandreplace.interfaces import ISearchReplaceUtility
from Products.statusmessages.interfaces import IStatusMessage


def validate_searchreplaceform(form, action, data):
    """ Validate the Search/Replace form. """
    

class ISearchReplaceForm(Interface):
    """ Interface for Search and Replace form """
    
    findWhat = Text(title=_(u'Find What'),
                    description=_(u'Enter the text to find.'),
                    required=True)

    replaceWith = Text(title=_(u'Replace With'),
                       description=_(u'Enter the text to replace the '
                                     'original text with.'),
                       required=False)

    searchSubfolders = Bool(title=_(u'Search Subfolders'),
                            description=_(u'If checked, this will '
                                          'recursively search through '
                                          'any selected folders and '
                                          'their children, replacing at '
                                          'each level.'),
                            default=True,
                            required=True)

    matchCase = Bool(title=_(u'Match Case'),
                     description=_(u'Check the box for a case sensitive search.'),
                     default=False,
                     required=True)


class SearchReplaceForm(AddForm):
    """ """

    form_fields = FormFields(ISearchReplaceForm)
    form_fields['findWhat'].custom_widget = TwoLineTextAreaWidget
    form_fields['replaceWith'].custom_widget = TwoLineTextAreaWidget
    
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
        srutil = getUtility(ISearchReplaceUtility)
        if self.request.has_key('form.affectedContent'):
            # Do only the selected items
            nitems = len(self.request['form.affectedContent'])
            items = srutil.parseItems(self.request['form.affectedContent'])
            replaced = srutil.searchObjects(
                self.context,
                data['findWhat'],
                searchSubFolders=data['searchSubfolders'],
                matchCase=data['matchCase'],
                replaceText=data['replaceWith'],
                doReplace=True,
                searchItems=items)
            IStatusMessage(self.request).addStatusMessage(
                _(u'Search text replaced in %d of %d instance(s).' %(replaced, nitems)), 
                  type='info')
        else:
            # Do everything you can find
            replaced = srutil.searchObjects(
                self.context,
                data['findWhat'],
                searchSubFolders=data['searchSubfolders'],
                matchCase=data['matchCase'],
                replaceText=data['replaceWith'],
                doReplace=True)
            IStatusMessage(self.request).addStatusMessage(_(u'Search text replaced.'), type='info')
        self.request.response.redirect(self.context.absolute_url())
        return ''
        
    @action(_(u'Reset'),
            validator=None,
            name=u'Reset')
    def action_reset(self, action, data):
        """ Reset the form fields to their defaults. """
