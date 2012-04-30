from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

class ElementType(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content_type = models.ForeignKey(ContentType)
    
    description = models.TextField(blank=True)
    default_filters = models.CharField(max_length=255, blank=True,
        help_text=_("Query string filter argument to use when filtering "
                    "objects of this content type in the admin."))

    def __unicode__(self):
        return self.title
    
    @property
    def name(self):
        return slugify(self.title)

class FlatElement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    def __unicode__(self):
        return self.title