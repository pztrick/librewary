# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brewer'
        db.create_table(u'core_brewer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('show_facebook', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contributed_cash', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('outstanding_fees', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'core', ['Brewer'])

        # Adding M2M table for field groups on 'Brewer'
        db.create_table(u'core_brewer_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('brewer', models.ForeignKey(orm[u'core.brewer'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'core_brewer_groups', ['brewer_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Brewer'
        db.create_table(u'core_brewer_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('brewer', models.ForeignKey(orm[u'core.brewer'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'core_brewer_user_permissions', ['brewer_id', 'permission_id'])

        # Adding model 'Commodity'
        db.create_table(u'core_commodity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['Commodity'])

        # Adding model 'EquipmentOffer'
        db.create_table(u'core_equipmentoffer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Brewer'])),
            ('tool', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'core', ['EquipmentOffer'])

        # Adding model 'Equipment'
        db.create_table(u'core_equipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contributor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Brewer'])),
            ('commodity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Commodity'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contributed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('p2p_is_checked_out', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'core', ['Equipment'])

        # Adding model 'Loan'
        db.create_table(u'core_loan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('borrower', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Brewer'])),
            ('commodity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Commodity'])),
            ('date_requested', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('earnest_deposit', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('equipment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Equipment'], unique=True, null=True, blank=True)),
            ('age_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_borrowed', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_returned', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Loan'])

        # Adding model 'Voucher'
        db.create_table(u'core_voucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('underwriter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Brewer'])),
            ('loan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Loan'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('date_offered', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Voucher'])

        # Adding model 'Transaction'
        db.create_table(u'core_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('debit', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('credit', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('staffer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Brewer'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Brewer'
        db.delete_table(u'core_brewer')

        # Removing M2M table for field groups on 'Brewer'
        db.delete_table('core_brewer_groups')

        # Removing M2M table for field user_permissions on 'Brewer'
        db.delete_table('core_brewer_user_permissions')

        # Deleting model 'Commodity'
        db.delete_table(u'core_commodity')

        # Deleting model 'EquipmentOffer'
        db.delete_table(u'core_equipmentoffer')

        # Deleting model 'Equipment'
        db.delete_table(u'core_equipment')

        # Deleting model 'Loan'
        db.delete_table(u'core_loan')

        # Deleting model 'Voucher'
        db.delete_table(u'core_voucher')

        # Deleting model 'Transaction'
        db.delete_table(u'core_transaction')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.brewer': {
            'Meta': {'object_name': 'Brewer'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'contributed_cash': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'outstanding_fees': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'show_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_facebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'core.commodity': {
            'Meta': {'object_name': 'Commodity'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.equipment': {
            'Meta': {'object_name': 'Equipment'},
            'commodity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Commodity']"}),
            'contributed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Brewer']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'p2p_is_checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'core.equipmentoffer': {
            'Meta': {'object_name': 'EquipmentOffer'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Brewer']"}),
            'tool': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.loan': {
            'Meta': {'object_name': 'Loan'},
            'age_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'borrower': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Brewer']"}),
            'commodity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Commodity']"}),
            'date_borrowed': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_requested': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_returned': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'earnest_deposit': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'equipment': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Equipment']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'credit': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'debit': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staffer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Brewer']"})
        },
        u'core.voucher': {
            'Meta': {'object_name': 'Voucher'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'date_offered': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Loan']"}),
            'underwriter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Brewer']"})
        }
    }

    complete_apps = ['core']