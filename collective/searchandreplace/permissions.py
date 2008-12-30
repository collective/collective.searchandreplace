"""
permissions.py
"""

from Products.CMFCore.permissions import *

SearchAndReplace = 'Search and replace'

# Set up default roles for permissions
setDefaultRoles(SearchAndReplace, ('Owner',))


