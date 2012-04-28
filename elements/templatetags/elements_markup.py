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


class MarkupElementsNode(template.Node):
    def __init__(self, obj, field, var_name=None):
        self.obj = template.Variable(obj)
        self.field = field
        self.var_name = var_name
    
    def render(self, context):
        obj = self.obj.resolve(context)
        data = getattr(obj, self.field, '')
        content = convert(data, obj, context)
        
        if self.var_name:
            context[self.var_name] = content
            return ''
        return content

@register.tag(name="markup_elements")
def do_markup_elements(parser, token):
    """
    Object-aware element markup tag.  This should be used instead of the
    simpler `markup` filter when you want the content to be rendered with
    respect to the object that it belongs to.  For example, let's say you have
    a ``Post`` model with a ``content`` field which contains some ``Element``
    macros in the textual content. By using this tag, the ``Elements`` will be
    aware of the fact that they belong to a blog ``Post``.
    
    Usage::
    
        {% markup_elements [object] [field] as [var name] %}
    """
    bits = token.split_contents()
    if len(bits) < 3:
        raise template.TemplateSyntaxError("%r tag requires at least two arguments" % bits[0])
    if len(bits) > 5:
        raise template.TemplateSyntaxError("%r tag accepts at most 4 arguments" % bits[0])
    
    obj = bits[1]
    field = bits[2]
    var_name = None
    
    if len(bits) > 4:
        if bits[3] != "as":
            raise template.TemplateSyntaxError("%r has been used incorrectly" % bits[0])
        var_name = bits[4]
    
    return MarkupElementsNode(obj, field, var_name)
    