##############################################################################
#    Copyright (c) 2009 Novell, All rights reserved.
#    Portions copyright 2009 Massachusetts Institute of Technology,
#    All rights reserved.
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
##############################################################################

from setuptools import setup, find_packages
import sys

pytest_extras = [
    "pytest",
    "requests",
]
if sys.version_info[0] == 2:
    pytest_extras.append("pathlib2")
    pytest_extras.append("gocept.pytestlayer")
if sys.version_info[0] == 3 and sys.version_info[1] <= 11:
    pytest_extras.append("gocept.pytestlayer")
if sys.version_info[0] == 3 and sys.version_info[1] >= 12:
    pytest_extras.append("zope.pytestlayer")


version = "8.3.1"

setup(
    name="collective.searchandreplace",
    version=version,
    description="Batch Search and Replace",
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    # Get more strings from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="batch search replace",
    author="enPraxis",
    author_email="info@enpraxis.net",
    maintainer="Maurits van Rees",
    maintainer_email="m.van.rees@zestsoftware.nl",
    url="https://github.com/collective/collective.searchandreplace",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
    install_requires=[
        "Acquisition",
        "plone.api",
        "plone.app.layout",
        "plone.app.textfield",
        "plone.autoform",
        "plone.resource",
        "Products.CMFCore",
        "Products.CMFPlone",
        "Products.statusmessages",
        "setuptools",
        "Zope2",
        "z3c.form",
        "zope.component",
        "zope.contentprovider",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.publisher",
        "zope.schema",
    ],
    extras_require=dict(
        test=[
            "collective.dexteritytextindexer",
            "plone.app.testing",
        ],
        pytest=pytest_extras,
    ),
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
