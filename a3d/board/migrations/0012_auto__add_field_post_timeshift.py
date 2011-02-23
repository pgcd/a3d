# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Post.timeshift'
        db.add_column('board_post', 'timeshift', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Post.timeshift'
        db.delete_column('board_post', 'timeshift')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'board.mention': {
            'Meta': {'ordering': "['-id']", 'unique_together': "(['user', 'post'],)", 'object_name': 'Mention'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_poster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'last_poster_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'mentions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'mentions'", 'to': "orm['auth.User']", 'through': "orm['board.Mention']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'no_replies': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'read_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'replies_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reverse_timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'posts'", 'symmetrical': 'False', 'through': "orm['board.TagAttach']", 'to': "orm['board.Tag']"}),
            'template_override': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Template']", 'null': 'True', 'blank': 'True'}),
            'timeshift': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_posts'", 'null': 'True', 'to': "orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'blank': 'True'}),
            'versions_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'views_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wiki': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_attach': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'reverse_timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Template']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'board.tagattach': {
            'Meta': {'unique_together': "(('tag', 'post'),)", 'object_name': 'TagAttach'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Post']"}),
            'reverse_timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Tag']"})
        },
        'board.template': {
            'Meta': {'object_name': 'Template'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'derived'", 'null': 'True', 'to': "orm['board.Template']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'board.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            '_last_reply_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'always_preview': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_quote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'back_to_topic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_change_short_desc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_modify_profile_own': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_set_nick_color': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contributor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'custom_nick_display': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hidden_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alias': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_page_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 1, 29, 12, 56, 55, 13060)', 'db_index': 'True'}),
            'last_page_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'last_post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posted_by'", 'null': 'True', 'to': "orm['board.Post']"}),
            'link_source_post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'long_desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mana': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'min_rating': ('django.db.models.fields.SmallIntegerField', [], {'default': '2', 'blank': 'True'}),
            'mod_denied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'post_per_page': ('django.db.models.fields.SmallIntegerField', [], {'default': '30', 'blank': 'True'}),
            'posts_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replies_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reverse_timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'save_password': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'secret_answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'secret_question': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'short_desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'show_ruler': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signature': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['board']
