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
