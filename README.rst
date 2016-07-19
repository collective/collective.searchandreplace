Introduction
============

.. image:: https://secure.travis-ci.org/collective/collective.searchandreplace.png?branch=master
   :target: https://travis-ci.org/#!/collective/collective.searchandreplace

The collective.searchandreplace product is a Plone Add-on designed to find and replace text in Plone content objects.
It looks in title, description, and document text, and since version 7 it looks in all text fields.
It operates over single or multiple Plone content objects and can show a preview of changes as well as immediately perform them.

Features include:

- being able to control searching in subfolders
- matching based on case sensitivity/insensitivity
- maximum number of results
- fast search using the catalog by default
- disable the fast search to be able to search and replace raw html tags, for example replace ``<strong>text</strong>`` by ``<em>text</em>``


Compatibility
-------------

From collective.searchandreplace version 5.0, we are compatible with
Plone 4.3 and 5.0.

The collective.searchandreplace product was initally built for use
with eduCommons by Novell, inc, later improved by EnPraxis.  It is
currently maintained by Maurits van Rees.  Plone 5 support added by
Gagaro.
