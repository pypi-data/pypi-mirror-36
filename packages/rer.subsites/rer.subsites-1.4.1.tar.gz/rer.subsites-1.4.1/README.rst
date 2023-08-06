==============================================================================
rer.subsites
==============================================================================

.. image:: https://travis-ci.org/PloneGov-IT/rer.subsites.svg?branch=master
    :target: https://travis-ci.org/PloneGov-IT/rer.subsites

Subsites implementation for RER.


Features
--------

- No additional portal-types
- Viewlet with subsite's customizable color and background image in every subsite children
- Control panel where set additional styles for the subsite

Enable a subsite
----------------

Folderish contents has a new "`Set as subsite`" action that mark them as a subsite.

Disable a subsite
-----------------

Folderish contents marked as a subsite, have a new "`Unset as subsite`" action that unmark them as a subsite.


Subsite settings
----------------

A subsite has a new voice in the toolbar: Subsite styles.
In this view we can set two parameters:
- subsite color
- background image

These parameters are used to style the subsite header (viewlet)
The styles are combined in a custom viewlet that inject them like css styles.

Customize subsite layout
------------------------

There is a configuration in the site control-panel with a text-area where you can insert some custom
css rules that will be applied only in subsites and their children.

This is useful for example if all headers (<h1> or <h2>) in the subsite should have the same color of the subsite.


Translations
------------

This product has been translated into

- Italian


Installation
------------

Install rer.subsites by adding it to your buildout::

   [buildout]

    ...

    eggs =
        rer.subsites


and then running "bin/buildout"


Compatibility
-------------
This package is fully compatible for Plone 5.


Contribute
----------

- Issue Tracker: https://github.com/PloneGov-IT/rer.subsites/issues
- Source Code: https://github.com/PloneGov-IT/rer.subsites


License
-------

The project is licensed under the GPLv2.
