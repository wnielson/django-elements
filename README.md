django-elements
===============

This application is designed to provide an easy way to embed arbitrary objects
into textual content.  Text is written in [Markdown][] and objects can be inserted,
as either inline or block-level elements, using a simple [Trac-like macro][]
syntax.  For more details check out the [docs][].

[Markdown]: http://daringfireball.net/projects/markdown/
[Trac-like macro]: http://trac.edgewall.org/wiki/WikiMacros
[docs]: http://readthedocs.org/docs/django-elements/en/latest/

Installation
------------

The first step is to install the prerequisites.  The only **required** package
is ``markdown-macros``, which can be installed via PyPI (using ``pip`` or
``easy_install``):

    pip install markdown-macros

Optionally, if you'd like a nice editor for use in the admin, you can install
``django-markitup``:

    pip install django-markitup==tip

Credits
-------

This project was inspired by Nathan Borror's [django-basic-apps][] inlines
application.

[django-basic-apps]: https://github.com/nathanborror/django-basic-apps.