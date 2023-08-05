# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class PacketCapture(pulumi.CustomResource):
    """
    Configures Packet Capturing against a Virtual Machine using a Network Watcher.
    """
    def __init__(__self__, __name__, __opts__=None, filters=None, maximum_bytes_per_packet=None, maximum_bytes_per_session=None, maximum_capture_duration=None, name=None, network_watcher_name=None, resource_group_name=None, storage_location=None, target_resource_id=None):
        """Create a PacketCapture resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if filters and not isinstance(filters, list):
            raise TypeError('Expected property filters to be a list')
        __self__.filters = filters
        """
        One or more `filter` blocks as defined below. Changing this forces a new resource to be created.
        """
        __props__['filters'] = filters

        if maximum_bytes_per_packet and not isinstance(maximum_bytes_per_packet, int):
            raise TypeError('Expected property maximum_bytes_per_packet to be a int')
        __self__.maximum_bytes_per_packet = maximum_bytes_per_packet
        """
        The number of bytes captured per packet. The remaining bytes are truncated. Defaults to `0` (Entire Packet Captured). Changing this forces a new resource to be created.
        """
        __props__['maximumBytesPerPacket'] = maximum_bytes_per_packet

        if maximum_bytes_per_session and not isinstance(maximum_bytes_per_session, int):
            raise TypeError('Expected property maximum_bytes_per_session to be a int')
        __self__.maximum_bytes_per_session = maximum_bytes_per_session
        """
        Maximum size of the capture in Bytes. Defaults to `1073741824` (1GB). Changing this forces a new resource to be created.
        """
        __props__['maximumBytesPerSession'] = maximum_bytes_per_session

        if maximum_capture_duration and not isinstance(maximum_capture_duration, int):
            raise TypeError('Expected property maximum_capture_duration to be a int')
        __self__.maximum_capture_duration = maximum_capture_duration
        """
        The maximum duration of the capture session in seconds. Defaults to `18000` (5 hours). Changing this forces a new resource to be created.
        """
        __props__['maximumCaptureDuration'] = maximum_capture_duration

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        The name to use for this Packet Capture. Changing this forces a new resource to be created.
        """
        __props__['name'] = name

        if not network_watcher_name:
            raise TypeError('Missing required property network_watcher_name')
        elif not isinstance(network_watcher_name, basestring):
            raise TypeError('Expected property network_watcher_name to be a basestring')
        __self__.network_watcher_name = network_watcher_name
        """
        The name of the Network Watcher. Changing this forces a new resource to be created.
        """
        __props__['networkWatcherName'] = network_watcher_name

        if not resource_group_name:
            raise TypeError('Missing required property resource_group_name')
        elif not isinstance(resource_group_name, basestring):
            raise TypeError('Expected property resource_group_name to be a basestring')
        __self__.resource_group_name = resource_group_name
        """
        The name of the resource group in which the Network Watcher exists. Changing this forces a new resource to be created.
        """
        __props__['resourceGroupName'] = resource_group_name

        if not storage_location:
            raise TypeError('Missing required property storage_location')
        elif not isinstance(storage_location, dict):
            raise TypeError('Expected property storage_location to be a dict')
        __self__.storage_location = storage_location
        """
        A `storage_location` block as defined below. Changing this forces a new resource to be created.
        """
        __props__['storageLocation'] = storage_location

        if not target_resource_id:
            raise TypeError('Missing required property target_resource_id')
        elif not isinstance(target_resource_id, basestring):
            raise TypeError('Expected property target_resource_id to be a basestring')
        __self__.target_resource_id = target_resource_id
        """
        The ID of the Resource to capture packets from. Changing this forces a new resource to be created.
        """
        __props__['targetResourceId'] = target_resource_id

        super(PacketCapture, __self__).__init__(
            'azure:network/packetCapture:PacketCapture',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'filters' in outs:
            self.filters = outs['filters']
        if 'maximumBytesPerPacket' in outs:
            self.maximum_bytes_per_packet = outs['maximumBytesPerPacket']
        if 'maximumBytesPerSession' in outs:
            self.maximum_bytes_per_session = outs['maximumBytesPerSession']
        if 'maximumCaptureDuration' in outs:
            self.maximum_capture_duration = outs['maximumCaptureDuration']
        if 'name' in outs:
            self.name = outs['name']
        if 'networkWatcherName' in outs:
            self.network_watcher_name = outs['networkWatcherName']
        if 'resourceGroupName' in outs:
            self.resource_group_name = outs['resourceGroupName']
        if 'storageLocation' in outs:
            self.storage_location = outs['storageLocation']
        if 'targetResourceId' in outs:
            self.target_resource_id = outs['targetResourceId']
