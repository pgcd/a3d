from django.conf.urls.defaults import url, patterns, include
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import profiles.views as profile_views #@UnresolvedImport
import sys
admin.autodiscover()

urlpatterns = patterns('',
    #TODO: Can we move this crap to board?
    # (r'^a3d/', include('a3d.foo.urls')),
    url(r'^(?:home)?$', 'board.views.post.home', name = "board_post_list_home"),
    url(r'^go/post_id/(?P<post_id>\d+)$', 'django.views.generic.simple.redirect_to', {'url': '/p/%(post_id)s', 'permanent': True}, name = "board_post_view"),
    url(r'^p/(?P<post_id>\d+)$', 'board.views.post.view', name = "board_post_view"),
    url(r'^p/(?P<post_id>\d+)/info$', 'board.views.post.view', {'info_only':True}, name = "board_post_view_info"),
    url(r'^p/(?P<post_id>\d+)/edit$', 'board.views.post.edit', name = "board_post_edit"),
    url(r'^p/(?P<post_id>\d+)/mark_read$', 'board.views.post.mark_as', {'action':'read'}, name = "board_post_mark_as_read"),
    url(r'^p/(?P<post_id>\d+)/mark_unread$', 'board.views.post.mark_as', {'action':'unread'}, name = "board_post_mark_as_unread"),

    url(r'^rate/(?P<post_id>\d+)/(?P<action>down|up)$', 'board.views.post.rate', name = "board_post_rate"),
    url(r'^p/create$', 'board.views.post.create', name = "board_post_create"),
    url(r'^p/preview$', 'board.views.post.preview', name = "board_post_preview"),
#    url(r'^p/delete$', 'board.views.post.delete', name="board_post_delete"),
    url(r'^by/(?P<username>.+)$', 'board.views.post.list_by_user', name = "board_post_list_by_user"),
    url(r'^s/(?P<search_term>.+)$', 'board.views.post.search', name = "board_post_search"),

    url(r'^i/all_read/(?P<post_id>\d+)$', 'board.views.userprofile.mark_all_read', name = "board_userprofile_all_read"),


    url(r'^t/0$', 'board.views.post.list_tagless', name = "board_post_list_tagless"),
    url(r'^t/autocomplete$', 'board.views.tag.autocomplete', name = "board_tag_autocomplete"),
#    url(r'^t/create/#(?P<tag_title>[^\d][-_\w]+)$', 'board.views.tag.create', name="board_tag_create"),
#    url(r'^t/edit/#(?P<tag_title>[^\d][-_\w]+)$', 'board.views.tag.edit', name="board_tag_edit"),
#    url(r'^t/delete/#(?P<tag_title>[^\d][-_\w]+)$', 'board.views.tag.delete', name="board_tag_delete"), #only if unattached
    url(r'^t/attach$', 'board.views.tag.attach', name = "board_tag_attach"), #require POST tag_id & post_id?
    url(r'^t/detach$', 'board.views.tag.detach', name = "board_tag_detach"), #require POST tag_id & post_id?    
    url(r'^t/(?P<post_id>\d+)$', 'board.views.tag.list_on_post', name = "board_tag_list_on_post"),
    url(r'^t/$', 'board.views.tag.list', name = "board_tags_list"),
    url(r'^t/(?P<tag_title>[-_\w]+)$', 'board.views.post.list_by_tag_title', name = "board_post_list_by_tag_title"),
    

#    url(r'^f/create$', 'board.views.fave.create', name="board_fave_create"),
#    url(r'^f/delete/(?P<content_type)\w+)/(?P<object_id>\w+)$', 'board.views.favorite.delete', name="board_favorite_delete"),
#    url(r'^f/(?P<content_type)\w+)/(?P<object_id>\w+)$', 'board.views.favorite.delete', name="board_favorite_delete"),

    (r'^f/', include('faves.urls')),
    url(r'^f/$', 'board.views.fave.fave_list', name = "board_fave_list"),
    url(r'^star/$', 'board.views.fave.add_star', name = "board_add_star"),
    (r'^accounts/', include('registration.urls')),
    (r'^api/', include('api.urls')),
    (r'^admin/', admin.site.urls),
    url(r'^u/autocomplete$', 'board.views.userprofile.autocomplete', name = "board_userprofile_autocomplete"),
    url(r'^u/create/$', profile_views.create_profile, name = 'profiles_create_profile'),
    url(r'^u/edit/$', profile_views.edit_profile, name = 'profiles_edit_profile'),
    url(r'^u/mentions/(?P<limit>\d+)?/?$', 'board.views.mention.mentions_list', name = 'board_own_mentions_list'),
    url(r'^u/(?P<username>.+)/$', profile_views.profile_detail, name = 'profiles_profile_detail'),
    url(r'^u/$', profile_views.profile_list, name = 'profiles_profile_list'),
    url(r'^login$', 'django.contrib.auth.views.login'),
    url(r'^logout$', 'django.contrib.auth.views.logout'),
)
