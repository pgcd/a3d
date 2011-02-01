'''
Created on 22/mag/2010

@author: pgcd
'''
from board.models.PostData import Post
from board.models.Tag import Tag
from board.models.base import ExtendedAttributesManager, Ignore, \
    InteractionType, Interaction
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.query_utils import Q
from django.utils.translation import ugettext_lazy as _
from faves.models import Fave
import datetime
import operator
import sys
#from django.core.exceptions import ObjectDoesNotExist
#from django.template.defaultfilters import slugify

#from denorm import CountField, denormalized, depend_on_related

#from board import signals as board_signals

class UserProfile(models.Model, ExtendedAttributesManager):
    user = models.ForeignKey(User, unique = True, related_name = 'profile')
    hidden_status = models.BooleanField(default = False)
    hidden_email = models.BooleanField(default = False)
    rating_total = models.IntegerField(default = 0)
    signature = models.TextField(blank = True)
    secret_question = models.TextField(blank = True)
    secret_answer = models.TextField(blank = True)
    short_desc = models.CharField(max_length = 255, blank = True)
    long_desc = models.TextField(blank = True)
    custom_nick_display = models.TextField(blank = True)
    mod_denied = models.BooleanField(blank = True)
    auto_login = models.BooleanField(blank = True)
    back_to_topic = models.BooleanField(blank = True)
    auto_quote = models.BooleanField(blank = True)
    link_source_post = models.BooleanField(blank = True)
    always_preview = models.BooleanField(blank = True)
    can_modify_profile_own = models.BooleanField(blank = True)
    can_set_nick_color = models.BooleanField(blank = True)
    can_change_short_desc = models.BooleanField(blank = True)
    show_ruler = models.BooleanField(blank = True)
    save_password = models.BooleanField(blank = True)
    contributor = models.BooleanField(blank = True)
    is_alias = models.BooleanField(blank = True)
    post_per_page = models.SmallIntegerField(blank = True, default = 30)
    min_rating = models.SmallIntegerField(blank = True, default = 2)
    mana = models.IntegerField(default = 0)
    last_post = models.ForeignKey("Post", blank = True, null = True, related_name = "posted_by")
    posts_count = models.IntegerField(blank = True, default = 0)
    _extended_attributes = generic.GenericRelation("ExtendedAttributeValue")
    ignores = generic.GenericRelation(Ignore)
    _replies = generic.GenericRelation("Post")
    _last_reply_id = models.PositiveIntegerField(default = 0, blank = True)
    reverse_timestamp = models.PositiveIntegerField(default = 0)
    replies_count = models.IntegerField(default = 0) #This should be a denorm.
    last_page_url = models.CharField(max_length = 255, blank = True, default = '')
    last_page_time = models.DateTimeField(default = datetime.datetime.now(), db_index = True)

    def __unicode__(self):
        return self.user.username
    
    @models.permalink
    def get_absolute_url(self):
        name = self.user.username
#        name=name+'\x01' if name.endswith('.') else name
        return ('profiles_profile_detail', (), { 'username':  name})

    @models.permalink
    def get_replies_url(self):
        name = self.user.username
        return ('board_profile_view_replies', (), { 'username':  name})

    
    @property
    def replies(self):
        return self._replies.filter(is_active = True).select_related('postdata')
    
    @property
    def last_reply(self): #TODO: Check if we want to have this return the actual object?
        return self._last_reply_id

    @property
    def posts(self):
        return self.user._posts.select_related('user', 'postdata').order_by('-pk')


    @property
    def interactions(self):
        return Interaction.objects.filter(user = self)

    @property
    def favorites(self):
        faves = Fave.objects.get_for_user(self.user)
        post_ct = ContentType.objects.get_for_model(Post).pk 
        tag_ct = ContentType.objects.get_for_model(Tag).pk
#        userprofile_ct = ContentType.objects.get_for_model(UserProfile).pk
        userpost_ct = ContentType.objects.get_for_model(User).pk
    
        fl = {
            post_ct:[],
           tag_ct:[],
#           userprofile_ct:[],
           userpost_ct:[],
           }
        itypes = InteractionType.objects.filter(name = 'read', content_type__in = fl).values('content_type_id', 'pk')
        ctypes = dict((i["pk"], i["content_type_id"]) for i in itypes)
        for f in faves:
            fl[f.content_type_id].append(f.object_id)
        fave_list = dict((i["pk"], fl[i["content_type_id"]]) for i in itypes)
        q = Q()
        for itype, f in fave_list.iteritems():
            q = q | (Q(interaction_type = itype) & Q(object_id__in = f))
        
        last_interactions = {}
        for li in self.interactions.filter(q):
            try:
                ct = ctypes[li.interaction_type_id]
                if not last_interactions.has_key(ct):
                    last_interactions[ct] = {}
                last_interactions[ct][li.object_id] = li
            except KeyError:
                pass
            
        faved_objects = {}
        faved_objects[post_ct] = dict((o.pk, {'last':o.last_reply, 'obj':o, 'type':'post'}) for o in Post.objects.filter(pk__in = fl[post_ct]))
        faved_objects[tag_ct] = dict((o.pk, {'last': o.reverse_timestamp, 'obj':o, 'op':operator.gt, 'type':'tag'}) for o in Tag.objects.filter(pk__in = fl[tag_ct]))
#        faved_objects[userprofile_ct] = dict((o.pk, {'last':o.last_reply, 'obj':o, 'type':'userprofile'}) for o in UserProfile.objects.filter(pk__in = fl[userprofile_ct]))
        faved_objects[userpost_ct] = dict((o.pk, {'last':o.get_profile().last_post_id, 'obj':o, 'type':'user'}) for o in User.objects.filter(pk__in = fl[userpost_ct]))

        link_prefix = {
           post_ct:'&para;',
           tag_ct:'.',
           userpost_ct:'@',
#           userpost_ct:'by: ',
           }

        
        for f in faves:
            ct = f.content_type_id
            oid = f.object_id
            fo = faved_objects[ct][oid]
            obj = fo['obj']
            try: #TODO: Should we link to the last interaction or to the starting point?
                f.link_start = int(last_interactions[ct][oid].value.split(';')[0])
            except KeyError: #This shouldn't actually ever happen, because there _should_ be an interaction of sorts.
                f.link_start = 0
                
            if fo['type'] == 'user':
                f.link_href = reverse('profiles_profile_detail', kwargs = {'username':obj.username})
            else:
                f.link_href = obj.get_absolute_url()
            f.link_title = link_prefix[ct] + getattr(obj, 'title', obj.__unicode__()) 
            f.current = fo['last']
            f.fresh = fo.get('op', operator.lt)(f.link_start, f.current)
            f.remove = reverse('unfave_object', kwargs = {'fave_type_slug':'star', 'content_type_id': ct, 'object_id': oid})
        return faves
    
    
    def save(self, *args, **kwargs):
        if not bool(self._last_reply_id):
            self._last_reply_id = self.pk
        super(UserProfile, self).save(*args, **kwargs) # Call the "real" save() method.    

    class Meta:
        app_label = 'board'
