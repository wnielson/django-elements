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

#@register.filter
#def extract_inlines(value):
#    return inlines(value, True)
#
#
#class InlineTypes(template.Node):
#    def __init__(self, var_name):
#        self.var_name = var_name
#
#    def render(self, context):
#        types = InlineType.objects.all()
#        context[self.var_name] = types
#        return ''
#
#@register.tag(name='get_inline_types')
#def do_get_inline_types(parser, token):
#    """
#    Gets all inline types.
#
#    Syntax::
#
#        {% get_inline_types as [var_name] %}
#
#    Example usage::
#
#        {% get_inline_types as inline_list %}
#    """
#    try:
#        tag_name, arg = token.contents.split(None, 1)
#    except ValueError:
#        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
#    m = re.search(r'as (\w+)', arg)
#    if not m:
#        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
#    var_name = m.groups()[0]
#    return InlineTypes(var_name)