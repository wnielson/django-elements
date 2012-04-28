.. _installation:

Installation
============

The first step is to add ``elements`` to your ``INSTALLED_APPS``
setting inside :file:`settings.py`::

    INSTALLED_APPS = (
        ...
        'elements',
    )

Then run ``syncdb``::

    python manange.py syncdb

That's it for the required steps.

Optional Steps
--------------

If you want to make editing in the admin easier, then you'll probably want to
install ``django-markitup``::

    pip install django-markitup==tip

``django-elements`` ships with an extended Markdown syntax set for the
javascript-based ``MarkItUp`` editor provided in ``django-markitup``.  To enable
it, add the following to your :file:`settings.py`::

    MARKITUP_FILTER = ('elements.markup.convert', {})
    MARKITUP_SET = 'elements/markitup/markdown'

Then run ``collectstatic``::

    python manage.py collectstatic

