'''
Created on 31/mar/2010

@author: pgcd
'''
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, \
    HttpResponseNotModified, HttpResponseServerError, HttpResponseForbidden
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required

from board.models import UserProfile, Post, Tag, PostData, InteractionType
from board.utils import EndlessPage, tripcode
from board.forms import PostDataForm, PostDataEditForm
from board import signals as board_signals
from django.utils import simplejson
from django.db.models.signals import pre_save
import re
from faves.templatetags.faves import has_faved
from django.contrib.contenttypes.models import ContentType
from a3d import settings
import sys
from django.template.loader import render_to_string
import datetime


#I think the following should be moved to the interaction views, but right now it doesn't make a lot of sense to do so

@login_required     #Shouldn't actually be required, but you never know
def mark_as(request, post_id, action, **kwargs):  #IGNORE:W0613
    '''
    @var request: The current request
    @var post_id: The id of the Post (not PostData) object to act upon
    @var action: 'read' or 'unread'  
    '''
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
    except DoesNotExist: #@UndefinedVariable #IGNORE:E0602
        return HttpResponseServerError()


def list_by_tag_title(request, tag_title, **kwargs):
    '''
    @var request: The current HttpRequest
    @var tag_title: A string with the tag to search for.  
    '''
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
    '''
    @var request: The current HttpRequest
    
    This function returns only the posts that have no tag applied.
    '''
    return _list(request, Post.objects.get_by_tag(0), **kwargs)

def search(request, search_term, **kwargs):
    '''
    @var request: The current HttpRequest
    @var search_term: String with the term to find. Currently matching only hashtags.
    '''
    return _list(request, Post.objects.ft_search('#' + search_term), **kwargs)

def home(request, **kwargs):
    """
    @var request: The current HttpRequest
    List "home" posts - that is, Posts returned by Post.objects.get_home_posts() 
    with the current min_rating_for_home setting. 
    """
    context = RequestContext(request)
    return _list(request,
                 Post.objects.get_home_posts(context['personal_settings']['min_rating_for_home']),
                 context_instance = context, **kwargs)
    

def _list(request, queryset, limit = None, template_name = 'board/thread_list.html', context_instance = None,
          extra_context = None, template_body = None, **kwargs): #IGNORE:W0613
    """
    @var request: The current HttpRequest
    @var queryset: The queryset to list.

    Utility function to list "threads" previously selected in a queryset. Please note that:
    1) what constitutes a thread is defined by the caller function; and
    2) the template_body var mechanism is currently not implemented.
    """
    extra_context = extra_context or {}
    context_instance = context_instance or RequestContext(request, extra_context)
    tag = kwargs.get("tag")
    limit = limit or context_instance['personal_settings']['post_per_page']
    if request.GET.get('count', None) is not None:
        c = EndlessPage(queryset, limit,
                        filter_field = 'timestamp').get_stats(request)
        if c['items_left'] == 0:
            return HttpResponseNotModified()
        else:
            _d = {'object_list':[],
                  'tag':tag,
                  'next_item': c.get('tip', 0),
                  'items_left': c['items_left']}
            return render_to_response(template_name,
                _d,
                context_instance = context_instance)
    if request.GET.get('info_only', False): 
        #We use this for the brief - might require some tweaking later on
        _d = EndlessPage(queryset, 10, #TODO: Remove hardcoding
                         filter_field = 'timestamp').page(request, list_name = 'post_list')
        return render_to_response('board/post_list_brief.html', #TODO: Remove hardcoding
                _d,
                context_instance = context_instance)

    #The actual processing takes place here.
    _d = EndlessPage(queryset.select_related('user', 'postdata'),
                     limit,
                     filter_field = 'timestamp').page(request)
    
    _d.update({'next_item':_d['first_item'],
               'tag':tag,
               })
    if tag:
        board_signals.tag_read.send(Tag, tag_id = tag.pk, last_item = _d["last_item"], user = request.user)
    else:
        board_signals.home_read.send(Post, last_item = _d["last_item"], user = request.user)
    return render_to_response(template_name,
            _d,
            context_instance = context_instance)

def _set_extra_attributes(request, post_obj):
    '''
    @var request:
    @var post_obj:   
    Helper function to set a few computed attributes on Post objects.
    '''
    #TODO: Check if there's a better way to do this
    #TODO: Move this to a different module
    setattr(post_obj, 'tag_set', post_obj.tags.all())
    setattr(post_obj, 'can_be_rated', post_obj._can_be_rated(request))
    setattr(post_obj, 'is_starred', has_faved(request.user, post_obj) if request.user.is_authenticated() else False)
    if post_obj.user_id > 0:
        post_obj.userprofile = UserProfile.objects.get(user = post_obj.user_id)
    return post_obj

def view(request, post_id, template_name = 'board/post_view.html',
                info_only = False, extra_context = None):
    """
    View a single post - also used as a response for editing and creating new posts.
    """
    if info_only:
        template_name = 'board/post_info.html'
    if request.GET.get('is_reply'):
        template_name = 'board/post_body.html'
    user = request.user
    post_obj = get_object_or_404(Post.objects.public(user).select_related('postdata'), pk = post_id).with_interactions(request)

    post_obj = _set_extra_attributes(request, post_obj)    
    setattr(post_obj, 'is_main_post', not info_only) #TODO: a more elaborate logic to ascertain if it actually is the main post or not
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request, extra_context)
    #The following deals with future enhancements
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'post': post_obj,
                                'extend': post_obj.extended_attributes
                              },
                              context_instance = context)


def list_replies(request,
                 post_id,
                 context_instance = None,
                 template_name = 'board/post_list.html',
                 discard_response = False):
    """
    @var discard_response: Pass this if you only want to update the context, without output to HttpResponse
    This view is used for replies to posts only; comments to user profiles are dealt with in views.user.list_replies.
    """
    user = request.user
    context_instance = context_instance if context_instance else RequestContext(request)
    limit = context_instance['personal_settings']['post_per_page']
    post = get_object_or_404(Post, pk = post_id)
    #Only public and user-specific replies
    qs = post.replies.public(user).tag_match(request)
    paginator = EndlessPage(qs, limit)
    if request.GET.get('count', None) is not None:
        #this is only a count request - result should only be a number
        c = paginator.get_stats(request)
        if c['items_left'] == 0:
            return HttpResponseNotModified()
        else: #Since there are new posts, we return them, formatted with the current template
            return render_to_response(template_name,
                {'post_list':[],
                  'next_item': c.get('tip', 0),
                  'parent_post':post,
                  'items_left': c['items_left'],
                 },
                context_instance = context_instance)
    
    #retrieve the actual list     
    _d = paginator.page(request, list_name = 'post_list')
    _d.update({
            'next_item':_d.get('tip', 0),
            'parent_post':post,
           })
    
    #Check if we only want the list of the last posts, without the actual data.
    #TODO: Check if it's possibile to remove select_related - perhaps we can make the check in the caller funcs?
    if request.GET.get('info_only', False):
        return render_to_response('board/post_list_brief.html',
                _d,
                context_instance = context_instance)
        
    last_item = "%s;%s" % (_d['last_item'] or post_id,
                           post.replies_count - _d['items_left'])
    board_signals.post_read.send(sender = Post,
                                 obj_id = post_id,
                                 last_item = last_item,
                                 user = request.user)
    
    #deal with mentions in replies 
    #(and possibly other situations as well, since it actually makes sense).
    try:
        starting_reply = abs(int(request.GET.get('start', '')))
        board_signals.post_read.send(sender = Post,
                                     obj_id = starting_reply,
                                     last_item = "%s;0" % starting_reply,
                                     user = request.user)
    except ValueError:
        pass
    #discard_response is used when calling the view from a template_tag
    if discard_response:
        #Next_item needs to be set here
        context_instance.update({'next_item':_d['next_item']})
        return render_to_string(template_name,
                _d,
                context_instance = context_instance)
    else:
        return render_to_response(template_name,
                _d,
                context_instance = context_instance)
    


@login_required(redirect_field_name = 'next_page')
@require_GET
def rate(request, post_id, action):
    '''
    This function has two effects: the actual rating if the user has the required permissions,
    and the timeshift for all other users.
    
    '''
    #first we require some kind of check
    next_page = request.GET.get('next_page')
    post = get_object_or_404(Post.objects.select_related(), pk = post_id).with_interactions(request)
   
    if post._can_be_rated(request) and request.user.has_perm('board.timeshift_post'):
        signal_action = 'timeshift'
        setattr(post, 'can_be_rated', True)
        if request.user.has_perm('board.rate_post'):
            signal_action = 'rate'
            post.rating = post.rating + {'down':-1, 'up':+1}[action]
        timeshift = {'down':-1000, 'up':1000}[action] #TODO: Figure out some realistic value/algorithm
        parent_timeshift = timeshift / max(5, post.replies_count / 5) #TODO: As above
        if post.object_id: #This post has a parent, so any timeshift should be applied to the parent as well. 
            parent = post.in_reply_to
            parent.timestamp = parent.timestamp + parent_timeshift
            parent.timeshift = parent.timeshift + parent_timeshift 
            if board_signals.interaction_event.send(Post,
                                                    request = request,
                                                    user = request.user,
                                                    object_id = parent.pk,
                                                    value = action,
                                                    interaction_type = 'timeshift'):
                parent.save(no_update = True) 
        post.timestamp = post.timestamp + timeshift
        post.timeshift = post.timeshift + timeshift 
        if board_signals.interaction_event.send(Post,
                                                request = request,
                                                user = request.user,
                                                object_id = post.pk,
                                                value = action,
                                                interaction_type = signal_action):
            post.save(no_update = True)
        
        setattr(post, 'tag_set', post.tags.all())
        if request.is_ajax():
            return view(request, post_id, info_only = True) #This calls this modules' view() function
        else:
            return HttpResponseRedirect(next_page) #TODO: Remove hardcode
    else: #No auth
        return HttpResponseForbidden()


@csrf_protect
@require_POST
def preview(request):
    '''
    A simple preview for Posts.
    '''
    #TODO: Save the preview as draft somewhere
    from almparse.parser import transform
    b = request.POST.get('data')
    p = PostData(body = transform(b))
    pre_save.send(sender = PostData, request = request, instance = p)
    context_instance = RequestContext(request)
    return render_to_response('board/post_preview.html',
                              {'post':p},
                              context_instance = context_instance)


@csrf_protect
def edit(request, post_id):
    '''
    If the request method is GET, we return the edit form; if it's POST we do the actual editing of the item.
    '''
    if request.method == 'GET':
        data = get_object_or_404(PostData, pk = post_id)
        initial = {'title':data._title,
                   'body_markup':data.body_markup,
                   'content_type':data.content_type,
                   'object_id':data.object_id,
                   }
        form = PostDataEditForm(initial = initial, prefix = "edit")
        return render_to_response('board/post_edit_form.html', {'form':form,
                                                                'post_id':post_id,
                                                                'is_reply':request.GET.get('is_reply', False),
                                                                }, RequestContext(request))
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
            p = _set_extra_attributes(request, p) #FIXME: can_be_edited doesn't seem to get passed 
            template_name = 'board/post_body.html' if request.REQUEST.get('is_reply') else 'board/post_view.html'
            return render_to_response(template_name,
                                      {'post':p.post_ptr, #Note: this is so that the template can retrieve all the replies; might be changed later. 
                                       'extend': p.extended_attributes},
                                      context_instance = context_instance)
        else: #TODO: Return a meaningful response.
            return HttpResponseNotModified()

@csrf_protect
@require_POST
def create(request):
    """
    Create a new post.
    """
    #TODO: Some serious validation is required here!
    next_page = request.POST.get('next_page', '')
    #We should never have "is_reply=false" in the req
    is_reply = request.POST.get('content_type', False) and request.POST.get('object_id', False)  
    form = PostDataForm(data = request.POST)
    context_instance = RequestContext(request)
    if form.is_valid():
        p = form.save(commit = False) #Here we have the basic data
        p.ip = request.META.get('REMOTE_ADDR')
        p._title = form.cleaned_data["title"]
        p.rating = settings.A3D_BASE_SETTINGS['base_rating'] #The default - might want to provide for different cases? Perhaps Group-based
        #Fully auth'ed post, with user_id
        if form.cleaned_data['username']:
            p.username = form.cleaned_data['username']
            if (request.user.is_authenticated() and request.user.username.lower() == form.cleaned_data['username'].lower()):
                p.user_id = request.user.id
            else:
                p.user_id = 0
        #Username with no password
        elif request.user.is_authenticated() and not form.cleaned_data['password']:
            p.username = request.user.username
            p.user_id = request.user.id
        #Fully anonymous with tripcode 
        else: 
            p.username = tripcode(form.cleaned_data['password'])
            p.user_id = -1 


        if p.user_id > 0 and len(p.body_markup) > 0:
            p.signature = getattr(request.user.get_profile(), "signature", '')
            #The base_rating applies ONLY to logged-in users who actually use their name, overriding the previously set default
            if not is_reply:
                p.rating = context_instance['personal_settings']["base_rating"]

        #Retrieve the user's previous post
        try:
            control = PostData.objects.filter(username = p.username).order_by('-pk')[0] #@UndefinedVariable
        except IndexError:
            control = None

        # same username
        if control is None or control._title != p._title or control.body_markup != p.body_markup:
            #Since we are here, the previous post is different enough to believe it's intentional
            #checking tags in title
            all_tags = re.findall(r'(?:^|\])\[(.*?[^ ])(?=\])', p._title)
            if request.POST.get('list_tag'):
                all_tags.append(request.POST.get('list_tag'))
            #cleanup title
            existing_tags = Tag.objects.filter(title__in = list(set(all_tags))) 
            p._title = re.sub('|'.join(['\[%s\]' % t.title for t in existing_tags]), '', p._title)
            board_signals.postdata_pre_create.send(sender = p.__class__,
                                              request = request, instance = p)
            #The post should be mostly ready, so we can save it.
            p.save()

            for newtag in existing_tags: #Create the required TagAttach records
                try:
                    #TODO: Find a way to deal with multiples, if that is desirable
                    p.tags.through(tag = newtag, post = p).save()
                except Tag.DoesNotExist: #@UndefinedVariable #IGNORE:E1101
                    #TODO: Do we want to create it automatically if it doesn't exist?
                    pass
            board_signals.postdata_created.send(sender = p.__class__, request = request, instance = p)
        else:
            p = control #There is a previous, identical post - we're simply returning it. 
                        #TODO: Perhaps a different response would be better?
            
        if request.is_ajax():
            #===================================================================
            # We need to be able to return: 
            # - post_view if it's a new topic
            # - post_body if it's a reply 
            #===================================================================
            expected_view, args, kwargs = urlresolvers.resolve(next_page)
            new_req = HttpRequest()
            new_req.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
            new_req.user = request.user
            new_req.GET = request.GET.copy()
            new_req.GET.update({'start': request.POST.get('next_item', ''),
                                'is_reply':is_reply,
            #The following prevents both endlesspaginators from being rendered
                                'discard_low': True,
                                'discard_high': True,
                                })
            return expected_view(new_req, *args, **kwargs) #IGNORE:W0142
        else:
            return HttpResponseRedirect(next_page)
    else: #Something's wrong with the submitted form, let's display the errors.
        if request.is_ajax():
            errors = dict((k, v[0].__unicode__()) for k, v in form.errors.items())
            return HttpResponse(simplejson.dumps(errors),
                                mimetype = 'application/json')
        else:
            #TODO: Some feedback for non-ajax enabled users?
            return HttpResponseRedirect(next_page)
