Changelog
=========

6.0.4 (unreleased)
------------------

- Add an option to limit the number of results shown.  Indirectly this
  limits the number of matches to replace, because matches that are
  not shown, cannot be selected for replacement.
  [Gagaro]

- Add a setting to limit the number of characters shown before and after.
  [Gagaro]

- Disable columns in searchreplaceform view.
  [Gagaro]

- Include toggleSelect for Plone 5.
  [Gagaro]


6.0.3 (2016-02-15)
------------------

- Allowed replacing with an empty string.  Fixes #13.  [maurits]

- Fix ensure we get the attributes of the base object in _getRawText.
  [Gagaro]


6.0.2 (2016-02-08)
------------------

- In SearchAndReplace.pot added the ability to translate configure.zcml , searchreplacetable.pt.
  Added Russian translation.


6.0.1 (2016-01-16)
------------------

- Added Russian translations.  [serge73]


6.0 (2015-11-30)
----------------

- Added a behavior to add ISearchReplaceable on Dexterity content types.
  Also added a profile to set this behavior on some content types.
  [Gagaro]

- Only search and replace contents with the ISearchReplaceable interface.
  [Gagaro]


5.1 (2015-10-27)
----------------

- Required ``plone.app.textfield`` in ``setup.py``.
  [maurits]


5.0 (2015-10-27)
----------------

- Compatibility with Plone 5 and Dexterity content types.
  [Gagaro]


4.2 (2015-06-22)
----------------

- Fix translation string of status message when replacing.
  [maurits]

- Nicer message when immediately replacing all text without preview.
  [maurits]


4.1 (2015-05-05)
----------------

- Add Travis badge.
  [maurits]


4.0 (2015-04-30)
----------------

- Check if the user has the ``Modify portal content`` permission for
  each item.  Ignore items for which this is not the case.
  [maurits]

- Add separate permission for showing the action.  This makes it
  easier to restrict usage of Search and Replace if wanted.  By
  default the same roles have this permission as for the standard
  'Modify portal content' permission.  Added upgrade steps for this.
  Permission title is: 'collective.searchandreplace: Use Search And
  Replace'.
  [maurits]

- Fix i18n.  Use SearchAndReplace domain everywhere.  Update po files.
  [maurits]

- Hide 'search subfolders' option for items that are not folderish or
  a default page. [davisagli]

- Also support 'search subfolders' for default pages. [davisagli]

- Use the unicode value stored in the Archetypes BaseUnit to avoid
  UnicodeDecodeErrors when the BaseUnit's encoding is not utf8.
  [davisagli]

- Enable searching the entire site. [davisagli]

- Cleanup.  Fix tests.  Add buildout for testing with Plone 4.3.
  [maurits]

- Include permissions from CMFCore, to avoid possible startup
  problems. [maurits]

- Make the plugin appears in quick installer [ivanteoh]

- Support unicode [ivanteoh]

- Fix the total of replaced instances [ivanteoh]


3.1
---

- Updated translation files [blambert555]

- Added updated Spanish translation [blambert555]

- Added updated Brazilian Porteguese translations [blambert555]


2.0/2.1
-------

- Updated for Plone 4. All forms and functionality completely refactored and brought up to date. [blambert555]


1.0.1
-----

- Updating licensing information


1.0
---

- Initial release
