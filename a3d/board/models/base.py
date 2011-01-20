'''
Created on 22/mag/2010

@author: pgcd
'''
import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

#from board import signals as board_signals


class Auditable(models.Model):
    """
    Base abstract model for models we wish to keep track of
    """
    created = models.DateTimeField(default = datetime.datetime.now, editable = False)
    updated = models.DateTimeField(default = datetime.datetime.now, editable = False)
    is_active = models.BooleanField(default = True, editable = False)
    
    class Meta:#IGNORE:W0232
        abstract = True
        app_label = 'board'
        
    
    def save(self, *args, **kwargs):
        if not kwargs.get('no_update'):
            self.updated = datetime.datetime.now()
        else:
            del kwargs['no_update']
        super(Auditable, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save(*args, **kwargs)

#class Attachable(models.Model):

class ExtendedAttribute(models.Model):
    """
    Vertical-table like structure to store fully normalized attributes types
    """
    name = models.CharField(max_length = 32)
    def __unicode__(self):
        return self.name
    class Meta:#IGNORE:W0232
        app_label = 'board'

    
class ExtendedAttributeValue(models.Model):
    """
    The actual attributes values.
    """
    key = models.ForeignKey(ExtendedAttribute)
    value = models.CharField(max_length = 255)    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index = True)
    content_object = generic.GenericForeignKey()
    def __unicode__(self):
        return "%s: %s" % (self.key, self.value)
    class Meta:#IGNORE:W0232
        app_label = 'board'


class ExtendedAttributesManager(object):
    @property
    def extended_attributes(self):
        """ This is the getter
        """
        extended_attrs = self._extended_attributes.values("key", "value")
        extended_keys = dict([(i.get("id"), i.get("name")) for i in ExtendedAttribute.objects.filter(pk__in = [k.get("key") for k in extended_attrs]).values()])
        extend = {}
        for k in extended_attrs: 
            keyname = extended_keys[k.get("key")]
            if extend.get(keyname) is None:
                extend[keyname] = []
            extend[keyname].append(k.get("value"))
        return extend    


class Ignore(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    def __unicode__(self):
        return "%s: %s" % (self.user, self.content_object)
    class Meta:#IGNORE:W0232
        app_label = 'board'


class Template(Auditable):
    name = models.CharField(max_length = 255)
    body = models.TextField()
    parent = models.ForeignKey('self', related_name = 'derived', null = True, blank = True) #todo
    def __unicode__(self):
        return self.name
    class Meta:#IGNORE:W0232
        app_label = 'board'

#class Thread(Auditable):
##    category = models.ForeignKey(Category, related_name='threads')
#    first_post=models.ForeignKey("Post")
#    user=models.ForeignKey(User, related_name='started_threads')
#    last_poster=models.ForeignKey(User)
#    reverse_timestamp=models.DateTimeField()
#    title=models.CharField(max_length=255)
#    top_lock=models.BooleanField()
#    _extended_attributes=generic.GenericRelation(ExtendedAttributeValue)
#    def __unicode__(self):
#        return "%s (%s %s)"%(self.title, self.user, self.created)
    
class MentionManager(models.Manager):
    use_for_related_fields = True
    def attachToPost(self, post, user):
        try:
            return self.create(post = post, user = user)
        except IntegrityError: #duplicate mention
            return False
    
class Mention(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey("Post")
    objects = MentionManager()
    class Meta:
        app_label = 'board'
        unique_together = ['user', 'post']
        get_latest_by = 'id'
        ordering = ['-id']
#        order_with_respect_to = 'user'

class InteractionTypeManager(models.Manager):
    _cache = {} #very basic caching stolen from contenttypes
    
    def get_type_for_model(self, interaction_type, ct = None):
        key = "%s:%s" % (interaction_type, ct.name.lower()) 
        try:
            it = self.__class__._cache[key]
        except KeyError:
            #TODO: Some kind of fallback
            it = self.get(name = interaction_type, content_type = ct)
            self.__class__._cache[key] = it
        return it
    
class InteractionType(Auditable): #any reason to keep this stuff here?
    name = models.CharField(max_length = 30)
    info = models.TextField(blank = True)
    content_type = models.ForeignKey(ContentType) # Each interaction type can only deal with a single content type
    objects = InteractionTypeManager()

    class Meta:#IGNORE:W0232
        unique_together = ['name', 'content_type', ]
        app_label = 'board'
    
    def __unicode__(self):
        return "%s %s" % (self.name, self.content_type)

class InteractionManager(models.Manager):
    def prepare(self, sender, user = None, interaction_type = None, object_id = None, content_type = None, **kwargs):
        """
        This method should return an Interaction instance to be used by the actual event handlers
        """
        if not user.is_authenticated():
            return False
        ct = content_type or ContentType.objects.get_for_model(sender)
        it = InteractionType.objects.get_type_for_model(interaction_type, ct) 
        try:
            i = Interaction.objects.get(user = user, object_id = object_id, interaction_type = it)
        except ObjectDoesNotExist:
            i = Interaction(user = user, object_id = object_id, interaction_type = it)
        return i


class Interaction(Auditable):
    """
    This class deals _ONLY_ with overwriting interactions; i.e. interactions that do not require an history but only the most recent value.
    """
    user = models.ForeignKey(User, related_name = 'interactions')
    interaction_type = models.ForeignKey(InteractionType, related_name = 'interactions')
    value = models.TextField()
    object_id = models.PositiveIntegerField(default = 0)
    objects = InteractionManager()
    def __unicode__(self):
        return "%s: %s %s - %s" % (self.user, self.interaction_type, self.object_id, self.value)
    class Meta: #IGNORE:W0232
        unique_together = ['user', 'interaction_type', 'object_id', ]
        app_label = 'board'
