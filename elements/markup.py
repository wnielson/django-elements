import markdown
import mdx_macros
import sys

#from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe

from elements import settings

class ElementMacro(mdx_macros.BaseMacro):
    name = "Element macro"
    key  = "Element"
    
    def handler(self, *args, **kwargs):
        """
        Returns a rendered Element or an empty string (or raises a
        ``TemplateSyntaxError`` in debug mode).
        """
        # We first need the app label in model name
        try:
            app_label, model_name = kwargs['type'].split('.')
        except:
            if settings.DEBUG:
                raise TemplateSyntaxError, "The Element macro attribute 'type' couldn't be found."
            else:
                return ''
        
        # Try to lookup the content type
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
            model = content_type.model_class()
        except ContentType.DoesNotExist:
            if settings.DEBUG:
                raise TemplateSyntaxError, "Inline ContentType not found."
            else:
                return ''
        
        # This gets passed to the template
        context = {
            'class':                smart_unicode(kwargs.get('class', '')),
            'content_type':         "%s.%s" % (app_label, model_name),
            'content_type_class':   "%s_%s" % (app_label, model_name),
            'inline':               self.inline,
            'settings':             settings
        }
        
        try:
            try:
                id_list = [int(i) for i in kwargs['ids'].split(',')]
                obj_list = model.objects.in_bulk(id_list)
                obj_list = list(obj_list[int(i)] for i in id_list)
                context.update({'object_list': obj_list})
            except ValueError:
                if settings.DEBUG:
                    raise ValueError, "The Element macro attribute 'ids' is missing or invalid."
                else:
                    return ''
        except KeyError:
            try:
                obj = model.objects.get(pk=kwargs['id'])
                context.update({'object': obj})
            except model.DoesNotExist:
                if settings.DEBUG:
                    raise model.DoesNotExist, "%s with pk of '%s' does not exist" % (model_name, kwargs['id'])
                else:
                    return ''
            except:
                if settings.DEBUG:
                    raise TemplateSyntaxError, "The Element macro attribute 'id' is missing or invalid."
                else:
                    return ''
        
        # TODO: Support more templates and use RequestContext somehow?
        templates = [
            "elements/%s_%s.html" % (app_label, model_name),
            "elements/default.html"
        ]
        
        # User-defined template?
        if kwargs.has_key('template'):
            templates.insert(0, kwargs['template'])
        
        return mark_safe(render_to_string(templates, context))


def convert(source):
    
    extensions_configs = settings.MARKDOWN_EXT_CONFIGS
    if not isinstance(extensions_configs, dict):
        extensions_configs = {}
    
    extensions_configs.update({
        'macros': {
            'macros': [ElementMacro]
            }
    })
    
    try:
        extensions = list(settings.MARKDOWN_EXT)
    except:
        extensions = []
    extensions.insert(0, 'macros')
    
    md = markdown.Markdown(
        extensions=extensions,
        extension_configs=extensions_configs
    )
    
    return md.convert(source)