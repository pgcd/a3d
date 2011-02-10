'''
Created on 22/mag/2010

@author: pgcd
'''
from django.db import models
#from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
#from django.conf import settings
import datetime

from board.models.base import Auditable, ExtendedAttributesManager
from django.template.defaultfilters import slugify

class TagAttach(models.Model):
    tag = models.ForeignKey("Tag")
    post = models.ForeignKey("Post")
    reverse_timestamp = models.PositiveIntegerField(blank = True, default = 0)
    
    
    def __unicode__(self):
        return "%s: %s" % (self.tag, self.post)
    def save(self, *args, **kwargs):
        if self.reverse_timestamp is None and self.post is not None:
            self.reverse_timestamp = self.post.reverse_timestamp
        t = self.tag
        t.attach_count = t.tagattach_set.count()
        #=======================================================================
        # NOTE: The following is meant to reflect the date of the attached post
        #=======================================================================
        t.last_attach = datetime.datetime.fromtimestamp(0xFFFFFFFF - self.reverse_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        t.reverse_timestamp = self.reverse_timestamp
        t.save()
        super(TagAttach, self).save(*args, **kwargs)
        
    class Meta:
        unique_together = ('tag', 'post')
        app_label = 'board'

class Tag(Auditable, ExtendedAttributesManager):
    """A tag on an item."""
    title = models.SlugField(unique = True)
    #I removed this, as it should be dealt with in CSS
    reverse_timestamp = models.PositiveIntegerField(blank = True, default = 0)
    last_attach = models.DateTimeField(default = datetime.datetime.now)
    icon = models.FileField(upload_to = 'tag', blank = True, default = '')
    attach_count = models.PositiveIntegerField(default = 0)
    template = models.ForeignKey('Template', null = True, blank = True) #TODO: Make this have some meaning?
    _extended_attributes = generic.GenericRelation("ExtendedAttributeValue")
    description = models.TextField(blank = True)
    #posts = models.ManyToManyField("Post", through="TagAttach")

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('board_post_list_by_tag_title', (), { 'tag_title': self.title })
    
    class Meta:
        app_label = 'board'
