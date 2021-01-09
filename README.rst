Introduction
============

.. image:: https://secure.travis-ci.org/collective/collective.searchandreplace.png?branch=master
   :target: https://travis-ci.org/#!/collective/collective.searchandreplace

The collective.searchandreplace product is a Plone Add-on designed to find and replace text in Plone content objects.

It searches in all text fields (since version 7.0) and all string fields (since 8.0).

This includes default content types fields like title, description, and document text.
It excludes the id/short name string field.

It operates over single or multiple Plone content objects and can show a preview of changes as well as immediately perform them.

Features include:

- being able to control searching in subfolders
- matching based on case sensitivity/insensitivity
- maximum number of results
- fast search using the catalog by default
- disable the fast search to be able to search and replace raw html tags, for example replace ``<strong>text</strong>`` by ``<em>text</em>``


Development
-----------

.. image:: https://coveralls.io/repos/github/collective/collective.searchandreplace/badge.svg?branch=master
  :target: https://coveralls.io/github/collective/collective.searchandreplace?branch=master


Binder
------

Running tests and demo Plone site on mybinder.org.

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/collective/collective.searchandreplace/master?filepath=binder%2Fpytest.ipynb


Compatibility
-------------

From version 8.0, we are compatible with
Plone 4.3, 5.1 and 5.2.

To be able to run the buildout for a specific Plone version, you need to set an environment variable for the Plone version you want to use, eg.
``export PLONE_VERSION=5.2``

.. warning:: 8.0 is not backward-compatible.

   - The Python API of the searchandreplace utility has changed. If your setup customizes searchandreplace, it will need some work.

   - String fields are now searched. You can turn that feature off to keep 7.x functionality by setting the registry
     ``include_textline_fields`` to ``False``

From version 5.0, we are compatible with
Plone 4.3 and 5.0.

The collective.searchandreplace product was initally built for use
with eduCommons by Novell, inc, later improved by EnPraxis.  It is
currently maintained by Maurits van Rees.  Plone 5 support added by
Gagaro.
