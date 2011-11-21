#!/bin/sh
# Run this script to update the translations.
i18ndude rebuild-pot --pot locales/zest.ploneglossaryhighlight.pot --create zest.ploneglossaryhighlight .
i18ndude rebuild-pot --pot locales/zest.ploneglossaryhighlight.pot --merge locales/manual.pot --create zest.ploneglossaryhighlight .

i18ndude sync --pot locales/zest.ploneglossaryhighlight.pot $(find . -name 'zest.ploneglossaryhighlight.po')
