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

__author__ = '''Brent Lambert, David Ray, Jon Thomas'''
__version__ = '$ Revision 0.0 $'[11:-2]

from base import SearchAndReplaceTestCase
from Products.Archetypes.tests.test_fields import FakeRequest
from zope.component import getUtility
from collective.searchandreplace.interfaces import ISearchReplaceUtility


class testMatchCase(SearchAndReplaceTestCase):
    """ Ensure that the match case flag works   """

    def afterSetUp(self):
        self.srutil = getUtility(ISearchReplaceUtility)
        self.request = FakeRequest()

    def testNoMatchCase(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setText('Test Case')
        results = self.srutil.searchObjects(
            doc1,
            'test case',
            replaceText='foo',
            matchCase=False)
        self.assertEqual(len(results), 1)

    def testMatchCase(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc2')
        doc2 = getattr(self.portal, 'doc2')
        doc2.setTitle('test title')
        doc2.setText('Test Case')
        results = self.srutil.searchObjects(
            doc2,
            'test case',
            replaceText='foo',
            matchCase=True)
        self.assertEqual(len(results), 0)

    def testOneMatch(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        doc1 = getattr(self.portal, 'doc1')
        doc1.setTitle('Test Title')
        doc1.setText('Test Case')
        self.portal.invokeFactory('Document', 'doc2')
        doc2 = getattr(self.portal, 'doc2')
        doc2.setTitle('test title')
        doc2.setText('test case')
        # path1 = '%s' %  '/'.join(doc1.getPhysicalPath())
        # path2 = '%s' % '/'.join(doc2.getPhysicalPath())
        # paths = {path1: {'body': [0]}, path2: {'body': [0]}}
        results = self.srutil.searchObjects(
            self.portal,
            'test case',
            replaceText='foo',
            matchCase=True,
            # searchItems=paths
            )
        self.assertEqual(len(results), 1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMatchCase))
    return suite
