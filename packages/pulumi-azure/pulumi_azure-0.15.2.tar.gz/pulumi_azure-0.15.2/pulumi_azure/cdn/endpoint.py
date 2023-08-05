# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Endpoint(pulumi.CustomResource):
    """
    A CDN Endpoint is the entity within a CDN Profile containing configuration information regarding caching behaviors and origins. The CDN Endpoint is exposed using the URL format <endpointname>.azureedge.net by default, but custom domains can also be created.
    """
    def __init__(__self__, __name__, __opts__=None, content_types_to_compresses=None, geo_filters=None, is_compression_enabled=None, is_http_allowed=None, is_https_allowed=None, location=None, name=None, optimization_type=None, origins=None, origin_host_header=None, origin_path=None, probe_path=None, profile_name=None, querystring_caching_behaviour=None, resource_group_name=None, tags=None):
        """Create a Endpoint resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if content_types_to_compresses and not isinstance(content_types_to_compresses, list):
            raise TypeError('Expected property content_types_to_compresses to be a list')
        __self__.content_types_to_compresses = content_types_to_compresses
        """
        An array of strings that indicates a content types on which compression will be applied. The value for the elements should be MIME types.
        """
        __props__['contentTypesToCompresses'] = content_types_to_compresses

        if geo_filters and not isinstance(geo_filters, list):
            raise TypeError('Expected property geo_filters to be a list')
        __self__.geo_filters = geo_filters
        """
        A set of Geo Filters for this CDN Endpoint. Each `geo_filter` block supports fields documented below.
        """
        __props__['geoFilters'] = geo_filters

        if is_compression_enabled and not isinstance(is_compression_enabled, bool):
            raise TypeError('Expected property is_compression_enabled to be a bool')
        __self__.is_compression_enabled = is_compression_enabled
        """
        Indicates whether compression is to be enabled. Defaults to false.
        """
        __props__['isCompressionEnabled'] = is_compression_enabled

        if is_http_allowed and not isinstance(is_http_allowed, bool):
            raise TypeError('Expected property is_http_allowed to be a bool')
        __self__.is_http_allowed = is_http_allowed
        """
        Defaults to `true`.
        """
        __props__['isHttpAllowed'] = is_http_allowed

        if is_https_allowed and not isinstance(is_https_allowed, bool):
            raise TypeError('Expected property is_https_allowed to be a bool')
        __self__.is_https_allowed = is_https_allowed
        """
        Defaults to `true`.
        """
        __props__['isHttpsAllowed'] = is_https_allowed

        if not location:
            raise TypeError('Missing required property location')
        elif not isinstance(location, basestring):
            raise TypeError('Expected property location to be a basestring')
        __self__.location = location
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        __props__['location'] = location

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        Specifies the name of the CDN Endpoint. Changing this forces a new resource to be created.
        """
        __props__['name'] = name

        if optimization_type and not isinstance(optimization_type, basestring):
            raise TypeError('Expected property optimization_type to be a basestring')
        __self__.optimization_type = optimization_type
        """
        What types of optimization should this CDN Endpoint optimize for? Possible values include `DynamicSiteAcceleration`, `GeneralMediaStreaming`, `GeneralWebDelivery`, `LargeFileDownload` and `VideoOnDemandMediaStreaming`.
        """
        __props__['optimizationType'] = optimization_type

        if not origins:
            raise TypeError('Missing required property origins')
        elif not isinstance(origins, list):
            raise TypeError('Expected property origins to be a list')
        __self__.origins = origins
        """
        The set of origins of the CDN endpoint. When multiple origins exist, the first origin will be used as primary and rest will be used as failover options. Each `origin` block supports fields documented below.
        """
        __props__['origins'] = origins

        if origin_host_header and not isinstance(origin_host_header, basestring):
            raise TypeError('Expected property origin_host_header to be a basestring')
        __self__.origin_host_header = origin_host_header
        """
        The host header CDN provider will send along with content requests to origins. Defaults to the host name of the origin.
        """
        __props__['originHostHeader'] = origin_host_header

        if origin_path and not isinstance(origin_path, basestring):
            raise TypeError('Expected property origin_path to be a basestring')
        __self__.origin_path = origin_path
        """
        The path used at for origin requests.
        """
        __props__['originPath'] = origin_path

        if probe_path and not isinstance(probe_path, basestring):
            raise TypeError('Expected property probe_path to be a basestring')
        __self__.probe_path = probe_path
        """
        the path to a file hosted on the origin which helps accelerate delivery of the dynamic content and calculate the most optimal routes for the CDN. This is relative to the `origin_path`.
        """
        __props__['probePath'] = probe_path

        if not profile_name:
            raise TypeError('Missing required property profile_name')
        elif not isinstance(profile_name, basestring):
            raise TypeError('Expected property profile_name to be a basestring')
        __self__.profile_name = profile_name
        """
        The CDN Profile to which to attach the CDN Endpoint.
        """
        __props__['profileName'] = profile_name

        if querystring_caching_behaviour and not isinstance(querystring_caching_behaviour, basestring):
            raise TypeError('Expected property querystring_caching_behaviour to be a basestring')
        __self__.querystring_caching_behaviour = querystring_caching_behaviour
        """
        Sets query string caching behavior. Allowed values are `IgnoreQueryString`, `BypassCaching` and `UseQueryString`. Defaults to `IgnoreQueryString`.
        """
        __props__['querystringCachingBehaviour'] = querystring_caching_behaviour

        if not resource_group_name:
            raise TypeError('Missing required property resource_group_name')
        elif not isinstance(resource_group_name, basestring):
            raise TypeError('Expected property resource_group_name to be a basestring')
        __self__.resource_group_name = resource_group_name
        """
        The name of the resource group in which to create the CDN Endpoint.
        """
        __props__['resourceGroupName'] = resource_group_name

        if tags and not isinstance(tags, dict):
            raise TypeError('Expected property tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags to assign to the resource.
        """
        __props__['tags'] = tags

        __self__.host_name = pulumi.runtime.UNKNOWN

        super(Endpoint, __self__).__init__(
            'azure:cdn/endpoint:Endpoint',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'contentTypesToCompresses' in outs:
            self.content_types_to_compresses = outs['contentTypesToCompresses']
        if 'geoFilters' in outs:
            self.geo_filters = outs['geoFilters']
        if 'hostName' in outs:
            self.host_name = outs['hostName']
        if 'isCompressionEnabled' in outs:
            self.is_compression_enabled = outs['isCompressionEnabled']
        if 'isHttpAllowed' in outs:
            self.is_http_allowed = outs['isHttpAllowed']
        if 'isHttpsAllowed' in outs:
            self.is_https_allowed = outs['isHttpsAllowed']
        if 'location' in outs:
            self.location = outs['location']
        if 'name' in outs:
            self.name = outs['name']
        if 'optimizationType' in outs:
            self.optimization_type = outs['optimizationType']
        if 'origins' in outs:
            self.origins = outs['origins']
        if 'originHostHeader' in outs:
            self.origin_host_header = outs['originHostHeader']
        if 'originPath' in outs:
            self.origin_path = outs['originPath']
        if 'probePath' in outs:
            self.probe_path = outs['probePath']
        if 'profileName' in outs:
            self.profile_name = outs['profileName']
        if 'querystringCachingBehaviour' in outs:
            self.querystring_caching_behaviour = outs['querystringCachingBehaviour']
        if 'resourceGroupName' in outs:
            self.resource_group_name = outs['resourceGroupName']
        if 'tags' in outs:
            self.tags = outs['tags']
