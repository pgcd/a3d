# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ExtendedAttribute'
        db.create_table('board_extendedattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('board', ['ExtendedAttribute'])

        # Adding model 'ExtendedAttributeValue'
        db.create_table('board_extendedattributevalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['board.ExtendedAttribute'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('board', ['ExtendedAttributeValue'])

        # Adding model 'Ignore'
        db.create_table('board_ignore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('board', ['Ignore'])

        # Adding model 'Template'
        db.create_table('board_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='derived', null=True, to=orm['board.Template'])),
        ))
        db.send_create_signal('board', ['Template'])

        # Adding model 'Mention'
        db.create_table('board_mention', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['board.UserProfile'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['board.Post'])),
        ))
        db.send_create_signal('board', ['Mention'])

        # Adding model 'InteractionType'
        db.create_table('board_interactiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('board', ['InteractionType'])

        # Adding unique constraint on 'InteractionType', fields ['name', 'content_type']
        db.create_unique('board_interactiontype', ['name', 'content_type_id'])

        # Adding model 'Interaction'
        db.create_table('board_interaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interactions', to=orm['auth.User'])),
            ('interaction_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interactions', to=orm['board.InteractionType'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('board', ['Interaction'])

        # Adding unique constraint on 'Interaction', fields ['user', 'interaction_type', 'object_id']
        db.create_unique('board_interaction', ['user_id', 'interaction_type_id', 'object_id'])

        # Adding model 'Post'
        db.create_table('board_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_posts', null=True, to=orm['auth.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('views_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('replies_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('versions_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(default='0.0.0.0', max_length=15)),
            ('userdata', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, blank=True)),
            ('last_poster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('reverse_timestamp', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('read_only', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('no_replies', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('wiki', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('template_override', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['board.Template'], null=True, blank=True)),
            ('_last_reply_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('board', ['Post'])

        # Adding model 'PostData'
        db.create_table('board_postdata', (
            ('post_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['board.Post'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('body_markup', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('signature', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('tagset', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('board', ['PostData'])

        # Adding model 'TagAttach'
        db.create_table('board_tagattach', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['board.Tag'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['board.Post'])),
            ('reverse_timestamp', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('board', ['TagAttach'])

        # Adding unique constraint on 'TagAttach', fields ['tag', 'post']
        db.create_unique('board_tagattach', ['tag_id', 'post_id'])

        # Adding model 'Tag'
        db.create_table('board_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('title', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('reverse_timestamp', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('icon', self.gf('django.db.models.fields.files.FileField')(default='', max_length=100, blank=True)),
            ('attach_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['board.Template'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('board', ['Tag'])

        # Adding model 'UserProfile'
        db.create_table('board_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('hidden_status', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('hidden_email', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('rating_total', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('signature', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('secret_question', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('secret_answer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('short_desc', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('long_desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('custom_nick_display', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('mod_denied', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('auto_login', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('back_to_topic', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('auto_quote', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('link_source_post', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('always_preview', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('can_modify_profile_own', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('can_set_nick_color', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('can_change_short_desc', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('show_ruler', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('save_password', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('contributor', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('is_alias', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('post_per_page', self.gf('django.db.models.fields.SmallIntegerField')(default=30, blank=True)),
            ('min_rating', self.gf('django.db.models.fields.SmallIntegerField')(default=2, blank=True)),
            ('mana', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_post', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='posted_by', null=True, to=orm['board.Post'])),
            ('posts_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('_last_reply_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('reverse_timestamp', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('replies_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('board', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'ExtendedAttribute'
        db.delete_table('board_extendedattribute')

        # Deleting model 'ExtendedAttributeValue'
        db.delete_table('board_extendedattributevalue')

        # Deleting model 'Ignore'
        db.delete_table('board_ignore')

        # Deleting model 'Template'
        db.delete_table('board_template')

        # Deleting model 'Mention'
        db.delete_table('board_mention')

        # Deleting model 'InteractionType'
        db.delete_table('board_interactiontype')

        # Removing unique constraint on 'InteractionType', fields ['name', 'content_type']
        db.delete_unique('board_interactiontype', ['name', 'content_type_id'])

        # Deleting model 'Interaction'
        db.delete_table('board_interaction')

        # Removing unique constraint on 'Interaction', fields ['user', 'interaction_type', 'object_id']
        db.delete_unique('board_interaction', ['user_id', 'interaction_type_id', 'object_id'])

        # Deleting model 'Post'
        db.delete_table('board_post')

        # Deleting model 'PostData'
        db.delete_table('board_postdata')

        # Deleting model 'TagAttach'
        db.delete_table('board_tagattach')

        # Removing unique constraint on 'TagAttach', fields ['tag', 'post']
        db.delete_unique('board_tagattach', ['tag_id', 'post_id'])

        # Deleting model 'Tag'
        db.delete_table('board_tag')

        # Deleting model 'UserProfile'
        db.delete_table('board_userprofile')


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
            'Meta': {'object_name': 'Mention'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.UserProfile']"})
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
            'last_poster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'no_replies': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'read_only': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'replies_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reverse_timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'posts'", 'symmetrical': 'False', 'through': "orm['board.TagAttach']", 'to': "orm['board.Tag']"}),
            'template_override': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['board.Template']", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_posts'", 'null': 'True', 'to': "orm['auth.User']"}),
            'userdata': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
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
            'tagset': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'board.tag': {
            'Meta': {'object_name': 'Tag'},
            'attach_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'derived'", 'null': 'True', 'to': "orm['board.Template']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'board.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            '_last_reply_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            '_mentions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'mentioned_users'", 'to': "orm['board.Post']", 'through': "orm['board.Mention']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'always_preview': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'auto_login': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'auto_quote': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'back_to_topic': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'can_change_short_desc': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'can_modify_profile_own': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'can_set_nick_color': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'custom_nick_display': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hidden_email': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hidden_status': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alias': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
            'reverse_timestamp': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'save_password': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'secret_answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'secret_question': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'short_desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'show_ruler': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
