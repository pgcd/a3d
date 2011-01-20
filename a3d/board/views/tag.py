'''
Created on 31/mar/2010

@author: pgcd
'''
# Create your views here.
from django.views.generic.list_detail import object_list
#from django.core import serializers
from board.models import Tag, TagAttach, Post
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.template.defaultfilters import slugify
from django.db.utils import IntegrityError



def list(request,
                 template_name = 'board/tag_list.html', **kwargs):
    """
    **Template:**
    
    ``template_name`` keyword argument or
    :template:`board/post_list.html`.
    
    """
    queryset = Tag.objects.filter(is_active = True).select_related(depth = 1)
    kwargs['queryset'] = queryset
    return object_list(request, template_name = template_name, **kwargs)

def list_on_post(request, post_id, template_name = 'board/tags_on_object.html', **kwargs):
    tags = Tag.objects.filter(tagattach__post__exact = post_id)
    context_instance = RequestContext(request)
    return render_to_response(template_name,
            {
             'tags':tags,
             'obj':{'pk':post_id},
             },
            context_instance = context_instance)
    

def view(request, tag_id = None, tag_title = None, page = 1, limit = 30,
                 template_name = 'board/tag_view.html', **kwargs):
    """
    **Template:**
    
    ``template_name`` keyword argument or
    :template:`board/post_list.html`.
    
    """


def autocomplete(request, **kwargs): #TODO: Enforce minimum chars here?
    """
    """
    tag_title = request.GET.get('s', '')
    object_list = Tag.objects.filter(is_active = True, title__startswith = tag_title).values_list('title')
    
#    json_serializer = serializers.get_serializer("json")()
#    json_serializer.serialize(queryset, ensure_ascii=False, stream=response,fields='title')
    return HttpResponse(object_list, mimetype = "text/plain")


@csrf_protect
@require_POST
def attach(request, **kwargs):
    """
    Attach a tag to a post
    """
    #TODO: REQUIRE AUTH/PERMISSIONS
    post_id = request.POST.get('post_id', 0)
    title = slugify(request.POST.get('tag_title', ''))
    if title <> '' and post_id > 0:
        tag, _ = Tag.objects.get_or_create(title = title)
        post = Post.objects.get(pk = post_id)
        rel = TagAttach(tag = tag, post = post, reverse_timestamp = post.reverse_timestamp)
        try:
            rel.save()
        except IntegrityError:
            pass
    return list_on_post(request, post_id)

@csrf_protect
def detach(request, **kwargs):
    """
    Remove a tag from a post
    """

    #TODO: REQUIRE AUTH/PERMISSIONS
    post_id = request.POST.get('post_id', 0)
    title = request.POST.get('tag_title', '')
    if title <> '' and post_id > 0:
        rel = get_object_or_404(TagAttach, tag__title = title, post = post_id)
        rel.delete()
    return list_on_post(request, post_id)

