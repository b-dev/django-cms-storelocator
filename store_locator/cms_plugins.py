from collections import OrderedDict
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from store_locator.models import StoreLocator, Location, DISTANCE_CHOICES, LocationType

class StoreLocatorPlugin(CMSPluginBase):
    """Subclass of Text plugin, includes 'topic' & 'css' fields"""

    model = StoreLocator
    name = _("Store Locator Map")
    render_template = "store_locator/store_locator_map.html"

    def render(self, context, instance, placeholder):
        country = context['request'].GET.get('country', None)
        region = context['request'].GET.get('region', None)
        #province = context['request'].GET.get('province', None)

        location_list = Location.objects.all().order_by('country', 'region', 'province').values('country', 'region', 'province')

        country_list_all = SortedDict()
        region_list_all = SortedDict()
        province_list_all = SortedDict()

        region_country_all = SortedDict()
        province_region_all = SortedDict()

        for loc in location_list:
            country_list_all[loc['country']] = None
            region_list_all[loc['region']] = None
            province_list_all[loc['province']] = None
            if country and not region:
                if loc['country'] == country:
                    region_country_all[loc['region']] = None
            if region:
                if loc['region'] == region:
                    province_region_all[loc['province']] = None

        get_lat_long_url = reverse('admin:get_lat_long_url')
        get_near_locations_url = reverse('admin:get_near_locations_url')
        get_list_locations_url = reverse('admin:get_list_locations_url')
        location_types = LocationType.objects.all()

        region_list = region_list_all.keys()
        region_list.sort()

        province_list = province_list_all.keys()
        province_list.sort()

        context.update({
            'get_lat_long_url': get_lat_long_url,
            'get_near_locations_url': get_near_locations_url,
            'get_list_locations_url': get_list_locations_url,
            'country_list_all': country_list_all.keys(),
            'region_list_all': region_list,
            'province_list_all': province_list,
            'region_country_all': region_country_all.keys(),
            'province_region_all': province_region_all.keys(),
            'instance': instance,
            'distance_choices': DISTANCE_CHOICES,
            'location_types': location_types,
        })
        return context

plugin_pool.register_plugin(StoreLocatorPlugin)
