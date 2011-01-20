#This file is encoded with UTF-8
'''
Created on 22/mag/2010

@author: pgcd
'''
from almparse.signals import parsing_done
from board import signals as board_signals
from board.models.PostData import *
from board.models.Tag import Tag, TagAttach
from board.models.UserProfile import UserProfile
from board.models.base import *
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
import urllib
from django.utils.html import escape
#from django.conf import settings




# Create your models here.



def home_read_handler(sender, user = None, last_item = None, **kwargs):
    i = Interaction.objects.prepare(sender, user, 'read', object_id = 0)
    if not bool(i):
        return False
    if not i.value.isdigit() or int(i.value) < last_item:
        try:
            i.value = max(int(i.value), last_item)
        except ValueError:
            i.value = last_item
        i.save()
        return True
    return False

def post_read_handler(sender, user = None, obj_id = None, last_item = None, **kwargs):
    i = Interaction.objects.prepare(sender, user, 'read', object_id = obj_id)
    if not bool(i):
        return False
    try:
        last_item_id, last_item_count = last_item.split(';')
    except ValueError: #Very uncertain about these.
        last_item_id, last_item_count = ['0', '0']
    try:
        previous_id, _ = i.value.split(';')
    except ValueError: #Unable to unpack
        previous_id, _ = ['0', '0']
    if not previous_id.isdigit() or previous_id < last_item_id:
        i.value = "%s;%s" % (last_item_id, int(last_item_count))
        i.save()
        return True
    return False

def tag_read_handler(sender, user = None, tag_id = None, last_item = None, **kwargs):
    i = Interaction.objects.prepare(sender, user, 'read', object_id = tag_id)
    if not bool(i):
        return False
    if not i.value.isdigit() or int(i.value) > -last_item:
        i.value = -last_item
        i.save()
        return True
    return False


def interaction_event_handler(sender, request = None, user = None, object_id = None, value = None, interaction_type = '', **kwargs):
    i = Interaction.objects.prepare(sender, user, interaction_type, object_id = object_id)
    try:
        i.value = ';'.join(i.value.split(';').append(value))
    except TypeError:
        i.value = value 
    i.save()
    return True



#TODO: Ok, I'm seriously unhappy with this. It will be merged with almparse.
def parse_tags_in_body(sender, instance = None, **kwargs):
    """
    Finds all hashtags in instance.body, adds them to instance.tagset (;-separated) and replaces them with links.
    """
    def replace_tags(match):
        i = re.sub(r'^(?P<m>[#@])\[(?P<s>.+)\]$', '\g<m>\g<s>', match.group())
        if i[0] == '#': #Hashtag
            tag = slugify(i[1:])
            if not tag[0].isdigit():
                hashtags.append('#%s' % tag)
                tag_href = urlresolvers.reverse('board_post_list_by_tag_title', kwargs = {'tag_title':tag})
                return '<a href="%s" class="tag-link" rel="tag index">%s</a>' % (tag_href, escape(match.group()))
            else:
                tag_href = urlresolvers.reverse('board_post_view', kwargs = {'post_id':i[1:]})
                return '<a href="%s" class="post-link" rel="related">%s</a>' % (tag_href, i)
        elif i[0] == '@':
            hashtags.append(i)
            tag_href = urlresolvers.reverse('profiles_profile_detail', kwargs = {'username':i[1:]})
            return '<a href="%s" class="user-link" rel="contributor">%s</a>' % (tag_href, escape(match.group()))

    hashtags = []
    instance.body = re.sub(r'(?=(?<=^)|(?<=\s|\n|>))((?:@|#)(?:[-\w]+|\[.*?[^|]\]))', replace_tags, instance.body)
    instance.tagset = ";".join(list(set(hashtags))) #remove duplicates

def parse_mentions(sender, instance = None, **kwargs):
    '''
    @param sender: PostData
    @param instance: PostData instance
    Clears the post's mentioned_users, then adds all the mentions found in the tagset.
    '''
    post = instance.post_ptr
    Mention.objects.filter(post = post).delete()

    mentions = instance.tagset.split(';')
    mentions = list(set(mentions))
     
    for m in mentions:
        if m.startswith('@'):
            try:
                Mention.objects.create(post = post, user = User.objects.get(username = m[1:]))
            except User.DoesNotExist: #@UndefinedVariable
                pass
    
     

def pd_created_handler(sender, request = None, instance = None, **kwargs):
    u = request.user
    if not u.is_authenticated():
        return False
    if instance.object_id:
        i = Interaction.objects.prepare(sender, request.user, 'replied', object_id = instance.object_id, content_type = instance.content_type)
        if not bool(i): #Not authenticated user, should never happen
            return False
        if not i.value.isdigit() or int(i.value) < instance.pk:
            i.value = instance.pk
            i.save()
    #You should be counted as having read your own post.
    i = Interaction.objects.prepare(sender, request.user, 'read', object_id = instance.pk, content_type = ContentType.objects.get_for_model(Post))
    if not bool(i): #Not authenticated user, should never happen
        return False
    i.value = instance.pk
    i.save()
    
    up = u.get_profile()
    up.last_post = instance #TODO: Several other fields need updating, probably - mana, for instance 
    up.posts_count = up.posts_count + 1 
    up.save()
    return True

board_signals.home_read.connect(home_read_handler, dispatch_uid = "board.postdata")
board_signals.post_read.connect(post_read_handler, dispatch_uid = "board.postdata")
board_signals.tag_read.connect(tag_read_handler, dispatch_uid = "board.postdata")
board_signals.interaction_event.connect(interaction_event_handler, dispatch_uid = "board.postdata")
board_signals.postdata_created.connect(pd_created_handler, dispatch_uid = "board.postdata")

pre_save.connect(parse_tags_in_body, sender = PostData, dispatch_uid = "board.postdata")
post_save.connect(parse_mentions, sender = PostData, dispatch_uid = "board.postdata")
