# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'UserProfile.can_set_nick_color'
        db.delete_column('board_userprofile', 'can_set_nick_color')

        # Adding field 'UserProfile.can_change_custom_nick_display'
        db.add_column('board_userprofile', 'can_change_custom_nick_display', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Changing field 'UserProfile.auto_quote'
        db.alter_column('board_userprofile', 'auto_quote', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.hidden_status'
        db.alter_column('board_userprofile', 'hidden_status', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.save_password'
        db.alter_column('board_userprofile', 'save_password', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.contributor'
        db.alter_column('board_userprofile', 'contributor', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.mod_denied'
        db.alter_column('board_userprofile', 'mod_denied', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.is_alias'
        db.alter_column('board_userprofile', 'is_alias', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.hidden_email'
        db.alter_column('board_userprofile', 'hidden_email', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.back_to_topic'
        db.alter_column('board_userprofile', 'back_to_topic', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.always_preview'
        db.alter_column('board_userprofile', 'always_preview', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.can_modify_profile_own'
        db.alter_column('board_userprofile', 'can_modify_profile_own', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.auto_login'
        db.alter_column('board_userprofile', 'auto_login', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.can_change_short_desc'
        db.alter_column('board_userprofile', 'can_change_short_desc', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.show_ruler'
        db.alter_column('board_userprofile', 'show_ruler', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'UserProfile.link_source_post'
        db.alter_column('board_userprofile', 'link_source_post', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'PostDataVersion.is_active'
        db.alter_column('board_postdataversion', 'is_active', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Tag.is_active'
        db.alter_column('board_tag', 'is_active', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'InteractionType.is_active'
        db.alter_column('board_interactiontype', 'is_active', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Template.is_active'
        db.alter_column('board_template', 'is_active', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Post.wiki'
        db.alter_column('board_post', 'wiki', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Post.sticky'
        db.alter_column('board_post', 'sticky', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Post.read_only'
        db.alter_column('board_post', 'read_only', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Post.no_replies'
        db.alter_column('board_post', 'no_replies', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Post.is_active'
        db.alter_column('board_post', 'is_active', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Post.is_private'
        db.alter_column('board_post', 'is_private', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Interaction.is_active'
        db.alter_column('board_interaction', 'is_active', self.gf('django.db.models.fields.BooleanField')(blank=True))


    def backwards(self, orm):
        
        # Adding field 'UserProfile.can_set_nick_color'
        db.add_column('board_userprofile', 'can_set_nick_color', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'UserProfile.can_change_custom_nick_display'
        db.delete_column('board_userprofile', 'can_change_custom_nick_display')

        # Changing field 'UserProfile.auto_quote'
        db.alter_column('board_userprofile', 'auto_quote', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.hidden_status'
        db.alter_column('board_userprofile', 'hidden_status', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.save_password'
        db.alter_column('board_userprofile', 'save_password', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.contributor'
        db.alter_column('board_userprofile', 'contributor', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.mod_denied'
        db.alter_column('board_userprofile', 'mod_denied', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.is_alias'
        db.alter_column('board_userprofile', 'is_alias', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.hidden_email'
        db.alter_column('board_userprofile', 'hidden_email', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.back_to_topic'
        db.alter_column('board_userprofile', 'back_to_topic', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.always_preview'
        db.alter_column('board_userprofile', 'always_preview', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.can_modify_profile_own'
        db.alter_column('board_userprofile', 'can_modify_profile_own', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.auto_login'
        db.alter_column('board_userprofile', 'auto_login', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.can_change_short_desc'
        db.alter_column('board_userprofile', 'can_change_short_desc', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.show_ruler'
        db.alter_column('board_userprofile', 'show_ruler', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'UserProfile.link_source_post'
        db.alter_column('board_userprofile', 'link_source_post', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'PostDataVersion.is_active'
        db.alter_column('board_postdataversion', 'is_active', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Tag.is_active'
        db.alter_column('board_tag', 'is_active', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InteractionType.is_active'
        db.alter_column('board_interactiontype', 'is_active', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Template.is_active'
        db.alter_column('board_template', 'is_active', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Post.wiki'
        db.alter_column('board_post', 'wiki', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Post.sticky'
        db.alter_column('board_post', 'sticky', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Post.read_only'
        db.alter_column('board_post', 'read_only', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Post.no_replies'
        db.alter_column('board_post', 'no_replies', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Post.is_active'
        db.alter_column('board_post', 'is_active', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Post.is_private'
        db.alter_column('board_post', 'is_private', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Interaction.is_active'
        db.alter_column('board_interaction', 'is_active', self.gf('django.db.models.fields.BooleanField')())


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'board.extendedattribute': {
            'Meta': {'object_name': 'ExtendedAttribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'board.extendedattributevalue': {
            'Meta': {'object_name': 'ExtendedAttributeValue'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.ExtendedAttribute']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'board.ignore': {
            'Meta': {'object_name': 'Ignore'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'board.interaction': {
            'Meta': {'unique_together': "(['user', 'interaction_type', 'object_id'],)", 'object_name': 'Interaction'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interaction_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interactions'", 'to': "orm['board.InteractionType']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interactions'", 'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'board.interactiontype': {
            'Meta': {'unique_together': "(['name', 'content_type'],)", 'object_name': 'InteractionType'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'board.mention': {
            'Meta': {'unique_together': "(['user', 'post'],)", 'object_name': 'Mention'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'board.post': {
            'Meta': {'object_name': 'Post'},
            '_last_reply_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            '_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_poster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'last_poster_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'mentions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'mentions'", 'to': "orm['auth.User']", 'through': "orm['board.Mention']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'no_replies': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'read_only': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'replies_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'posts'", 'symmetrical': 'False', 'through': "orm['board.TagAttach']", 'to': "orm['board.Tag']"}),
            'template_override': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Template']", 'null': 'True', 'blank': 'True'}),
            'timeshift': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_posts'", 'null': 'True', 'to': "orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'blank': 'True'}),
            'versions_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'views_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wiki': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'board.postdata': {
            'Meta': {'object_name': 'PostData', '_ormbases': ['board.Post']},
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_markup': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['board.Post']", 'unique': 'True', 'primary_key': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'tagset': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'userdata': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'board.postdataversion': {
            'Meta': {'object_name': 'PostDataVersion'},
            'body_markup': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['board.PostData']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'board.tag': {
            'Meta': {'object_name': 'Tag'},
            'attach_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Template']", 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'title': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'board.tagattach': {
            'Meta': {'unique_together': "(('tag', 'post'),)", 'object_name': 'TagAttach'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Post']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Tag']"}),
            'timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'})
        },
        'board.template': {
            'Meta': {'object_name': 'Template'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'derived'", 'null': 'True', 'to': "orm['board.Template']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'board.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            '_last_reply_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'always_preview': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'auto_login': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'auto_quote': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'back_to_topic': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'can_change_custom_nick_display': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'can_change_short_desc': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'can_modify_profile_own': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'custom_nick_display': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hidden_email': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hidden_status': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alias': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_page_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 23, 12, 5, 55, 584000)', 'db_index': 'True'}),
            'last_page_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'last_post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posted_by'", 'null': 'True', 'to': "orm['board.Post']"}),
            'link_source_post': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'long_desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mana': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'min_rating': ('django.db.models.fields.SmallIntegerField', [], {'default': '2', 'blank': 'True'}),
            'mod_denied': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'post_per_page': ('django.db.models.fields.SmallIntegerField', [], {'default': '30', 'blank': 'True'}),
            'posts_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replies_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'save_password': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'secret_answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'secret_question': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'short_desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'show_ruler': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['board']
