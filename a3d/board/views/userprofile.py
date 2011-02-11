#encoding utf-8
'''
Created on 13/lug/2010

@author: pgcd
'''
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseNotModified
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from board.models.base import ExtendedAttribute
from django.views.decorators.http import require_GET
from django.contrib.contenttypes.models import ContentType
from board.models import UserProfile
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from board.utils import EndlessPage
from board import signals as board_signals
import urllib2

def autocomplete(request, **kwargs): #TODO: Enforce minimum chars here?
    """
    """
    username = request.GET.get('s', '')
    object_list = User.objects.filter(username__startswith = username).values_list('username')
    
#    json_serializer = serializers.get_serializer("json")()
#    json_serializer.serialize(queryset, ensure_ascii=False, stream=response,fields='title')
    return HttpResponse(object_list, mimetype = "text/plain")

@require_GET
@login_required
def mark_all_read(request, post_id, **kwargs):
    """
    Mark all posts before starting_post as read (that is, set the "all_read_before" extended_attribute to post_id);
    
    """
    p = request.user.get_profile()
    lastread, _ = p._extended_attributes.get_or_create(key = ExtendedAttribute.objects.get(name = 'all_read_before'),
                                                       content_type = ContentType.objects.get_for_model(UserProfile),
                                                       object_id = p.pk)
    lastread.value = post_id
    lastread.save()
    return HttpResponseRedirect(request.GET.get('next', '/'))



def list_replies(request,
                 username,
                 context_instance = None,
                 template_name = 'board/post_list.html',
                 data_only = False,
                 discard_response = False):
    """
    This view is used for replies to profiles only; We really should merge it with views.post.list_replies, though.
    """
    user = request.user
    context_instance = context_instance if context_instance else RequestContext(request)
    limit = context_instance['personal_settings']['post_per_page']
    post = get_object_or_404(User, username = urllib2.unquote(username)).get_profile()
    qs = post.replies.public(user).tag_match(context_instance["request"]) #Only public and user-specific replies
    lastcount = request.GET.get('count', False)
    if lastcount:
        #this is only a count request - result should only be a number
        c = EndlessPage(qs, 30).page(context_instance, count_only = True)
        if c == 0 or c == int(lastcount):
            return HttpResponseNotModified()
        else:
            _d = {'post_list':[],
                  'more_up':'%s' % (request.GET.get('start', '').lstrip('-')),
                  'next_item_direction':'up',
                  'parent_post':post, 'items_left': c}
            return render_to_response(template_name,
                _d,
                context_instance = context_instance)
    
    
    _d = EndlessPage(qs, limit).page(context_instance, list_name = 'post_list')
    _d.update({
            'next_item':_d['last_item'] + 1,
            'next_item_direction':'down',
            'parent_post':post,
           })
    context_instance.update(_d)
    
    if request.GET.get('info_only', False):
        return render_to_response('board/post_list_brief.html',
                {},
                context_instance = context_instance)
    last_item = "%s;%s" % (_d['last_item'] or post.pk, post.replies_count - _d['items_left'])
    board_signals.post_read.send(sender = UserProfile, obj_id = post.pk, last_item = last_item, user = request.user)
    if not discard_response:
        return render_to_response(template_name,
                _d,
                context_instance = context_instance)
