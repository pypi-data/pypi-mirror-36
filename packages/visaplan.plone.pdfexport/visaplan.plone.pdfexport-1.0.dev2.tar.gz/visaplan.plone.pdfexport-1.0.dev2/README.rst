.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

========================
visaplan.plone.pdfexport
========================

Support for configurable exports of single-page and structured documents
(built from folders and documents) from a Plone site.

The configuration of exports is implemented using "export profiles"
which allow to specify several types for TOCs as well.

Those export profiles live in a relational database; there is no support for
configuration of database name prefixes yet (thus, currently you'd want to
create your own fork, to implement such configuration - pull requests welcome -
or simply use your own schema and table names).

We use PostgreSQL and have no idea whether or not our product will work with
other databases ...

The purpose of this package (for now) is *not* to provide new functionality
but to factor out existing functionality from an existing monolitic Zope product.
Thus, it is more likely to lose functionality during further development
(as parts of it will be forked out into their own packages,
or some functionality may even become obsolete because there are better
alternatives in standard Plone components).


Features
--------

- Talks to a PDFReactor_ server
  (currently version 7 which is quite outdated meanwhile)
- Export profiles, which allow to configure:

  - TOCs (based on HTML hN elements, filterable by classes; default)
  - lists of images
  - etc.


Examples
--------

This add-on can be seen in action at the following sites:

- https://www.unitracc.de
- https://www.unitracc.com

Well, it can't be really seen, because the functionality is for privileged
users only ...


Documentation
-------------

Sorry, we don't have real user documentation yet.


Installation
------------

Install visaplan.plone.pdfexport by adding it to your buildout::

    [buildout]

    ...

    eggs =
        visaplan.plone.pdfexport


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/visaplan/visaplan.plone.pdfexport/issues
- Source Code: https://github.com/visaplan/visaplan.plone.pdfexport


Support
-------

If you are having issues, please let us know;
please use the issue tracker mentioned above.


License
-------

The project is licensed under the GPLv2.

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
   _PDFReactor: https://www.pdfreactor.com/
