.. django-lass-utils documentation master file, created by
   sphinx-quickstart on Thu Nov 22 10:45:15 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================
django-lass-utils
=================

*django-lass-utils* provides the :mod:`lass_utils` package, which
contains multiple models, mixins and functions that are too general to
fit into a more specific app but are depended upon by the rest of the
*LASS* project.

:mod:`lass_utils` factors out some common general patterns seen in
a large variety of models throughout *LASS*, including:

1) Models with effective date ranges
2) Models that specify types/categories of other models (similar to
   dynamic lookup/choice tables)

Contents
========

.. toctree::
    :maxdepth: 2

    licence
    contributors
    apidocs

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

