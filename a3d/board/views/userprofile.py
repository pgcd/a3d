'''
Created on 13/lug/2010

@author: pgcd
'''
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from a3d.board.models.base import ExtendedAttribute
from django.views.decorators.http import require_GET
from django.contrib.contenttypes.models import ContentType
from a3d.board.models import UserProfile

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
