import urllib2
import urllib
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from store_locator.models import Location

def get_lat_long(request):
    if not request.GET.get('q'):
        return HttpResponse('')
    query = request.GET.get('q')
    if query == "L'Aquila":
        query = "LAquila"
    args = urllib.urlencode({'q': query})
    r = urllib2.urlopen("http://maps.google.com/maps/geo?output=csv&%s" % args)
    return HttpResponse(r.read())

def get_near_locations(request):
    try:
        latitude = float(request.GET.get('lat'))
        longitude = float(request.GET.get('long'))
        distance = int(request.GET.get('distance', 0))
        location_type = request.GET.get('location_type', '0')
    except:
        return HttpResponse('[]')

    locations = Location.objects.near(latitude, longitude, distance)
    if location_type:
        locations = [l for l in locations if location_type in [str(t[0]) for t in l.location_types.values_list('id')]]
    json_locations = []
    locations.sort(key=lambda loc: loc.distance)
    for location in locations:
        location_dict = {}
        location_dict['id'] = location.id
        location_dict['name'] = location.name
        location_dict['address'] = location.address
        location_dict['latitude'] = location.latitude
        location_dict['longitude'] = location.longitude
        location_dict['distance'] = location.distance
        location_dict['description'] = location.description or ''
        location_dict['url'] = location.url or ''
        location_dict['phone'] = location.phone or ''
        json_locations.append(location_dict)
    return HttpResponse(json.dumps(json_locations), mimetype="application/json")

def get_list_locations(request):
    try:
        region = request.GET.get('region')
        province = request.GET.get('province')
    except:
        return HttpResponse('[]')

    locations = Location.objects.all()
    if not region and not province:
        return HttpResponse('[]')

    if region:
        locations = locations.filter(region__iexact=region)
    if province:
        locations = locations.filter(province__iexact=province)

    locations = locations.order_by('region', 'province', 'name')
    json_locations = []

    for location in locations:
        location_dict = {}
        location_dict['id'] = location.id
        location_dict['name'] = location.name
        location_dict['address'] = location.address
        location_dict['latitude'] = location.latitude
        location_dict['longitude'] = location.longitude
        location_dict['description'] = location.description or ''
        location_dict['url'] = location.url or ''
        location_dict['phone'] = location.phone or ''
        json_locations.append(location_dict)
    return HttpResponse(json.dumps(json_locations), mimetype="application/json")