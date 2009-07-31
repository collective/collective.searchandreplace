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

from base import prod, oflags, SearchAndReplaceFunctionalTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite
from unittest import TestSuite


def test_suite():
    suite = TestSuite()

    basicsearchtest = FunctionalDocFileSuite('tests/basicsearch.txt',
                                       package=prod,
                                       test_class=SearchAndReplaceFunctionalTestCase,
                                       optionflags=oflags)

    searchavailabletest = FunctionalDocFileSuite('tests/searchavailable.txt',
                                       package=prod,
                                       test_class=SearchAndReplaceFunctionalTestCase,
                                       optionflags=oflags)
                                                         
    suite.addTests((basicsearchtest, searchavailabletest))

    return suite
