'''
Created on 06/apr/2010

@author: pgcd
'''
from django.conf.urls.defaults import url, patterns
from piston.resource import Resource
from api.handlers import PostHandler, TagHandler, UserHandler

post_resource = Resource(PostHandler)
tag_resource = Resource(TagHandler)
user_resource = Resource(UserHandler)

urlpatterns = patterns('',
   url(r'^posts/(?P<id>\d+)$', post_resource, name = 'api_posts_by_id'),
   url(r'^posts$', post_resource, name = 'api_posts_list'),
   url(r'^tags/(?P<title_partial>\w+)$', tag_resource, name = 'api_tags_by_title'),
   url(r'^tags$', tag_resource, name = 'api_tags_list'),
  url(r'^users/$', user_resource, name = 'api_users_list'),
)
