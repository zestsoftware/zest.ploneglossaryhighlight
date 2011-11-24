Introduction
============

This is an extra package for `Products.PloneGlossary`_.  It adds a
field ``highlight`` to Archetypes content types in your site.  With
that field you can specify for a page whether terms on it should be
highlighted.  Values can be yes, no, or use the value of the parent
(which is the default).

.. _`Products.PloneGlossary`: http://pypi.python.org/pypi/Products.PloneGlossary


Installation
============

- Add it to the eggs option of the zope instance in your buildout.
  Add it to the zcml option as well if you are on Plone 3.2 or lower
  (untested).

- Restart your Zope instance.

- Install it in the Add-ons control panel in Plone.


Compatibility
=============

- Tested with Plone 3.3.5 and 4.1.2 (should be fine with earlier Plone
  3 or 4 versions too).

- Requires Products.PloneGlossary 1.5.0 or later.


Todo
====

- I don't mind putting a dexterity behavior in here that offers the
  same functionatily for Dexterity content, as long as this does not
  mean dexterity becomes a dependency.
