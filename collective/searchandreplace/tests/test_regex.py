##################################################################################
#    Copyright (c) 2009 Novell, All rights reserved.
#    Portions copyright 2009 Massachusetts Institute of Technology, All rights reserved.
#                                                                                 
#    This program is free software; you can redistribute it and/or modify         
#    it under the terms of the GNU General Public License as published by         
#    the Free Software Foundation, version 2.                                      
#                                                                                 
#    This program is distributed in the hope that it will be useful,              
#    but WITHOUT ANY WARRANTY; without even the implied warranty of               
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                
#    GNU General Public License for more details.                                 
#                                                                                 
#    You should have received a copy of the GNU General Public License            
#    along with this program; if not, write to the Free Software                  
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    
#                                                                                 
##################################################################################

__author__  = '''Brent Lambert, David Ray, Jon Thomas'''
__version__   = '$ Revision 0.0 $'[11:-2]

from Products.CMFPlone.tests import PloneTestCase
from unittest import TestSuite, makeSuite
from Testing import ZopeTestCase
from Testing.ZopeTestCase import user_name
from AccessControl import Unauthorized
from base import SearchAndReplaceTestCase
from Products.Archetypes.tests.test_fields import FakeRequest


class testRegex(SearchAndReplaceTestCase):
    """ Ensure that the match case flag works   """

    def afterSetUp(self):
        self.srtool = self.portal.portal_search_and_replace
        self.request = FakeRequest()

    def testRegex(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setText('Test TestTest')
        path = ['/'.join(doc1.getPhysicalPath())]
        results = self.srtool.searchAndReplace(self.request,
                                               path,
                                               '\\bTest\\b',
                                               'text',
                                               'foo',
                                               useRegex='on',
                                               preview=True)
        assert(len(results) == 1)

    def testNoRegex(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setText('Test TestTest')
        path = ['/'.join(doc1.getPhysicalPath())]
        results = self.srtool.searchAndReplace(self.request,
                                               path,
                                               '\\bTest\\b',
                                               'text',
                                               'foo',
                                               useRegex=False,
                                               preview=True)
        
        assert(len(results) == 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testRegex))
    return suite
