'''
Created on 24/mar/2010

@author: pgcd
'''
from django import template
import datetime
#from django.views.generic.list_detail import object_list
from board.models import Tag, UserProfile, Interaction
#from django.contrib.contenttypes.models import ContentType
from board import forms as board_forms
#from board.paginator import Paginator
from board.decorators import parsingTag
#from django.template import RequestContext
#from django.core.urlresolvers import reverse
#from django.template.loader import render_to_string    
from django.views.decorators.csrf import csrf_protect
from django.utils import simplejson
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.contrib.humanize.templatetags import humanize

register = template.import_library("board.decorators")


#@ parsingTag
class TagsList(template.Node):
    def __init__(self, limit = 15):
        self.limit = limit
    def render(self, context):
        from board.views.tag import list as tag_list
        return tag_list(context['request'], limit = self.limit, context_instance=context, discard_response = True) 
parsingTag(TagsList, "do_tags_list")


class ProfilesNode(template.Node):
    def __init__(self, lst, varname = ''):
        self.lst = template.Variable(lst)
        self.varname = varname
    def render(self, context):
        posts = self.lst.resolve(context)
        userids = list(set([i.user_id for i in posts]))
        userprofiles = UserProfile.objects.filter(user__in = userids).values()
        for p in posts:
            try:
                p.userprofile = filter(lambda x: p.user_id == x.get('user_id'), userprofiles)[0]
            except IndexError:
                p.userprofile = {}
        context[self.lst] = posts
        if self.varname:
            context[self.varname] = userprofiles 
        return ''

class PostInteractionsNode(template.Node):
    def __init__(self, lst, with_parents = True, varname = ''):
        self.lst = template.Variable(lst)
        self.varname = varname
    def render(self, context):
        posts = self.lst.resolve(context)
        user = context["request"].user
        if not user.is_authenticated():
            return ''
        object_pks = [x.pk for x in posts]
        interactions = Interaction.objects.filter(object_id__in = object_pks, 
                                                  user = user).values('value', 
                                                                      'object_id', 
                                                                      'interaction_type__name', 
                                                                      'interaction_type__content_type_id')
        pdict = dict((d.pk, d) for d in posts)
        for i in interactions:
            p_id = i["object_id"]
            if i["interaction_type__content_type_id"] == ContentType.objects.get_for_model(pdict[p_id])._get_pk_val():
                # print >> sys.stderr, i["interaction_type__name"], i["value"]
                try:
                    i_val, i_count = i["value"].split(';')
                except ValueError:
                    i_val, i_count = [i["value"], '']
                if i_val.isdigit():
                    setattr(pdict[p_id], "%s_last" % i["interaction_type__name"], int(i_val))
                else: #Trying to cater to the "post count" crowd - shouldn't harm anything else. Hopefully.
                    setattr(pdict[p_id], "%s_last" % i["interaction_type__name"], i_val)
                
                if i_count.isdigit():
                    setattr(pdict[p_id], "%s_last_count" % i["interaction_type__name"], int(i_count))
                elif i_count: #Trying to cater to the "post count" crowd - shouldn't harm anything else. Hopefully.
                    setattr(pdict[p_id], "%s_last_count" % i["interaction_type__name"], i_count)
                
                #The next line has been removed to allow the *_count attrs
                #setattr(pdict[p_id], "%s_last" % i["interaction_type__name"], int(i["value"]) if i["value"].isdigit() else i['value'])
        #Adding this bit to check for rateability
        for p in posts:
            setattr(p, 'can_be_rated', p._can_be_rated(context["request"]))
            setattr(p, 'can_be_edited', p._can_be_edited(context["request"]))
            
        context[self.lst] = posts
        if self.varname:
            context[self.varname] = interactions 
        return ''

class TagsNode(template.Node):
    def __init__(self, lst, varname = ''):
        self.lst = template.Variable(lst)
        self.varname = varname
    def render(self, context):
        posts = self.lst.resolve(context)
        tags = Tag.objects.filter(tagattach__post__pk__in = [x.pk for x in posts]).extra(select = {"post_id":"post_id"}).values("post_id", "title")
        pdict = dict((d.pk, d) for d in posts)
        for i in tags:
            p_id = i["post_id"]
            setattr(pdict[p_id], "tag_set", getattr(pdict[p_id], 'tag_set', []) + [i["title"]])
        context[self.lst] = posts
        if self.varname:
            context[self.varname] = tags 
        return ''
    

@register.tag
def prefetch(parser, token):
    """
    Usage: prefetch [arg] for [objects_list] <as [var name]>
    """
    args = token.split_contents()
    if len(args) < 4:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % args[0]
    node = "%sNode" % ''.join([x.capitalize() for x in args[1].split('_')])
    try:
        if len(args) == 6:
            return globals().get(node)(args[3], args[5]) #TODO: Check if this can be improved upon
        else:
            return globals().get(node)(args[3]) #TODO: Check if this can be improved upon
    except TypeError:
        raise template.TemplateSyntaxError, "Missing node for %s tag: %s" % (args[0], node)


@register.inclusion_tag("board/tags_on_object.html", takes_context = True)
def object_tags(context, obj):
    '''
    @param context:
    @param obj:
    '''
    return {"tags":getattr(obj, "tag_set", []), 
            'obj':obj,
            'request':context['request']
            }
    


@register.inclusion_tag("board/user_link.html")
def user_link(obj):
    '''
    
    '''
    
    if obj.user_id is not None:
        if obj.user_id <> 0:
            return {"user":{"id":obj.user_id,
                            "username":obj.username,
                            "profile":getattr(obj, 'userprofile', {})}}
        else:
            return {"user":{"username":obj.username}}
    else:
        return {}

@csrf_protect
@register.inclusion_tag("registration/login.html", takes_context = True)
def login_form(context):
    '''
    
    '''
    from django.contrib.auth.forms import AuthenticationForm
    return {
            'form':AuthenticationForm(context["request"]),
            'request': context['request'],
            }


@csrf_protect
@register.inclusion_tag("board/post_form.html", takes_context = True)
def post_form(context, obj = None):
    '''
    
    '''
    request = context['request']
    return {'form':board_forms.PostDataForm(obj, request = request), 
            'hide_auth': request.user.is_authenticated() and request.GET.get('auth') != 'show',
            'request': request,
            'next_item': context['next_item'],
            'csrf_token': context['csrf_token'],
            'tag': context.get('tag',False),
            }


@register.inclusion_tag("board/post_info.html", takes_context = True)
def post_info(context, post):
    '''
    
    '''
    return {'post':post,
            'request':context['request'],
            'personal_settings':context['personal_settings'],
            }

@register.inclusion_tag('board/mention_list.html', takes_context = True)
def list_mentions_for(context, user):
    # TODO: remove hardcoded limit
    # TODO: Check if ordering by mention_id makes any sense 
    mentions = user.mentions.public(user).order_by('-mention__id')[:10]
    return {'mentions':mentions, 'request':context['request']}


class RepliesToken(template.Node):
    """
    """
    def __init__(self, obj, list_name='object_list'):
        self.obj = template.Variable(obj)
        
    def render(self, context):
        try:
            obj = self.obj.resolve(context)
        except template.VariableDoesNotExist:
            return "Object %s does not exist" % self.obj
        
        ct = ContentType.objects.get_for_model(obj).name
        if ct == 'post':
            from board.views.post import list_replies as post_replies
            return post_replies(context["request"], obj.pk, context, discard_response = True)
        if ct == 'user profile':
            from board.views.userprofile import list_replies as profile_comments
            profile_comments(context["request"], obj.user.username, context, discard_response = True)
            return ''
        return ''
parsingTag(RepliesToken, "get_replies", required = 1)


#@parsingTag("get_posts_by", required=1)
class UserPostsToken(template.Node):
    def __init__(self, user_object, var_name = "object_list"):
        self.user_object = template.Variable(user_object)
        self.var_name = var_name
    
    def render(self, context):
        try:
            obj = self.user_object.resolve(context)
        except template.VariableDoesNotExist:
            return "Object %s does not exist" % self.user_object
        from board.views.userprofile import list_by_user
        list_by_user(context['request'], obj.user.username, context, discard_response = True)
        return ''
parsingTag(UserPostsToken, "get_posts_by", required = 1)

#============================================================================
# Simple Tags
#============================================================================
@register.simple_tag
def class_tags(obj, prefix = "tag-"):
    '''
    Returns the object's tag_set (only available after prefetching!) in a format suitable for 
    being included in a CSS class declaration."
    '''
    return " ".join(["%s%s" % (prefix, x) for x in getattr(obj, "tag_set", [])])


@register.simple_tag
def list_online_users(timespan = 5):
    '''
    Returns the currently online (activity within the last timespan minutes) users and the page they're watching
    '''
    t = datetime.datetime.now() - datetime.timedelta(minutes = int(timespan))
    u = UserProfile.objects.filter(last_page_time__gte = t, hidden_status__exact = False)
    return ", ".join(['<a href="%s" class="user-link user-online">%s</a>' % (reverse('profiles_profile_detail', kwargs = {'username':p.user.username}), p.user.username) for p in u])

#=============================================================================
# Filters
#=============================================================================

@register.filter
def from_reverse_timestamp(ts):
    try:
        res = datetime.datetime.fromtimestamp(0xFFFFFFFF - ts)
    except:
        res = datetime.datetime.fromtimestamp(1) 
    return res

@register.filter
def font_by_rating(r):
    if r > 4: #TODO: Remove hardcode
        return "%s high-rating" % r
    elif r <= 0:
        return "%s low-rating" % r
    else:
        return r


@register.filter
def jsonify(object):
    return simplejson.dumps(object)

@register.filter
def escapecss(st):
    return st.replace('}', '&#7d;')


@register.filter
def updateurl(url, arg): #We might make this more robust later but it's ok for now
    j = '?' if url.find('?') == -1 else '&'
    return url + j + arg

@register.filter
def is_direct(title, user):
    return title.lower().startswith('@[%s]' % user.username.lower())

@register.filter
def clean_mention(title, user):
    return title.replace('@[%s]' % user.username.lower(), '')

@register.filter
def replies_for_path(path):
    '''
    Add /replies to path if required. Not really useful, anyway.
    '''
    path = path.split('?')
    if not path[0].endswith('replies'):
        path[0] += '/replies'
    return '?'.join(path)

@register.filter
def sensibletime(value, arg = None):
    """
    If it's today, show the time, otherwise show the date. Might be improved later on.
    """
    try: 
        p_value = datetime.date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    except ValueError:
        # Date arguments out of range
        return value
    
    delta = p_value - datetime.date.today()
    if delta.days == 0:
        return value.strftime('%H:%M:%S') #TODO: Remove hardcoding
    return humanize.naturalday(value, arg)
