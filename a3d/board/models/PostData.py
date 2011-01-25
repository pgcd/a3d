'''
Created on 22/mag/2010

@author: pgcd
'''
from board.models.base import Auditable, ExtendedAttributesManager, Interaction, \
    Mention
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangosphinx.models import SphinxSearch #@UnresolvedImport
import re
import time
from django.db.models.query import QuerySet
import sys
#from django.core.exceptions import ObjectDoesNotExist
#from django.template.defaultfilters import slugify


class PostMixin(object):
    def public(self, user = None):
        q = models.Q(is_private = False)
        if user and user.is_authenticated():
            q = q | models.Q(_title__istartswith = '@[%s]' % user.username)
            q = q | models.Q(user = user)
        return self.filter(q)
    
    def tag_match(self, request):
        follow = request.GET.get('tag_match') #TODO: Expand this to account for usernames as well
        if follow:
            return self.filter(postdata__body__contains = follow)
        else:
            return self

class PostQuerySet(QuerySet, PostMixin):
    pass

#from board import signals as board_signals
class PostManager(models.Manager, PostMixin):
    def get_query_set(self):
        return PostQuerySet(Post, using = self._db)
            
    def get_replies(self, pk, ct, search = None, user = None):
        if search is None:
            return self.public(user).filter(object_id = pk, content_type = ct, is_active = True)
        else:
            return self.public(user).filter(object_id = pk, content_type = ct, is_active = True, postdata__body__search = search)
    
    def get_highest_rated(self, limit = 5, tag_id = None, user = None):
        queryset = self.public(user).order_by('reverse_timestamp')
        if tag_id is not None:
            queryset = queryset.filter(tags__exact = tag_id)
        return queryset[:limit]
    
    def get_for_user(self, user_id, user = None):
        return self.public(user).filter(user__exact = user_id).order_by('-updated')
    
    def ft_search(self, search_term, user = None):
        #TODO: Update to use Sphinx
        #return Post.search.query(search_term).select_related('postdata')
        return self.public(user).filter(postdata__body__search = search_term).order_by('reverse_timestamp')
    
    def get_by_tag(self, tag_id, user = None):
        if tag_id > 0:
            return self.public(user).filter(tagattach__tag__exact = tag_id).order_by('tagattach__reverse_timestamp')
        else:
            return self.public(user).filter(tagattach = None).filter(object_id = 0).order_by('reverse_timestamp') # should we also check posts?
        
    def get_home_posts(self, min_rating, user = None):
        # Should we only check threads (ie with replies or without parent)?
        list = self.public(user).filter(models.Q(rating__gte = min_rating) | \
                                           models.Q(replies_count__gt = 0) | \
                                           models.Q(object_id = 0)).order_by('reverse_timestamp')
        return list
    
class Post(Auditable, ExtendedAttributesManager):
    user = models.ForeignKey(User, related_name = '_posts', blank = True, null = True)
    content_type = models.ForeignKey(ContentType, blank = True, null = True)
    object_id = models.PositiveIntegerField(blank = True, null = True, db_index = True)
    in_reply_to = generic.GenericForeignKey()
    rating = models.IntegerField(default = 0)
    views_count = models.IntegerField(default = 0)
    replies_count = models.IntegerField(default = 0) #This should be a denorm.
    status = models.SmallIntegerField(default = 0) # make this an index WITH is_active
    versions_count = models.IntegerField(default = 0)
    ip = models.IPAddressField(default = '0.0.0.0')
    username = models.CharField(max_length = 30, blank = True, db_index = True)
    last_poster = models.ForeignKey(User, blank = True, null = True)
    last_poster_name = models.CharField(max_length = 30, blank = True, default = '') #denormalization
    reverse_timestamp = models.PositiveIntegerField(db_index = True)
    _title = models.CharField(max_length = 255, blank = True)
    read_only = models.BooleanField()
    no_replies = models.BooleanField()
    wiki = models.BooleanField()
    sticky = models.BooleanField()
    is_private = models.BooleanField()
    template_override = models.ForeignKey("Template", blank = True, null = True)
    _extended_attributes = generic.GenericRelation("ExtendedAttributeValue")
    tags = models.ManyToManyField("Tag", related_name = 'posts', through = "TagAttach")
    _replies = generic.GenericRelation('self')
    _last_reply_id = models.PositiveIntegerField(default = 0)
    search = SphinxSearch('a3d_post')
    objects = PostManager()
    mentions = models.ManyToManyField(User, related_name = 'mentions', blank = True, null = True, through = "Mention")
    
    def __unicode__(self):
        return "#%s (%s)" % (self.pk, self.title) 

    def save(self, *args, **kwargs):
        #TODO: Make some kind of duplicate check
        parent = None
        pvt_recipient = False
        try: 
            pvt_recipient = User.objects.get(username = re.search('^@\[(?P<username>[^]]+)\]', self.title).group('username'))
            self.is_private = True
        except AttributeError:
            pass

        if not bool(self.reverse_timestamp):
            self.reverse_timestamp = 0xFFFFFFFF - int(time.time())
        if self.pk: #This is an update, should perhaps do something?
            pass
        elif self.object_id: #New post, update parent accordingly
                parent = self.in_reply_to
                parent.reverse_timestamp = min(parent.reverse_timestamp, self.reverse_timestamp)
                parent.replies_count = parent.replies.count() + 1 #I'd rather hit the DB than end up with the wrong numbers
                parent.last_poster_id = self.user_id
                parent.last_poster_name = self.username
                
        _ = super(Post, self).save(*args, **kwargs) # Call the "real" save() method.
        if parent:
            parent._last_reply_id = self.pk
            parent.save()
        if pvt_recipient:
            Mention.objects.attachToPost(self, pvt_recipient)
        return _

    @models.permalink
    def get_absolute_url(self):
        return ('board_post_view', (), { 'post_id': self.pk })

    
    
    def get_smart_url(self):
        if self.replies_count or self.object_id == 0: #Not a reply, or has replies
            return reverse('board_post_view', kwargs = { 'post_id': self.pk })
        else:
            return self.parent_url + '?start=%s' % self.pk

    @property
    def title(self):
        return self._title or "#%s" % self.pk

    @property
    def title_as_reply(self): #Yeah, I don't like it either but I can't think of a better way right now.
        if self.replies_count > 0:
            return self._title or "#%s" % self.pk
        else:
            return self._title

    @property
    def last_reply(self): #TODO: Check if we want to have this return the actual object?
        return self._last_reply_id or self.pk

    @property
    def replies(self):
        return self._replies.filter(is_active = True).order_by('pk').select_related('postdata')

    @property
    def unread_replies(self):
        read_count = int(getattr(self, 'read_last_count', 0))
        return self.replies_count - read_count

    @property
    def parent_url(self):
        #model = self.content_type_id #TODO: I want to find a way of caching this
        model = ContentType.objects.get_for_id(self.content_type_id).name
        if model == 'post':
            return urlresolvers.reverse('board_post_view', kwargs = {'post_id':self.object_id}) 
        elif model == 'userprofile':
            return urlresolvers.reverse('profiles_profile_detail', kwargs = {'username':re.sub(r'/^\[\d+\]\s+/', '', self.title)})
        else:
            return self.in_reply_to.get_absolute_url()

    def has_new_replies(self):
        read_last = getattr(self, 'read_last', False)
        if not read_last or read_last < self.last_reply:
            return True
        return False

    def _can_be_rated(self, request):
        if not request.user.is_authenticated():
            return False
        if request.user.is_superuser:
            return True
        if self.user_id <> request.user.id \
                and not(hasattr(self, 'timeshift_last') or hasattr(self, 'rate_last')):
                return True

    def _can_be_edited(self, request):
        if not request.user.is_authenticated():
            return False
        if request.user.is_superuser:
            return True
        if self.wiki or self.user_id == request.user.id:
            return True
    
    def _can_be_read(self, request):
        if request.user.is_superuser:
            return True
        if self.is_private():
            return request.user.is_authenticated() and request.user.username == self.title[2:].partition(']')[0] #hackish but yields
        return True


    def with_interactions(self, request):
        if request.user.is_authenticated():
            interactions = Interaction.objects.filter(object_id = self.pk, user = request.user).values('value', 'object_id', 'interaction_type__name')
            for i in interactions:
                try:
                    i_val, i_count = i["value"].split(';')
                except ValueError:
                    i_val, i_count = [i["value"], '']
                if i_val.isdigit():
                    setattr(self, "%s_last" % i["interaction_type__name"], int(i_val))
                else: #Trying to cater to the "post count" crowd - shouldn't harm anything else. Hopefully.
                    setattr(self, "%s_last" % i["interaction_type__name"], i_val)
                if i_count.isdigit():
                    setattr(self, "%s_last_count" % i["interaction_type__name"], int(i_count))
                elif i_count:
                    setattr(self, "%s_last_count" % i["interaction_type__name"], i_count)
                    
                    
            setattr(self, 'can_be_rated', self._can_be_rated(request))
            setattr(self, 'can_be_edited', self._can_be_edited(request))
        return self

    class Meta:
        permissions = (
                     ("rate_post", "Can rate"),
                     ("timeshift_post", "Can timeshift"),
                     ("read_post", "Can read"),
                     )
        app_label = 'board'





class PostData(Post):
    #post = models.OneToOneField(Post)
    body = models.TextField()
    body_markup = models.TextField(blank = True, verbose_name = _("message body"), default = '')
    summary = models.TextField(blank = True, default = '')
    signature = models.TextField(blank = True, default = '')
    userdata = models.CharField(max_length = 255, blank = True, default = '')
    tagset = models.TextField(blank = True, default = '')
    
    
    @property
    def hashtags(self):
        def strip_brackets(s):
            return re.sub(r'^(?P<m>[#@])\[(?P<s>.+)\]$', '\g<m>\g<s>', s)
            
        if bool(self.tagset):
            _ = list(set([strip_brackets(x) for x in self.tagset.split(';')]))
            hashtags = []
            for tag in _:
                try:
                    if tag[0] == '@':
                        hashtags.append(dict(title = tag,
                                             link = urlresolvers.reverse('board_post_list_by_user',
                                             args = [tag[1:]]), rel = "contributor", klass = "follow-user user-link"))
                    elif tag[1].isdigit():
                        hashtags.append(dict(title = tag,
                                             link = urlresolvers.reverse('board_post_view',
                                             args = [tag[1:]]), rel = "related", klass = "follow-post post-link"))
                    else:
                        hashtags.append(dict(title = tag,
                                             link = urlresolvers.reverse('board_post_list_by_tag_title',
                                             args = [tag[1:]]), rel = "tag index", klass = "follow-tag tag-link"))
                except NoReverseMatch: 
                    pass
            return hashtags
        return []
    
    #Override save here, catch the tags
    def save(self, *args, **kwargs): 
        from almparse.parser import transform
        #TODO: Process @tags here
        #TODO: Make it so the parser is a user attribute
        self.body = transform(self.body_markup)
        super(PostData, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        app_label = 'board'

class PostDataVersion(Auditable):
    post = models.ForeignKey(PostData, related_name = 'versions')
    body_markup = models.TextField(blank = True, verbose_name = _("message body"), default = '')
    title = models.CharField(max_length = 255, blank = True)
    class Meta:
        app_label = 'board'
