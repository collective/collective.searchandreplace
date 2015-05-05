Changelog
=========

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
