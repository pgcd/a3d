'''
Created on 13/lug/2010

@author: pgcd
'''
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseNotModified

def mentions_list(request, limit = 10, offset = 0):
    context_instance = RequestContext(request)
    u = request.user
    after = request.GET.get('after', 0)
    if u.is_authenticated():
        mentions = list(u.mentions.public(u).filter(pk__gt = after).order_by('-id')[:limit])
    else:
        mentions = []
    if len(mentions) == 0:
        return HttpResponseNotModified()    
    return render_to_response('board/mention_list.html', {'mentions':mentions}, context_instance)
