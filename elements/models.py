from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

class ElementType(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content_type = models.ForeignKey(ContentType)

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