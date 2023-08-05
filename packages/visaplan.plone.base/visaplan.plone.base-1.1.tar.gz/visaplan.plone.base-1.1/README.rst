.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

===================
visaplan.plone.base
===================

This package simply collects some basic constants etc. (e.g. permission names)
which are used by other packages, e.g. ``visaplan.plone.browsers``.

It is part of the footing of the "Unitracc family" of Plone sites
which are maintained by visaplan GmbH, Bochum, Germany.

Some parts of this package might be outdated now and not anymore considered to
follow Plone's current Best Practices.  The reason is:

The purpose of this package (for now) is *not* to provide new functionality
but to factor out existing functionality from our former monolithic Zope product.
Later versions might reflect more recent insights and/or the requirements of
more recent Zope/Plone versions.

This package does still contain some resources (e.g. permission names) which
are specific to our "Unitracc family" of sites; thus, we considere it more
likely you to create your own *yourcompany*.plone.base fork than to use this
package directly.


Features
--------

- ``exceptions`` module

  - Provides the ``UnitraccBaseException`` class which supports the
    localization of error messages which are presented to the users

  - Some more exception classes.

- ``permissions`` module

  Imports some permission names from the Zope/Plone packages,
  and adds some proprietary permission names from our "Unitracc family".

- ``typestr`` module

  Creates dictionaries for the localization (l10n) of strings related to object
  type names; e.g., for your portal_type ``thingy`` you might want a Gettext
  message id ``thingies``, and perhaps as well ``My thingies`` and others.

  When calles as a script, the module creates a honeypot file for use by
  extraction tools.

- ``adapter`` module

  A "Base" class for the adapters of ``visaplan.plone.adapters``
  which saves the ``context`` (given during adapter creation) to an attribute
  and calls (probably for historical reasons) the ``reference_catalog`` tool
  (this may change in the future).

- the ``browserview`` module

  Provides an extended version of the ``Products.Five.BrowserView``
  (hwich may as well change in the future).


Examples
--------

This add-on can be seen in action at the following sites:

- https://www.unitracc.de
- https://www.unitracc.com


Installation
------------

Install visaplan.plone.base by adding it to your buildout::

    [buildout]

    ...

    eggs =
        visaplan.plone.base


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/visaplan/visaplan.plone.base/issues
- Source Code: https://github.com/visaplan/visaplan.plone.base


Support
-------

If you are having issues, please let us know;
please use the issue tracker mentioned above.


License
-------

The project is licensed under the GPLv2.

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
