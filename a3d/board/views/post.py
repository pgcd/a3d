'''
Created on 31/mar/2010

@author: pgcd
'''


# Create your views here.
#from board.views.list_detail import object_list
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, \
    HttpResponseNotModified, HttpResponseServerError
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required, user_passes_test

from board.models import UserProfile, Post, Tag, PostData, InteractionType
from board.utils import EndlessPage, tripcode
from board.forms import PostDataForm, PostDataEditForm
from board import signals as board_signals
from django.utils import simplejson
import sys
from django.db.models.signals import pre_save
import re
from django.contrib.auth.models import User
from faves.templatetags.faves import has_faved
from django.contrib.contenttypes.models import ContentType


#from django.contrib.contenttypes.models import ContentType
#from endless_pagination.decorators import page_template
#from django.template import loader
#from django.http import Http404, HttpResponse

#from datetime import datetime, time

#I think the following should be moved to the interaction views, but right now it doesn't make a lot of sense to do so

@login_required     #Shouldn't actually be required, but you never know
def mark_as(request, post_id, action, **kwargs):
    try:
        p = Post.objects.get(pk = post_id)
        it = InteractionType.objects.get_type_for_model('read', ContentType.objects.get_for_model(Post))
        i = request.user.interactions.get_or_create(interaction_type = it, object_id = p.id)
        if action == 'read':
            i[0].value = "%s;%s" % (p.last_reply, p.replies_count)
            i[0].save()
        elif action == 'unread':
            request.user.interactions.filter(pk = i[0].pk).delete()
        
        #if request.is_ajax(): #TODO: Some kind of response+template for non-ajax requests
        return view(request, post_id, info_only = True) #FIXME:I really don't like using "board.views.post.view" like this, I'd rather use a more specific addressing
    except Post.DoesNotExist, InteractionType.DoesNotExist:
        return HttpResponseServerError()



def list_by_tag_title(request, tag_title = None, **kwargs):
    try:
        tag = Tag.objects.select_related('template__body').get(title__iexact = tag_title)
    except Tag.DoesNotExist: #@UndefinedVariable
        #TODO: This view should return something different, I believe.
        return search(request, tag_title)
    try:
        template_body = tag.template.body
    except AttributeError:
        template_body = None
    extra_context = {'basetag': tag}
    return _list(request, Post.objects.get_by_tag(tag.id), template_body = template_body, extra_context = extra_context, tag = tag, **kwargs)

def list_tagless(request, **kwargs):
    return _list(request, Post.objects.get_by_tag(0), **kwargs)

def search(request, search_term, **kwargs):
    return _list(request, Post.objects.ft_search('#' + search_term), **kwargs)

def home(request, **kwargs):
    """
    List home posts
    
    """
    context = RequestContext(request)
    return _list(request, Post.objects.get_home_posts(context['personal_settings']['min_rating_for_home']), context_instance = context, **kwargs)
    

def _list(request, queryset, limit = None, template_name = 'board/thread_list.html', context_instance = None,
          extra_context = {}, template_body = None, **kwargs):
    """
    It actually makes sense for this to use a "thread" list - posts are those that always have a body,
    while those that only have a summary are threads.
    """
    context_instance = context_instance if context_instance else RequestContext(request, extra_context)
    tag = kwargs.get("tag")
    
    if request.GET.get('count', False):
        #this is only a count request - result should only be a number
        c = EndlessPage(queryset, 30, filter_field = 'reverse_timestamp').page(context_instance, count_only = True)
        if c == 0:
            return HttpResponseNotModified()
        else:
            _d = {'object_list':[], 'more_down':'%s' % (request.GET.get('start', '').lstrip('-')), 'next_item_direction':'up', 'tag':tag, 'how_many_more': c}
            return render_to_response(template_name,
                _d,
                context_instance = context_instance)

    
    if limit is None:
        paginate_by = context_instance['personal_settings']['post_per_page']
    else:
        paginate_by = limit or 30 # I need to enforce the hard limit for list_tagless, perhaps there's a better way.

    _d = EndlessPage(queryset.select_related('user', 'postdata'), paginate_by, filter_field = 'reverse_timestamp').page(context_instance)
    _d.update({'next_item':'-%s' % ((_d['first_item'] or 0xFFFFFFFF) - 1), 'next_item_direction':'up', 'tag':tag})

    if tag:
        board_signals.tag_read.send(Tag, tag_id = tag.pk, last_item = _d["last_item"], user = request.user)
    else:
        board_signals.home_read.send(Post, last_item = _d["last_item"], user = request.user)
    return render_to_response(template_name,
            _d,
            context_instance = context_instance)


def view(request, post_id, template_name = 'board/single_post_view.html',
                info_only = False, extra_context = None):
    """
    ``template_name`` keyword argument or
    :template:`board/single_post_view.html`.
    
    """
    if info_only:
        template_name = 'board/post_info.html'
    user = request.user
    post_obj = get_object_or_404(Post.objects.public(user).select_related('postdata'), pk = post_id).with_interactions(request)
    #TODO: Check if there's a better way to do this
    setattr(post_obj, 'tag_set', post_obj.tags.all())
    setattr(post_obj, 'can_be_rated', post_obj._can_be_rated(request))
    setattr(post_obj, 'is_starred', has_faved(request.user, post_obj) if request.user.is_authenticated() else False)
    setattr(post_obj, 'is_main_post', not info_only) #TODO: a more elaborate logic to ascertain if it actually is the main post or not
    if post_obj.user_id > 0:
        post_obj.userprofile = UserProfile.objects.get(user = post_obj.user_id)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request, extra_context)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'post': post_obj,
                                'extend': post_obj.extended_attributes
                              },
                              context_instance = context)

def list_replies(request, post_id, context_instance = None, template_name = 'board/post_list.html', data_only = False):
    """
    This view is used for replies to posts only; for comments to user profiles we'll do something different.
    """
    user = request.user
    context_instance = context_instance if context_instance else RequestContext(request)
    limit = context_instance['personal_settings']['post_per_page']
    post = get_object_or_404(Post, pk = post_id)
    qs = post.replies.public(user).tag_match(context_instance["request"]) #Only public and user-specific replies
    
    _d = EndlessPage(qs, limit).page(context_instance, list_name = 'post_list')
    _d.update({
            'next_item':_d['last_item'] + 1,
            'next_item_direction':'down',
            'post':post,
           })
    context_instance.update(_d)
    last_item = "%s;%s" % (_d['last_item'] or post_id, post.replies_count - _d['items_left'])
#        last_item = ";".join([str(_d['last_item'] or obj.pk), str(obj.replies_count)])
    board_signals.post_read.send(sender = Post, obj_id = post_id, last_item = last_item, user = request.user)
    return render_to_response(template_name,
            _d,
            context_instance = context_instance)
    

    
    
    
def list_by_user(request, username, **kwargs): #TODO: Ehm.
    user_obj = get_object_or_404(UserProfile, user__username = username)
    context_instance = RequestContext(request, {})
    context_instance.update(EndlessPage(user_obj.posts, context_instance['personal_settings']['post_per_page'], filter_field = 'reverse_timestamp').page(context_instance))
    board_signals.post_read.send(User, obj_id = user_obj.pk, last_item = context_instance["last_item"], user = request.user) #same functionality with different semantics. what to do?
    return render_to_response('board/thread_list.html',
                                    {},
                                   context_instance = context_instance)


@login_required(redirect_field_name = 'next_page')
@user_passes_test(lambda u: u.has_perm('board.timeshift_post') or u.has_perm('board.rate_post'))
@require_GET
def rate(request, post_id, action):
    #first we require some kind of check
    next_page = request.GET.get('next_page')
    context_instance = RequestContext(request, {})
    post = get_object_or_404(Post.objects.select_related(), pk = post_id).with_interactions(request)
   
    if post._can_be_rated(request) and request.user.has_perm('board.timeshift_post'):
        signal_action = 'timeshift'
        setattr(post, 'can_be_rated', True)
        if request.user.has_perm('board.rate_post'):
            signal_action = 'rate'
            post.rating = post.rating + {'down':-1, 'up':+1}[action]
        timeshift = {'down':1000, 'up':-1000}[action] #TODO: Figure out some realistic value/algorithm
        if post.object_id: #This post has a parent, so any timeshift should be applied to the parent as well. 
            parent = post.in_reply_to
            parent.reverse_timestamp = parent.reverse_timestamp + timeshift
            if board_signals.interaction_event.send(Post, request = request, user = request.user, object_id = parent.pk, value = action, interaction_type = 'timeshift'):
                parent.save(no_update = True) 
        post.reverse_timestamp = post.reverse_timestamp + timeshift
        if board_signals.interaction_event.send(Post, request = request, user = request.user, object_id = post.pk, value = action, interaction_type = signal_action):
            post.save(no_update = True)
        
    setattr(post, 'tag_set', post.tags.all())
    if request.is_ajax():
        view, args, kwargs = urlresolvers.resolve(next_page) #@UnusedVariable
        if view.__name__.find('list') > -1:
            template_name = 'board/thread_body.html'
        elif request.GET.get('as_reply') == 'true':
            template_name = 'board/post_body.html'
        else:
            template_name = 'board/single_post_view.html'
        return render_to_response(template_name, {'post':post}, context_instance = context_instance)
    else:
        return HttpResponseRedirect(next_page) #TODO: Remove hardcode



@csrf_protect
@require_POST
def preview(request):
    from almparse.parser import transform
#    f=PostDataForm(data=request.POST)
#    p=f.save(commit=False)
#    board_signals.postdata_pre_create.send(sender=p.__class__, request=request, instance=p)
#    p.postdata.body=transform(p.postdata.body_markup)
    b = request.POST.get('data')
    p = PostData(body = transform(b))
    pre_save.send(sender = PostData, request = request, instance = p)
    context_instance = RequestContext(request, {'post':p})
    return render_to_response('board/post_preview.html', {}, context_instance = context_instance)

@csrf_protect
def edit(request, post_id):
    if request.method == 'GET':
        data = get_object_or_404(PostData, pk = post_id)
        initial = {'title':data._title,
                   'body_markup':data.body_markup,
                   'content_type':data.content_type,
                   'object_id':data.object_id,
                   }
        form = PostDataEditForm(initial = initial, prefix = "edit")
        return render_to_response('board/post_edit_form.html', {'form':form, 'post_id':post_id, }, RequestContext(request))
    else:
        #POST, so we need to save the stuff
        #TODO: Somehow we should require auth and use the password.
        form = PostDataEditForm(data = request.POST, prefix = "edit")
        context_instance = RequestContext(request)
        if form.is_valid(): #TODO: Fix all the denormalized values like tags etc
            p = get_object_or_404(PostData, pk = post_id).with_interactions(request)
            #First we save the current version
            p.versions.create(body_markup = p.body_markup, title = p.title)
            #then we clean the tagset
            p.tagset = ''
            p.body_markup = form.cleaned_data['body_markup']
            p._title = form.cleaned_data['title']
            p.save()
            template_name = 'board/post_body.html' if request.GET.get('is_reply') else 'board/single_post_view.html'
            return render_to_response(template_name, {'post':p}, context_instance = context_instance)
        else:
            p = PostData(body = "DID NOT WORK", title = "DID NOT WORK")


@csrf_protect
@require_POST
def create(request, is_editing = False):
    """
    """
    #TODO: Some serious validation is required here!
    next_page = request.POST.get('next_page', '')
    form = PostDataForm(data = request.POST)
    context_instance = RequestContext(request)
    if form.is_valid():
        p = form.save(commit = False) #Here we have the basic data
        p.ip = request.META.get('REMOTE_ADDR')
        p._title = form.cleaned_data["title"]
        if form.cleaned_data['username']:
            p.username = form.cleaned_data['username']
            if (request.user.is_authenticated() and request.user.username == form.cleaned_data['username']):
                p.user_id = request.user.id
            else:
                p.user_id = 0 
        elif request.user.is_authenticated() and not form.cleaned_data['password']:
            p.username = request.user.username
            p.user_id = request.user.id 
        else: 
            p.username = tripcode(form.cleaned_data['password'])
            p.user_id = -1 

        if p.user_id > 0 and len(p.body_markup) > 0:
            p.signature = getattr(request.user.get_profile(), "signature", '')
            #FIXME: This needs attention - as it is, all posts end up in homepage when base_rating is high enough
            #Disabled until it gets fixed
            #p.rating = context_instance['personal_settings']["base_rating"] 
            p.rating = context_instance['personal_settings']["base_rating"] / 4
        try:
            control = PostData.objects.filter(username = p.username).order_by('-pk')[0] #@UndefinedVariable
        except IndexError:
            control = False

        # same username
        if not control or control._title <> p._title or control.body_markup <> p.body_markup:
            #checking tags in title
            all_tags = re.findall(r'(?:^|\])\[(.*?[^ ])(?=\])', p._title)
            if request.POST.get('list_tag'):
                all_tags.append(request.POST.get('list_tag'))
            #cleanup title
            existing_tags = Tag.objects.filter(title__in = list(set(all_tags)))
            p._title = re.sub('|'.join(['\[%s\]' % t.title for t in existing_tags]), '', p._title)
            board_signals.postdata_pre_create.send(sender = p.__class__, request = request, instance = p)
            # Let's start with the checks
            p.save()
            
            
            for newtag in existing_tags:
                try:
                    #TODO: Find a way to deal with multiples, if that is desirable
                    p.tags.through(tag = newtag, post = p, reverse_timestamp = p.reverse_timestamp).save()
                except Tag.DoesNotExist: #@UndefinedVariable
                    #TODO: Do we want to create it automatically if it doesn't exist?
                    pass
            board_signals.postdata_created.send(sender = p.__class__, request = request, instance = p)
        if request.is_ajax():
            view, args, kwargs = urlresolvers.resolve(next_page)
            new_req = HttpRequest()
            new_req.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
            new_req.user = request.user
            new_req.GET = request.GET.copy()
            new_req.GET.update({'start': request.POST.get('next_item', ''), 'skip_text':True, 'down':True, 'up': True})
#            print "In %s \nCalling view \"%s\" with parameters %s"%(__name__, view.__name__, new_req.GET)
            return view(new_req, *args, **kwargs)
        else:
            return HttpResponseRedirect(next_page) #TODO: Remove hardcode
    else:
        #TODO: Some feedback would be nice
        if request.is_ajax():
            errors = dict((k, v[0].__unicode__()) for k, v in form.errors.items())
            return HttpResponse(simplejson.dumps(errors), mimetype = 'application/json')
        else:
            return HttpResponseRedirect(next_page) #TODO: Remove hardcode
    pass
