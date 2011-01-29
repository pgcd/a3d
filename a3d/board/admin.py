from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.contrib.auth.admin import UserAdmin
from board.models import *
from faves.models import Fave


class ExtendedValueInline(GenericTabularInline):
    model = ExtendedAttributeValue


class IgnoreInline(GenericTabularInline):
    model = Ignore
    fields = ['content_type', ]

class FaveInline(GenericTabularInline):
    model = Fave

class InteractionInline(admin.StackedInline):
    model = Interaction

class MentionInline(admin.StackedInline):
    model = Mention


class UserProfileInline(admin.StackedInline):
    raw_id_fields = ['last_post', ] 
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline, ExtendedValueInline, FaveInline,]
    list_display = ('username', 'email',)
    search_fields = ['username', 'email', ]

# Unregister the built in user admin and register the custom User admin with UserProfile
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class TagsInline(admin.StackedInline):
    model = TagAttach
    
class TagAdmin(admin.ModelAdmin):
    model = Tag
     

class RepliesInline(GenericTabularInline):
    model = Post
    fields = ['user', '_title', ]

class PostAdmin(admin.ModelAdmin):
    inlines = [ExtendedValueInline, TagsInline, RepliesInline]
    save_as = True

admin.site.register(PostData, PostAdmin)
admin.site.register(Template)
admin.site.register(UserProfile)
admin.site.register(Tag, TagAdmin)
admin.site.register(InteractionType)
admin.site.register(Interaction)
admin.site.register(ExtendedAttribute)
admin.site.register(ExtendedAttributeValue)
    
