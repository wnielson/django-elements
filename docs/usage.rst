.. _usage:

Usage
=====

To convert a Markdown document with ``Elements`` contained within, you need to
first load the template tags::

    {% load elements_markup %}

Currently there is both a tag and a filter that you can use to render the
Markdown content as HTML.  The more powerful option is the template tag and
its usage is best explained with an example.  Let's pretend we've created a
``FlatPage`` who's ``content`` contains text written in Markdown with elements
contained within.  We can render the page as HTML, assuming the ``FlatPage``
object is referenced as ``flatpage``, like so::

    {% markup_elements flatpage content %}

This template tag is more powerful than the filter described below, because
each element contained within this ``FlatPage`` is "aware" of the context in
which is is being rendered.  Again, this concept is more easily explained with
and example.

Let's consider a very simple application, which we'll call ``media``, that has
a very simple model::

    from django.db import models
    
    class MediaItem(models.Model):
        title = models.CharField(max_length=255)
        file = models.FileField()
        caption = models.TextField(blank=True)

Now let's also pretend that we've created an ``ElementType`` for this model,
titled "Image".  This means that we can now add an "Image" into a
``FlatPage`` like so, assuming we've uploaded an image with ``pk=1``::

    Here is some flatpage content.  Let's go ahead an insert an image:
    
    [[El('Image', id=1)]]

To recap what we've got currently:

  * A ``FlatPage`` with ``pk=2`` and ``content`` shown above
  * An ``ElementType`` titled "Image"
  * An ``MediaItem`` with ``pk=1`` from the ``media`` application

Now we can control how the ``Image`` above is actually rendered into HTML
by defining various templates.  Here is the order in which templates will
be searched:

  * :file:`elements/flatpages/flatpage/2/media_mediaitem_1.html`
  * :file:`elements/flatpages/flatpage/2/media_mediaitem-image.html`
  * :file:`elements/flatpages/flatpage/2/media_mediaitem.html`
  * :file:`elements/flatpages/flatpage/2/media-image.html`
  * :file:`elements/flatpages/flatpage/2/media.html`
  * :file:`elements/flatpages/flatpage/2/default.html`
  * :file:`elements/flatpages/flatpage/media_mediaitem_1.html`
  * :file:`elements/flatpages/flatpage/media_mediaitem-image.html`
  * :file:`elements/flatpages/flatpage/media_mediaitem.html`
  * :file:`elements/flatpages/flatpage/media-image.html`
  * :file:`elements/flatpages/flatpage/media.html`
  * :file:`elements/flatpages/flatpage/default.html`
  * :file:`elements/flatpages/media_mediaitem_1.html`
  * :file:`elements/flatpages/media_mediaitem-image.html`
  * :file:`elements/flatpages/media_mediaitem.html`
  * :file:`elements/flatpages/media-image.html`
  * :file:`elements/flatpages/media.html`
  * :file:`elements/media_mediaitem-image.html`
  * :file:`elements/media_mediaitem.html`
  * :file:`elements/default.html`


This means we can define a template that will dictate how this "Image" element
will render for this ``FlatPage`` (and only this particular ``FlatPage``) via
the :file:`elements/flatpages/flatpage/2/media_mediaitem_1.html`, or we can
simply define a more generic template that will define how to render any
"Image" for any ``FlatPage`` via the
:file:`elements/flatpages/flatpage/media_mediaitem-image.html`.
