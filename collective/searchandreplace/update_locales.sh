#!/bin/bash
# Run this script to update the translations.

i18ndude rebuild-pot --pot locales/SearchAndReplace.pot --create SearchAndReplace .
i18ndude sync --pot locales/SearchAndReplace.pot $(find . -name 'SearchAndReplace.po')
