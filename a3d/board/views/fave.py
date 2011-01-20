'''
Created on 21/giu/2010

@author: pgcd
'''

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
import sys
from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType
from board.models.PostData import Post
from board.models.Tag import Tag
from django.contrib.auth.models import User
from faves.models import Fave, FaveType



def fave_list(request):
    context = RequestContext(request) 
    if not request.user.is_authenticated():
        return render_to_response('board/fave_list.html', {}, context)
    else:
        return render_to_response('board/fave_list.html', {'faves':request.user.get_profile().favorites}, context)

    
@require_POST
def add_star(request):
    link_href = request.POST.get('link_href') 
    if not link_href:
        return render_to_response('base_ajax.html') #TODO: Return some kind of useful info, maybe?
    context = RequestContext(request)
    view, args, kwargs = resolve(link_href) #@UnusedVariable
    if kwargs.has_key('post_id'):
        faved_object = Post.objects.get(pk = kwargs['post_id'])
    elif kwargs.has_key('tag_title'):
        faved_object = Tag.objects.get(title = kwargs['tag_title'])
    elif kwargs.has_key('username'):
        faved_object = User.objects.get(username = kwargs['username'])
    else:
        return render_to_response('base_ajax.html') #TODO: Return some kind of useful info, maybe?

    fave_type = FaveType.objects.get(slug = 'star')
    Fave.objects.create_or_update(request.user, faved_object, fave_type, force_not_withdrawn = True)
    return render_to_response('board/fave_list.html', {'faves':request.user.get_profile().favorites}, context)
