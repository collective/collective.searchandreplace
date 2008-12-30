""" Extensions/Install.py """

# Copyright (c) 2006 by Klein & Partner KEG, Austria
#
# Generated: 
# Generator: ArchGenXML Version 1.4.0-beta2
#            http://sf.net/projects/archetypes/
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__    = '''Jens Klein <jens.klein@jensquadrat.com>'''
__docformat__ = 'plaintext'
__version__   = '$ Revision 0.0 $'[11:-2]

import os.path
import sys
import transaction
from StringIO import StringIO

from App.Common import package_home
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import manage_addTool
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from zExceptions import NotFound, BadRequest

from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
try:
    from Products.Archetypes.lib.register import listTypes
except ImportError:
    from Products.Archetypes.public import listTypes
from collective.searchandreplace.config import PROJECTNAME, TOOL_NAME, TOOL_PORTAL_NAME, EXTENSION_PROFILES
from collective.searchandreplace.config import product_globals as GLOBALS

import logging

LOG = logging.getLogger('Install.py')

def install(self):
    LOG.info('Install.py executing')
    """ External Method to install SearchAndReplace """
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    # If the config contains a list of dependencies, try to install
    # them.  Add a list called DEPENDENCIES to your custom
    # AppConfig.py (imported by config.py) to use it.
    try:
        from collective.searchandreplace.config import DEPENDENCIES
    except:
        DEPENDENCIES = []
    portal = getToolByName(self,'portal_url').getPortalObject()
    portal_quickinstaller = portal.portal_quickinstaller
    portal_setup = getToolByName(self, 'portal_setup')
    for dependency in DEPENDENCIES:
        print >> out, "Installing dependency %s:" % dependency
        portal_quickinstaller.installProduct(dependency)
        transaction.savepoint()

    for extension_id in EXTENSION_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
        product_name = extension_id.split(':')[0]
        portal_quickinstaller.notifyInstalled(product_name)
        transaction.savepoint()


    classes = listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)
    install_subskin(self, out, GLOBALS)
    install_tool(self, out, GLOBALS)

    # try to call a custom install method
    # in 'AppInstall.py' method 'install'
    try:
        install = ExternalMethod('temp','temp',PROJECTNAME+'.AppInstall', 'install')
    except NotFound:
        install = None

    if install:
        print >>out,'Custom Install:'
        res = install(self)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no custom install'
    return out.getvalue()

def install_tool(self, out, product_globals):
    """ Setup a tool in the Plone site."""

    # Add the tool if it does not already exist.
    bt = getToolByName(self, TOOL_NAME, None)
    if bt is None:
        print >> out, "* Installing %s as %s\n" % (TOOL_PORTAL_NAME, TOOL_NAME)
        portal = getToolByName(self, 'portal_url').getPortalObject()
        addTool = portal.manage_addProduct[PROJECTNAME].manage_addTool
        addTool(type = TOOL_PORTAL_NAME)

        action_tool = getToolByName(self, 'portal_actions')
        action_tool.addActionProvider(TOOL_NAME)

        bt = getToolByName(self, TOOL_NAME)

def uninstall(self):
    out = StringIO()

    # try to call a workflow uninstall method
    # in 'InstallWorkflows.py' method 'uninstallWorkflows'
    try:
        installWorkflows = ExternalMethod('temp','temp',PROJECTNAME+'.InstallWorkflows', 'uninstallWorkflows').__of__(self)
    except NotFound:
        installWorkflows = None

    if installWorkflows:
        print >>out,'Workflow Uninstall:'
        res = uninstallWorkflows(self,out)
        print >>out,res or 'no output'
    else:
        print >>out,'no workflow uninstall'

    # try to call a custom uninstall method
    # in 'AppInstall.py' method 'uninstall'
    try:
        uninstall = ExternalMethod('temp','temp',PROJECTNAME+'.AppInstall', 'uninstall')
    except:
        uninstall = None

    if uninstall:
        print >>out,'Custom Uninstall:'
        res = uninstall(self)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no custom uninstall'

    return out.getvalue()
