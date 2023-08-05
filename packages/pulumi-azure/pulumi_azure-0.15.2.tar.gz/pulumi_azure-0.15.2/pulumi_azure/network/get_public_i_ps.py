# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class GetPublicIPsResult(object):
    """
    A collection of values returned by getPublicIPs.
    """
    def __init__(__self__, public_ips=None, id=None):
        if public_ips and not isinstance(public_ips, list):
            raise TypeError('Expected argument public_ips to be a list')
        __self__.public_ips = public_ips
        """
        A List of `public_ips` blocks as defined below filtered by the criteria above.
        """
        if id and not isinstance(id, basestring):
            raise TypeError('Expected argument id to be a basestring')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

def get_public_i_ps(allocation_type=None, attached=None, name_prefix=None, resource_group_name=None):
    """
    Use this data source to access a filtered list of Public IP Addresses
    """
    __args__ = dict()

    __args__['allocationType'] = allocation_type
    __args__['attached'] = attached
    __args__['namePrefix'] = name_prefix
    __args__['resourceGroupName'] = resource_group_name
    __ret__ = pulumi.runtime.invoke('azure:network/getPublicIPs:getPublicIPs', __args__)

    return GetPublicIPsResult(
        public_ips=__ret__.get('publicIps'),
        id=__ret__.get('id'))
