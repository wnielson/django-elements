import re

from django import template

from elements.markup import convert

register = template.Library()

@register.filter
def markup(value):
    """
    Processes markdown text and returns HTML.  Usage::
    
        {{ object.content|markup|safe }}
    """
    return convert(value)
