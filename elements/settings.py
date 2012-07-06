from django.conf import settings

DEBUG = getattr(settings, 'DEBUG', False)

MARKDOWN_EXT = getattr(settings, "ELEMENTS_MARKDOWN_EXT", ['toc', 'tables', 'abbr', 'footnotes', 'def_list', 'headerid', 'meta', 'codehilite', 'video', 'subscript', 'superscript', 'extra'])

MARKDOWN_EXT_CONFIGS = getattr(settings, "ELEMENTS_MARKDOWN_EXT_CONFIGS", {})