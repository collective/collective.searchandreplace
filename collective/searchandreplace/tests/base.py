from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Testing import ZopeTestCase as ztc

import doctest


@onsetup
def setup_searchandreplace_project():
    """Load and install packages required for the tests.
    """

    fiveconfigure.debug_mode = True

    import collective.searchandreplace
    zcml.load_config('configure.zcml', collective.searchandreplace)

    fiveconfigure.debug_mode = False

    ztc.installPackage('collective.searchandreplace')


setup_searchandreplace_project()
setupPloneSite(
    with_default_memberarea=0,
    extension_profiles=['collective.searchandreplace:default'])

oflags = (doctest.ELLIPSIS |
          doctest.NORMALIZE_WHITESPACE)

prod = "collective.searchandreplace"


class SearchAndReplaceTestCase(PloneTestCase):
    """ Test Class """

    def _setupHomeFolder(self):
        """Don't create a user folder in the tests.

        Presumably this is needed to avoid replacing stuff in that
        Members folder, where we only want the tests to replace stuff in
        content that we create.
        """
        pass


class SearchAndReplaceFunctionalTestCase(FunctionalTestCase):
    """ Functional test class """
