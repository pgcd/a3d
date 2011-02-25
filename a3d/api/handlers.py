'''
Created on 06/apr/2010

@author: pgcd
'''
from piston.handler import BaseHandler
from board.models import Post, Tag, TagAttach
from django.contrib.auth.models import User
from urllib import unquote

class PostHandler(BaseHandler):
    model = Post
    #TODO: Remove all @user posts

class UserHandler(BaseHandler):
    model = User
    allowed_methods = ('GET',)
    fields = ('username',)

    @classmethod
    def read(cls, request, username = None):
        q = request.GET.get('term', None)
        if q is not None:
            user = User.objects.filter(username__istartswith = unquote(q))
            return user
        user = User.objects.filter(username = username)
        return user

    
class TagHandler(BaseHandler):
    model = Tag
    allowed_methods = ('GET',)
    fields = ('title',)

    @classmethod
    def read(cls, request, title = None):
        q = request.GET.get('term', None)
        if q is not None:
            tag = Tag.objects.filter(title__startswith = q)
            return tag
        tag = Tag.objects.filter(title = title)
        return tag
        
class TagAttachHandler(BaseHandler):
    model = TagAttach
    allowed_methods = ('GET', 'DELETE')
