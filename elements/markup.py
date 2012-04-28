import markdown
import mdx_macros
import sys

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe

from elements import settings
from elements.models import ElementType

from pprint import pprint

class ElementMacro(mdx_macros.BaseMacro):
    name = "Element macro"
    key  = "El"
    
    def handler(self, title, **kwargs):
        """
        Returns a rendered Element or an empty string (or raises a
        ``TemplateSyntaxError`` in debug mode).  ``title`` should be the
        title of the desired ``ElementType``.
        """
        # TODO: stop raising TemplateSyntaxError
        
        try:
            element = ElementType.objects.get(title=title)
        except ElementType.DoesNotExist:
            if settings.DEBUG:
                raise TemplateSyntaxError, "ElementType not found."
            return ''
        
        # Try to lookup the content type
        try:
            content_type = element.content_type
            model = content_type.model_class()
            app_label = element.content_type.app_label
            model_name = element.content_type.model
        except ContentType.DoesNotExist:
            if settings.DEBUG:
                raise TemplateSyntaxError, "Element ContentType not found."
            else:
                return ''
        
        # This gets passed to the template
        context = {
            'class':                smart_unicode(kwargs.get('class', '')),
            'content_type':         "%s.%s" % (app_label, model_name),
            'content_type_class':   "%s_%s" % (app_label, model_name),
            'inline':               self.inline,
            'settings':             settings,
            'args':                 kwargs
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
        
        name = element.name
        
        # Default templates
        templates = [
            "elements/%s_%s-%s.html" % (app_label, model_name, name),
            "elements/%s_%s.html" % (app_label, model_name),
            "elements/default.html"
        ]
        
        # Owner-based templates
        if self.config.get('owner'):
            owner = self.config.get('owner')
            if isinstance(owner, models.Model):
                owner_app_label = owner._meta.app_label
                owner_model_name = owner._meta.module_name
                owner_pk = owner.pk
                
                # TODO: Support mutiple objects: 'ids'
                pk = kwargs.get('id', 0)
                
                
                templates = [
                    'elements/%s/%s/%s/%s_%s_%s.html'   % (owner_app_label,
                                                           owner_model_name,
                                                           owner_pk, app_label,
                                                           model_name, pk),
                    'elements/%s/%s/%s/%s_%s-%s.html'   % (owner_app_label,
                                                           owner_model_name,
                                                           owner_pk, app_label,
                                                           model_name, name),
                    'elements/%s/%s/%s/%s_%s.html'      % (owner_app_label,
                                                           owner_model_name,
                                                           owner_pk, app_label,
                                                           model_name),
                    'elements/%s/%s/%s/%s-%s.html'      % (owner_app_label,
                                                           owner_model_name,
                                                           owner_pk,
                                                           app_label, name),
                    'elements/%s/%s/%s/%s.html'         % (owner_app_label,
                                                           owner_model_name,
                                                           owner_pk,
                                                           app_label),
                    'elements/%s/%s/%s/default.html'    % (owner_app_label,
                                                           owner_model_name,
                                                           owner_pk),
                    'elements/%s/%s/%s_%s_%s.html'      % (owner_app_label,
                                                           owner_model_name,
                                                           app_label,
                                                           model_name, pk),
                    'elements/%s/%s/%s_%s-%s.html'      % (owner_app_label,
                                                           owner_model_name,
                                                           app_label,
                                                           model_name, name),
                    'elements/%s/%s/%s_%s.html'         % (owner_app_label,
                                                           owner_model_name,
                                                           app_label,
                                                           model_name),
                    'elements/%s/%s/%s-%s.html'         % (owner_app_label,
                                                           owner_model_name,
                                                           app_label, name),
                    'elements/%s/%s/%s.html'            % (owner_app_label,
                                                           owner_model_name,
                                                           app_label),
                    'elements/%s/%s/default.html'       % (owner_app_label,
                                                           owner_model_name),
                    'elements/%s/%s_%s_%s.html'         % (owner_app_label,
                                                           app_label,
                                                           model_name, pk),
                    'elements/%s/%s_%s-%s.html'         % (owner_app_label,
                                                           app_label,
                                                           model_name, name),
                    'elements/%s/%s_%s.html'            % (owner_app_label,
                                                           app_label,
                                                           model_name),
                    'elements/%s/%s-%s.html'            % (owner_app_label,
                                                           app_label, name),
                    'elements/%s/%s.html'               % (owner_app_label,
                                                           app_label)
                ] + templates
                
        
        # Config-defined template
        if self.config.get('template'):
            templates.insert(0, self.config.get('template'))
        
        # User-defined template
        if kwargs.has_key('template'):
            templates.insert(0, kwargs['template'])
        
        # Special context instance?
        context_instance = None
        if self.config.get('context'):
            context_instance = self.config.get('context')
        
        pprint(templates)
        
        return mark_safe(render_to_string(templates, context, context_instance))


def convert(source, owner=None, context=None, template=None):

    extensions_configs = settings.MARKDOWN_EXT_CONFIGS
    if not isinstance(extensions_configs, dict):
        extensions_configs = {}

    # TODO: Support user-defined macros
    extensions_configs.update({
        'macros': {
            'macros':   [ElementMacro],
            'owner':    owner,
            'context':  context,
            'template': template
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