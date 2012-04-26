from django.contrib import admin
from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.utils import simplejson as json

from elements.models import ElementType, FlatElement

FIELDS = (
    'id',
    'title',
    'content_type__name',
    'content_type__model',
    'content_type__app_label'
)

class ElementTypeAdmin(admin.ModelAdmin):
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