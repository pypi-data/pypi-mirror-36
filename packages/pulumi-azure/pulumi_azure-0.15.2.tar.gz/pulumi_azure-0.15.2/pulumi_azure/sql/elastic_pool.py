# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class ElasticPool(pulumi.CustomResource):
    """
    Allows you to manage an Azure SQL Elastic Pool.
    """
    def __init__(__self__, __name__, __opts__=None, db_dtu_max=None, db_dtu_min=None, dtu=None, edition=None, location=None, name=None, pool_size=None, resource_group_name=None, server_name=None, tags=None):
        """Create a ElasticPool resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if db_dtu_max and not isinstance(db_dtu_max, int):
            raise TypeError('Expected property db_dtu_max to be a int')
        __self__.db_dtu_max = db_dtu_max
        """
        The maximum DTU which will be guaranteed to all databases in the elastic pool to be created.
        """
        __props__['dbDtuMax'] = db_dtu_max

        if db_dtu_min and not isinstance(db_dtu_min, int):
            raise TypeError('Expected property db_dtu_min to be a int')
        __self__.db_dtu_min = db_dtu_min
        """
        The minimum DTU which will be guaranteed to all databases in the elastic pool to be created.
        """
        __props__['dbDtuMin'] = db_dtu_min

        if not dtu:
            raise TypeError('Missing required property dtu')
        elif not isinstance(dtu, int):
            raise TypeError('Expected property dtu to be a int')
        __self__.dtu = dtu
        """
        The total shared DTU for the elastic pool. Valid values depend on the `edition` which has been defined. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for valid combinations.
        """
        __props__['dtu'] = dtu

        if not edition:
            raise TypeError('Missing required property edition')
        elif not isinstance(edition, basestring):
            raise TypeError('Expected property edition to be a basestring')
        __self__.edition = edition
        """
        The edition of the elastic pool to be created. Valid values are `Basic`, `Standard`, and `Premium`. Refer to [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus) for details. Changing this forces a new resource to be created.
        """
        __props__['edition'] = edition

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
        The name of the elastic pool. This needs to be globally unique. Changing this forces a new resource to be created.
        """
        __props__['name'] = name

        if pool_size and not isinstance(pool_size, int):
            raise TypeError('Expected property pool_size to be a int')
        __self__.pool_size = pool_size
        """
        The maximum size in MB that all databases in the elastic pool can grow to. The maximum size must be consistent with combination of `edition` and `dtu` and the limits documented in [Azure SQL Database Service Tiers](https://docs.microsoft.com/en-gb/azure/sql-database/sql-database-service-tiers#elastic-pool-service-tiers-and-performance-in-edtus). If not defined when creating an elastic pool, the value is set to the size implied by `edition` and `dtu`.
        """
        __props__['poolSize'] = pool_size

        if not resource_group_name:
            raise TypeError('Missing required property resource_group_name')
        elif not isinstance(resource_group_name, basestring):
            raise TypeError('Expected property resource_group_name to be a basestring')
        __self__.resource_group_name = resource_group_name
        """
        The name of the resource group in which to create the elastic pool. This must be the same as the resource group of the underlying SQL server.
        """
        __props__['resourceGroupName'] = resource_group_name

        if not server_name:
            raise TypeError('Missing required property server_name')
        elif not isinstance(server_name, basestring):
            raise TypeError('Expected property server_name to be a basestring')
        __self__.server_name = server_name
        """
        The name of the SQL Server on which to create the elastic pool. Changing this forces a new resource to be created.
        """
        __props__['serverName'] = server_name

        if tags and not isinstance(tags, dict):
            raise TypeError('Expected property tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags to assign to the resource.
        """
        __props__['tags'] = tags

        __self__.creation_date = pulumi.runtime.UNKNOWN
        """
        The creation date of the SQL Elastic Pool.
        """

        super(ElasticPool, __self__).__init__(
            'azure:sql/elasticPool:ElasticPool',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'creationDate' in outs:
            self.creation_date = outs['creationDate']
        if 'dbDtuMax' in outs:
            self.db_dtu_max = outs['dbDtuMax']
        if 'dbDtuMin' in outs:
            self.db_dtu_min = outs['dbDtuMin']
        if 'dtu' in outs:
            self.dtu = outs['dtu']
        if 'edition' in outs:
            self.edition = outs['edition']
        if 'location' in outs:
            self.location = outs['location']
        if 'name' in outs:
            self.name = outs['name']
        if 'poolSize' in outs:
            self.pool_size = outs['poolSize']
        if 'resourceGroupName' in outs:
            self.resource_group_name = outs['resourceGroupName']
        if 'serverName' in outs:
            self.server_name = outs['serverName']
        if 'tags' in outs:
            self.tags = outs['tags']
