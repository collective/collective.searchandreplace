from Testing.ZopeTestCase import FunctionalDocFileSuite
from collective.searchandreplace.tests.base import \
    SearchAndReplaceFunctionalTestCase
from collective.searchandreplace.tests.base import oflags
from collective.searchandreplace.tests.base import prod
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
