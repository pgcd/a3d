'''
Created on 13/mag/2010

@author: pgcd
'''
from django.dispatch import Signal

interaction_event=Signal(providing_args=["request", "user", "object_id", "value", "interaction_type"])

post_read=Signal(providing_args=["user", "post_id", "last_item"])
post_view=Signal(providing_args=["user", "post_id", "view_time"])
tag_read=Signal(providing_args=["user", "tag_id", "last_item"])
home_read=Signal(providing_args=["user", "last_item"])
post_fetching_list=Signal(providing_args=["request", "queryset"])
post_list_fetched=Signal(providing_args=["request", "object_list"])

postdata_pre_create=Signal(providing_args=["request", "instance"])
postdata_created=Signal(providing_args=["request", "instance"])
