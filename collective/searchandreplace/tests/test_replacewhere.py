##########################################################################
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
##########################################################################

__author__ = '''Brent Lambert, David Ray, Jon Thomas'''
__version__ = '$ Revision 0.0 $'[11:-2]

from base import SearchAndReplaceTestCase
from zope.component import getUtility
from collective.searchandreplace.interfaces import ISearchReplaceUtility


class testReplaceWhere(SearchAndReplaceTestCase):
    """Ensure that we can replace in title, description and text."""

    def afterSetUp(self):
        self.srutil = getUtility(ISearchReplaceUtility)

    def testReplaceText(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setDescription('Test Description')
        doc1.setText('Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test case',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testReplaceTitle(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc2')
        doc1 = getattr(self.portal, 'doc2')
        doc1.setTitle('Test Title')
        doc1.setDescription('Test Description')
        doc1.setText('Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test title',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testReplaceDescription(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setDescription('Test Description')
        doc1.setText('Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test desc',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testReplaceWhere))
    return suite
