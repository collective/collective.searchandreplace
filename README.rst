Introduction
============

.. image:: https://secure.travis-ci.org/collective/collective.searchandreplace.png?branch=master
   :target: https://travis-ci.org/#!/collective/collective.searchandreplace

The collective.searchandreplace product is a Plone Add-on designed to
find and replace text in Plone content objects, namely titles,
descriptions, and document text. It operates over single or multiple
Plone content objects and can show a preview of changes as well as
immediately perform them.

Optional features include being able to control searching in
subfolders, and matching based on case sensitivity/insensitivity.

Note: since version 6.0, we search and replace only items that
implement the ``ISearchReplaceable`` interface.  Since this version,
this interface can be set on dexterity content types using a
behavior.  Note that when you enable or disable this interface on a
content type, either through the web or in code, you should reindex
the ``object_provides`` index in the ``portal_catalog``.


Compatibility
-------------

From collective.searchandreplace version 5.0, we are compatible with
Plone 4.3 and 5.0.

The collective.searchandreplace product was initally built for use
with eduCommons by Novell, inc, later improved by EnPraxis.  It is
currently maintained by Maurits van Rees.  Plone 5 support added by
Gagaro.
