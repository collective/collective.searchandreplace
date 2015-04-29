import doctest
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase.PloneTestCase import PloneTestCase, FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc


@onsetup
def setup_searchandreplace_project():
    """
    Load and install packages required for the collective.searchandreplace tests
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
        """ Ugly hack to keep the underlying testing framework from trying to create a user folder."""
        pass


class SearchAndReplaceFunctionalTestCase(FunctionalTestCase):
    """ Functional test class """
