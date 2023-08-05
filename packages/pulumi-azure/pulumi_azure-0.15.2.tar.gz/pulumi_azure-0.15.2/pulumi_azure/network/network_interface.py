# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class NetworkInterface(pulumi.CustomResource):
    """
    Manages a Network Interface located in a Virtual Network, usually attached to a Virtual Machine.
    """
    def __init__(__self__, __name__, __opts__=None, applied_dns_servers=None, dns_servers=None, enable_accelerated_networking=None, enable_ip_forwarding=None, internal_dns_name_label=None, internal_fqdn=None, ip_configurations=None, location=None, mac_address=None, name=None, network_security_group_id=None, resource_group_name=None, tags=None, virtual_machine_id=None):
        """Create a NetworkInterface resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if applied_dns_servers and not isinstance(applied_dns_servers, list):
            raise TypeError('Expected property applied_dns_servers to be a list')
        __self__.applied_dns_servers = applied_dns_servers
        """
        If the VM that uses this NIC is part of an Availability Set, then this list will have the union of all DNS servers from all NICs that are part of the Availability Set
        """
        __props__['appliedDnsServers'] = applied_dns_servers

        if dns_servers and not isinstance(dns_servers, list):
            raise TypeError('Expected property dns_servers to be a list')
        __self__.dns_servers = dns_servers
        """
        List of DNS servers IP addresses to use for this NIC, overrides the VNet-level server list
        """
        __props__['dnsServers'] = dns_servers

        if enable_accelerated_networking and not isinstance(enable_accelerated_networking, bool):
            raise TypeError('Expected property enable_accelerated_networking to be a bool')
        __self__.enable_accelerated_networking = enable_accelerated_networking
        """
        Enables Azure Accelerated Networking using SR-IOV. Only certain VM instance sizes are supported. Refer to [Create a Virtual Machine with Accelerated Networking](https://docs.microsoft.com/en-us/azure/virtual-network/create-vm-accelerated-networking-cli). Defaults to `false`.
        """
        __props__['enableAcceleratedNetworking'] = enable_accelerated_networking

        if enable_ip_forwarding and not isinstance(enable_ip_forwarding, bool):
            raise TypeError('Expected property enable_ip_forwarding to be a bool')
        __self__.enable_ip_forwarding = enable_ip_forwarding
        """
        Enables IP Forwarding on the NIC. Defaults to `false`.
        """
        __props__['enableIpForwarding'] = enable_ip_forwarding

        if internal_dns_name_label and not isinstance(internal_dns_name_label, basestring):
            raise TypeError('Expected property internal_dns_name_label to be a basestring')
        __self__.internal_dns_name_label = internal_dns_name_label
        """
        Relative DNS name for this NIC used for internal communications between VMs in the same VNet
        """
        __props__['internalDnsNameLabel'] = internal_dns_name_label

        if internal_fqdn and not isinstance(internal_fqdn, basestring):
            raise TypeError('Expected property internal_fqdn to be a basestring')
        __self__.internal_fqdn = internal_fqdn
        """
        Fully qualified DNS name supporting internal communications between VMs in the same VNet
        """
        __props__['internalFqdn'] = internal_fqdn

        if not ip_configurations:
            raise TypeError('Missing required property ip_configurations')
        elif not isinstance(ip_configurations, list):
            raise TypeError('Expected property ip_configurations to be a list')
        __self__.ip_configurations = ip_configurations
        """
        One or more `ip_configuration` associated with this NIC as documented below.
        """
        __props__['ipConfigurations'] = ip_configurations

        if not location:
            raise TypeError('Missing required property location')
        elif not isinstance(location, basestring):
            raise TypeError('Expected property location to be a basestring')
        __self__.location = location
        """
        The location/region where the network interface is created. Changing this forces a new resource to be created.
        """
        __props__['location'] = location

        if mac_address and not isinstance(mac_address, basestring):
            raise TypeError('Expected property mac_address to be a basestring')
        __self__.mac_address = mac_address
        """
        The media access control (MAC) address of the network interface.
        """
        __props__['macAddress'] = mac_address

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        The name of the network interface. Changing this forces a new resource to be created.
        """
        __props__['name'] = name

        if network_security_group_id and not isinstance(network_security_group_id, basestring):
            raise TypeError('Expected property network_security_group_id to be a basestring')
        __self__.network_security_group_id = network_security_group_id
        """
        The ID of the Network Security Group to associate with the network interface.
        """
        __props__['networkSecurityGroupId'] = network_security_group_id

        if not resource_group_name:
            raise TypeError('Missing required property resource_group_name')
        elif not isinstance(resource_group_name, basestring):
            raise TypeError('Expected property resource_group_name to be a basestring')
        __self__.resource_group_name = resource_group_name
        """
        The name of the resource group in which to create the network interface. Changing this forces a new resource to be created.
        """
        __props__['resourceGroupName'] = resource_group_name

        if tags and not isinstance(tags, dict):
            raise TypeError('Expected property tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags to assign to the resource.
        """
        __props__['tags'] = tags

        if virtual_machine_id and not isinstance(virtual_machine_id, basestring):
            raise TypeError('Expected property virtual_machine_id to be a basestring')
        __self__.virtual_machine_id = virtual_machine_id
        """
        Reference to a VM with which this NIC has been associated.
        """
        __props__['virtualMachineId'] = virtual_machine_id

        __self__.private_ip_address = pulumi.runtime.UNKNOWN
        """
        The private ip address of the network interface.
        """
        __self__.private_ip_addresses = pulumi.runtime.UNKNOWN

        super(NetworkInterface, __self__).__init__(
            'azure:network/networkInterface:NetworkInterface',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'appliedDnsServers' in outs:
            self.applied_dns_servers = outs['appliedDnsServers']
        if 'dnsServers' in outs:
            self.dns_servers = outs['dnsServers']
        if 'enableAcceleratedNetworking' in outs:
            self.enable_accelerated_networking = outs['enableAcceleratedNetworking']
        if 'enableIpForwarding' in outs:
            self.enable_ip_forwarding = outs['enableIpForwarding']
        if 'internalDnsNameLabel' in outs:
            self.internal_dns_name_label = outs['internalDnsNameLabel']
        if 'internalFqdn' in outs:
            self.internal_fqdn = outs['internalFqdn']
        if 'ipConfigurations' in outs:
            self.ip_configurations = outs['ipConfigurations']
        if 'location' in outs:
            self.location = outs['location']
        if 'macAddress' in outs:
            self.mac_address = outs['macAddress']
        if 'name' in outs:
            self.name = outs['name']
        if 'networkSecurityGroupId' in outs:
            self.network_security_group_id = outs['networkSecurityGroupId']
        if 'privateIpAddress' in outs:
            self.private_ip_address = outs['privateIpAddress']
        if 'privateIpAddresses' in outs:
            self.private_ip_addresses = outs['privateIpAddresses']
        if 'resourceGroupName' in outs:
            self.resource_group_name = outs['resourceGroupName']
        if 'tags' in outs:
            self.tags = outs['tags']
        if 'virtualMachineId' in outs:
            self.virtual_machine_id = outs['virtualMachineId']
