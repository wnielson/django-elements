from django.contrib import admin
from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.utils import simplejson as json

from elements.models import ElementType, FlatElement

FIELDS = (
    'id',
    'title',
    'default_filters',
    'content_type__name',
    'content_type__model',
    'content_type__app_label'
)

class ElementTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'element_name', 'app_label', 'model_name')
    list_filter = ('content_type__app_label',)
    
    def app_label(self, obj):
        return obj.content_type.app_label
    app_label.admin_order_field = 'content_type__app_label'
    
    def model_name(self, obj):
        return obj.content_type.model
    model_name.admin_order_field = 'content_type__model'
    
    def element_name(self, obj):
        return obj.name
    element_name.short_description = 'name'
    element_name.admin_order_field = 'title'
    
    def get_urls(self):
        urls = super(ElementTypeAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^get_types/$', self.admin_site.admin_view(self.get_types), name="elements_get_types")
        )
        return my_urls + urls
    
    def get_types(self, request):
        data = []
        for element in ElementType.objects.values(*FIELDS):
            d = {}
            for k, v in element.items():
                d[k] = str(v)
            data.append(d)
        return HttpResponse(json.dumps(data), mimetype="application/json")

admin.site.register(ElementType, ElementTypeAdmin)
admin.site.register(FlatElement)