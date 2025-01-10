Changelog
=========

8.3.1 (2025-01-10)
------------------

- Fix the search in a folder that is set as the default view of the parent folder. [Mychae1]

- Add tests for calculating the path to start the search from. [Mychae1]

- Also test under python 3.12. [gotcha]

8.3 (2023-09-25)
----------------

- Depend on z3c.form instead of zope.formlib
  [gotcha]


8.2.2 (2023-03-10)
------------------

- Test on GitHub Actions on Plone 4.3-6.0.  [gotcha]

- Fix isDefaultPage moved to a different interface module.
  [Rudd-O]


8.2.1 (2022-01-06)
------------------

- Fix the title of the action category disappearing (and displaying ``object`` instead) when installing this addon.
  [Rudd-O]


8.2.0 (2021-05-26)
------------------

- Do not show "Replace" button until user has seen Preview results.
  [gotcha]


8.1.1 (2021-01-11)
------------------

- Made "Find What" field required and allow empty "Replace With".
  Fixes `issue 43 <https://github.com/collective/collective.searchandreplace/issues/43>`_.
  [spereverde]


8.1.0 (2020-03-31)
------------------

- use pytest as test runner
  [gotcha]

- Enable search and replace on lines fields, Archetypes ``ILinesField`` and dexterity ``ITuple`` with ``value_type==ITextLine``
  Can be enabled with registry ``include_lines_fields`` to True
  [gotcha]



8.0.0 (2020-03-06)
------------------

- use safe_unicode from CMFPlone
  [maurits, gotcha]

- Enable search and replace on string fields, Archetypes ``IStringField`` and dexterity ``ITextLine``
  Can be disabled with registry ``include_textline_fields`` to False
  [gotcha]

- Translate field names in preview table
  [gotcha]

- Python 3 support for 5.2
  [gotcha]

- Major refactoring for readability
  [gotcha]

- Added update_modified setting to allow replacing without updating the modified index/metadata.  [Gagaro]


7.1.3 (2017-01-12)
------------------

- Fixed ImportErrors when dexterity is not available.  [maurits]


7.1.2 (2016-08-29)
------------------

Bug fixes:

- Do not use base object when replacing [Gagaro]


7.1.1 (2016-08-02)
------------------

Bug fixes:

- Fix UnicodeEncodeError when searching for non ascii characters.
  Fixes https://github.com/collective/collective.searchandreplace/issues/33
  [maurits]

- Added Russian translation and fixed translation mistakes.  [serge73]


7.1 (2016-07-20)
----------------

New features:

- Allow overriding the permission that is checked on an object.  By
  default this is the Modify portal content permission.  But when you
  have setup a workflow that does not allow editing published content,
  for example when you require doing changes with check-out/check-in
  from Iterate, then you may want to use a different permission.  You
  can then override the utility in your own code.  [maurits]

- Save a new version in the repository, when CMFEditions is enabled
  for the changed type.  [maurits]


7.0.1 (2016-07-19)
------------------

Bug fixes:

- Synced translations, updated Dutch.  [maurits]

- Do not fail when an object from the catalog cannot be found.  Print
  a warning in the logs.  [maurits]


7.0 (2016-07-19)
----------------

Breaking changes:

- Removed ``ISearchReplaceable`` behavior.  This was introduced in version 6.
  Kept the interface for backwards compatibility, but it is not used anymore.
  Instead, by default all types are searched and replaced.
  You can configure this in the new control panel.
  There you can restrict the types that are searched, if needed.

  There are upgrade steps to install the new configuration options,
  add the control panel, and remove the behavior from existing
  dexterity types.  Before you run the upgrade steps, you may see a
  warning and an error once when accessing the site in Plone 5:

  - WARNING plone.dexterity.schema No behavior registration found for behavior named: "collective.searchandreplace.interfaces.ISearchReplaceable" - trying fallback lookup..."
  - ERROR plone.dexterity.schema Error resolving behavior collective.searchandreplace.interfaces.ISearchReplaceable

  This should cause no troubles.
  This fixes issue https://github.com/collective/collective.searchandreplace/issues/25
  [maurits]

New features:

- Added option in form to use fast search.  By default this is
  checked.  This means we use the catalog, instead of waking up every
  object in the path.  [maurits]

- Search and replace in all text fields.  Removed special cases for
  Description and Text/Body field: these are handled the same as other
  text fields now.  TextLine fields and StringFields are ignored,
  except for the Title field.  [maurits]

- Ported tests to plone.app.testing.  [maurits]

- Added number of contents affected after a search. [Gagaro]

Bug fixes:

- Fixed Travis (continuous integration) test setup for Plone 5.  [maurits]

- Minor code cleanup: pyflakes, pep8, sorting imports.  [maurits]

- Conditionally load zcml for dexterity behavior/profile and ATContentTypes.  [maurits]

- Added ``plone.resource`` to our requirements for our resources.  [maurits]


6.0.4 (2016-03-23)
------------------

- Show link to searchreplace form in parent folder when you are not
  viewing a folderish item.
  [maurits]

- Add edit links in table.
  [Gagaro]

- Keep table and form values when replacing.
  [Gagaro]

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
