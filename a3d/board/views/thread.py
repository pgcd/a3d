'''
Created on 31/mar/2010

@author: pgcd
'''

# Create your views here.
from django.views.generic.list_detail import object_list
#from django.shortcuts import get_object_or_404, render_to_response
#from django.template import RequestContext
from board.models import Thread


def list(request, tag_id = None, 
                 template_name='board/thread_list.html', **kwargs):
    queryset = Thread.objects.filter(is_active = True).select_related(depth=1)
    
    if tag_id is not None:
        queryset = queryset.filter(tags__in=[tag_id])
    
    kwargs['queryset'] = queryset
    return object_list(request, template_name=template_name, **kwargs)
