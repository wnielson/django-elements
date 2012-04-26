django-elements
===============

This application is designed to provide an easy way to embed arbitrary objects
into textual content.  Text is written in [Markdown][] and objects can be inserted,
as either inline or block-level elements, using a simple [Trac-like macro][]
syntax.  As a simple example, here is some text written in Markdown using
`django-elements`:

    Let's assume that [django-filer][] is installed.  If I want to embed an
    image into this content, all I have to do is this
    `[[Element(type='filer.image', id='1')]]`.  So, here is the image, which
    will be rendered as a block-level element:
	
    [[Element(type='filer.image', id='1')]]
	
    See how easy it is to insert arbitrary objected into a Markdown-based
    document?
	
    You can also embed an item inline by simply adding it in the location you
    want.  For example, here is an image that has been placed inline with the
    text [[Element(type='filer.image', id='2')]].
	
    [django-filer]: https://github.com/stefanfoulis/django-filer

[Markdown]: http://daringfireball.net/projects/markdown/
[Trac-like macro]: http://trac.edgewall.org/wiki/WikiMacros

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