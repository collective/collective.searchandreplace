SearchAndReplace Product
========================

The SearchAndReplace product is a Plone Add-on designed to find and replace text in Plone titles, descriptions, and document text.

Installing SearchAndReplace
===========================

To install SearchAndReplace you must first setup up easy_install_. After installing easy_install, you can install the SearchAndReplace product by running:
  
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall

  easy_install collective.searchandreplace
  
To add the *SearchAndReplace* product to your Plone site, start your Plone site and enter the control panel. Then click on the *Add-on products* link in your Plone control panel. Select the *SearchAndReplace* checkbox and click the *install* button. The product will appear in the list of installed products.

.. image:: images/install_searchandreplace.png
   :alt: Install SearchAndReplace checkbox

Using the Search and Replace Product
====================================

To use the Search and Replace product, click on the *Search/Replace* tab. The Search and Replace from will be displayed.

.. image:: images/searchandreplace_form.png
   :alt: The Search and Replace form

Search And Replace Form
-----------------------

There are several fields on the Search and Replace form:

Affected content
  Displays the objects that the Search and Replace will process. Unchecking an object will prevent the SearchAndReplace product from processing that particular object.

Search subfolders
  If checked, this will recursively search through any selected folders and their children, replacing at each level.

Find what
  The text to be replaced

Match case
  If selected the product will match the case of the string in the 'Find what' field, otherwise case will be ignored.

Use Regular Expression
  If checked, the text in the 'Find what' field will be used as a python-syntaxed `regular expression`_.

Replace where
  Enter the destination field for the replacement text. 'Attachment File' will make replacements in the file. 'Title' or 'Description' only make sense to use if you are using regular expressions. With regular expressions, you can match text in the file using parentheses and then set the text in the title or description. 

Replace with
  The text that will replace the original text 

Replace All button
  The Replace All button runs the request.

Preview Results button
  The Preview Results button allows you to view the phrases that will be replaced before processing the request.

.. image:: images/previewresults_display.png
   :alt: Preview of text to be replaced

.. _`regular expression`: http://en.wikipedia.org/wiki/Regular_expression




	