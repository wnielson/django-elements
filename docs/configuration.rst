.. _configuration:

Configuration
=============

Admin Integration
-----------------

If you installed `django-markitup`_, and you'd like to have the ``MarkItUp``
editor enabled for text areas in the admin, then you need to create special
templates.  For example, let's say you'd like to add the editor to Django's
``flatpages`` application.  In your templates directory, create the following
file: ``admin/flatpages/flatpage/change_form.html``, and add the following
content::

    {% extends "admin/change_form.html" %}

    {% load markitup_tags %}

    {% block extrahead %}
      {{ block.super }}
      {% markitup_media %}
    {% endblock %}


    {% block content %}
      {{ block.super }}
      {% markitup_editor "id_content" %}
    {% endblock %}

You can repeat this for any other text area you'd like to add the editor to.

.. _django-markitup: http://bitbucket.org/carljm/django-markitup/

Settings
--------

There are a few settings that let you control the behavior of
``django-elements``.

**ELEMENTS_MARKDOWN_EXT**

The ``ELEMENTS_MARKDOWN_EXT`` directive allows you to define extra
`python-markdown`_ extensions to use in the Markdown rendering.  The default
is::

    ELEMENTS_MARKDOWN_EXT = (
        'toc',
        'tables',
        'abbr',
        'footnotes',
        'def_list',
        'headerid',
        'meta',
        'codehilite'
    )

For a complete list of available extenstions, see `this page`_.  Additionally,
if you'd like to take advantage of the ``codehilite`` extension, you'll need to
install `pygments`_::

    pip install pygments

.. _python-markdown: http://freewisdom.org/projects/python-markdown/ 
.. _this page: http://freewisdom.org/projects/python-markdown/Available_Extensions
.. _pygments: http://pygments.org/

**ELEMENTS_MARKDOWN_EXT_CONFIGS**

This directive allows you to pass extra extension-specific config options to
to Markdown processor.  The default is::

    ELEMENTS_MARKDOWN_EXT_CONFIGS = {}