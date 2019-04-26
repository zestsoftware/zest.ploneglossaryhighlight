Introduction
============

This is an extra package for `Products.PloneGlossary <https://pypi.org/project/Products.PloneGlossary>`_.
It adds a field ``highlight`` to content types in your site.
With that field you can specify for a page whether terms on it should be highlighted.
Values can be yes, no, or use the value of the parent (which is the default).

Support for Archetypes has been there since the first release (with ``archetypes.schemaextender``).
Support for Dexterity has been there since release 2.0.0 (with ``plone.behavior`` and ``plone.dexterity``).


Installation
============

- Add it to the eggs option of the zope instance in your buildout.
  When you want Archetypes support, please use ``zest.ploneglossaryhighlight[archetypes]``.
  When you want Dexterity support, please use ``zest.ploneglossaryhighlight[dexterity]``.
  Or use both: ``zest.ploneglossaryhighlight[archetypes, dexterity]``.

- Restart your Zope instance.

- Go to the Add-ons control panel in Plone.

- Install PloneGlossary.

- Install zest.ploneglossaryhighlight.


Compatibility
=============

- Tested with Plone 4.3 on Python 2.7.

- Requires Products.PloneGlossary 1.5.0 or later.
