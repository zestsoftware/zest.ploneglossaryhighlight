from setuptools import setup, find_packages

version = "2.0.0"

setup(
    name="zest.ploneglossaryhighlight",
    version=version,
    description="Make highlighting PloneGlossary terms optional per page or folder.",
    long_description=open("README.rst").read() + "\n" + open("CHANGES.rst").read(),
    # Get more strings from https://pypi.org/classifiers/
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="plone glossary highlight",
    author="Maurits van Rees",
    author_email="m.van.rees@zestsoftware.nl",
    url="https://github.com/zestsoftware/zest.ploneglossaryhighlight",
    license="GPL",
    packages=find_packages(),
    namespace_packages=["zest"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "Products.CMFPlone",
        "Products.PloneGlossary>=1.5.0",
    ],
    extras_require={
        "archetypes": ["archetypes.schemaextender"],
        "dexterity": ["plone.behavior", "plone.dexterity"],
        "test": ["plone.app.testing"],
    },
    entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
)
