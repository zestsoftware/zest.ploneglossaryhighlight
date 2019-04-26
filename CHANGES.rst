Changelog
=========

2.0.0 (2019-04-26)
------------------

- Added Dexterity support in a ``[dexterity]`` extra requirement in ``setup.py``.
  This has ``plone.behavior`` and ``plone.dexterity`` as dependencies.
  [maurits]

- Moved Archetypes support to an ``[archetypes]`` extra requirement in ``setup.py``.
  This has ``archetypes.schemaextender`` as dependency.
  [maurits]

- Register the default adapter only for Archetypes base content, instead of everything.
  [maurits]

- Test only with Python 2.7 and Plone 4.3.
  [maurits]


1.0 (2011-11-24)
----------------

- Initial release
  [maurits]
