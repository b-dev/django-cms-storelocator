import tarfile
import StringIO
import shutil
import urllib
from django.utils import simplejson as json
from django.utils.encoding import smart_str
import os
import math
from django.conf import settings
from django.db import models
from cms.models import CMSPlugin

class LocationManager(models.Manager):
    def __init__(self):
        super(LocationManager, self).__init__()

    def near(self, source_latitude, source_longitude, distance):
        queryset = super(LocationManager, self).get_query_set()
        rough_distance = distance / 2
        queryset = queryset.filter(
                    latitude__range=(source_latitude - rough_distance, source_latitude + rough_distance),
                    longitude__range=(source_longitude - rough_distance, source_longitude + rough_distance)
                    )
        locations = []
        for location in queryset:
            if location.latitude and location.longitude:
                exact_distance = self.GetDistance(
                                    source_latitude, source_longitude,
                                    location,
                                    )
                if exact_distance <= distance:
                    setattr(location, 'distance', exact_distance)
                    locations.append(location)
                    #print "%s - %s" % (location, exact_distance)

        return locations
        #queryset = queryset.filter(id__in=[l.id for l in locations])
        #return queryset

    def GetDistance(self, source_latitude, source_longitude, target_location):
        lat_1 = math.radians(source_latitude)
        long_1 = math.radians(source_longitude)

        lat_2 = math.radians(target_location.latitude)
        long_2 = math.radians(target_location.longitude)

        dlong = long_2 - long_1
        dlat = lat_2 - lat_1
        a = (math.sin(dlat / 2))**2 + math.cos(lat_1) * math.cos(lat_2) * (math.sin(dlong / 2))**2
        c = 2 * math.asin(min(1, math.sqrt(a)))
        dist = 3956 * c
        return dist


class LocationType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Location(models.Model):
    location_types = models.ManyToManyField(LocationType, blank=True, null=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=False)
    country = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    province_short = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    cap = models.CharField(max_length=10, null=True, blank=True)
    number = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True, help_text="If you do not enter a latitude and longitude we will try to find them for you using Google Maps.")
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    objects = LocationManager()

    class Meta:
        verbose_name = "Store Location"
        verbose_name_plural = "Store Locations"

    def __unicode__(self):
        return self.name

    def get_full_address(self):
        map_query = self.address
        if self.number:
            map_query += ' %s' % self.number
        if self.cap:
            map_query += ', %s' % self.cap
        if self.city:
            map_query += ', %s' % self.city
        return map_query

    def get_lat_long(self):
        location = urllib.quote_plus(smart_str(self.get_full_address()))
        request = "http://maps.google.it/maps/api/geocode/json?address=%s&sensor=false" % location
        response = urllib.urlopen(request).read()
        data = json.loads(response)
        if data['status'] == 'OK':
            # take first result
            lat = str(data['results'][0]['geometry']['location']['lat'])
            long = str(data['results'][0]['geometry']['location']['lng'])
            region = ''
            province = ''
            short_province = ''
            for r in data['results'][0]['address_components']:
                if 'administrative_area_level_1' in r['types']:
                    region =  r['long_name']
                if 'administrative_area_level_3' in r['types']:
                    province =  r['long_name']
                    short_province = r['short_name']

            return (lat, long, region, province, short_province)
        else:
            return (None, None, None, None, None)

    def save(self, *args, **kwargs):
        #if not self.latitude or not self.longitude:
        lat, long, regione, provincia, short_province = self.get_lat_long()
        self.latitude = lat
        self.longitude = long
        if regione:
            self.region = regione.lower()
        if provincia:
            self.province = provincia.lower()
        if short_province:
            self.province_short = short_province.lower()
        super(Location, self).save(*args, **kwargs) # Call the "real" save() method.


DISTANCE_CHOICES = (
    ('1', '1.5 Km'),
    ('5', '10 Km'),
    ('10', '15 Km'),
    ('15', '25 Km'),
    ('25', '40 Km'),
    ('50', ' 80 Km'),
    ('100', '150 Km'),
)

class StoreLocator(CMSPlugin):
    default_distance = models.CharField(max_length=50, default='10', choices=DISTANCE_CHOICES)
    starting_location = models.CharField(max_length=255, help_text="A city or address to center the map on.")
    show_distance = models.BooleanField(default=True, help_text='Disabling this will render all locations on the map regardless of zoom level')
