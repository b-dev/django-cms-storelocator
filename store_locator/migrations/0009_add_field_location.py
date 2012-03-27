# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Location.country'
        db.add_column('store_locator_location', 'country', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Location.region'
        db.add_column('store_locator_location', 'region', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Location.province'
        db.add_column('store_locator_location', 'province', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Location.province_short'
        db.add_column('store_locator_location', 'province_short', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True), keep_default=False)

        # Adding field 'Location.city'
        db.add_column('store_locator_location', 'city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Location.cap'
        db.add_column('store_locator_location', 'cap', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True), keep_default=False)

        # Adding field 'Location.number'
        db.add_column('store_locator_location', 'number', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True), keep_default=False)

        # Adding field 'Location.email'
        db.add_column('store_locator_location', 'email', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True, blank=True), keep_default=False)

        # Changing field 'Location.address'
        db.alter_column('store_locator_location', 'address', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Adding field 'StoreLocator.show_distance'
        db.add_column('cmsplugin_storelocator', 'show_distance', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Location.country'
        db.delete_column('store_locator_location', 'country')

        # Deleting field 'Location.region'
        db.delete_column('store_locator_location', 'region')

        # Deleting field 'Location.province'
        db.delete_column('store_locator_location', 'province')

        # Deleting field 'Location.province_short'
        db.delete_column('store_locator_location', 'province_short')

        # Deleting field 'Location.city'
        db.delete_column('store_locator_location', 'city')

        # Deleting field 'Location.cap'
        db.delete_column('store_locator_location', 'cap')

        # Deleting field 'Location.number'
        db.delete_column('store_locator_location', 'number')

        # Deleting field 'Location.email'
        db.delete_column('store_locator_location', 'email')

        # Changing field 'Location.address'
        db.alter_column('store_locator_location', 'address', self.gf('django.db.models.fields.TextField')(max_length=255))

        # Deleting field 'StoreLocator.show_distance'
        db.delete_column('cmsplugin_storelocator', 'show_distance')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'store_locator.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cap': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['store_locator.LocationType']", 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'province_short': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'store_locator.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'store_locator.storelocator': {
            'Meta': {'object_name': 'StoreLocator', 'db_table': "'cmsplugin_storelocator'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'default_distance': ('django.db.models.fields.CharField', [], {'default': "'10'", 'max_length': '50'}),
            'show_distance': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'starting_location': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['store_locator']
