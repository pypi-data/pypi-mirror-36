# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class LinkAggregationGroup(pulumi.CustomResource):
    """
    Provides a Direct Connect LAG.
    """
    def __init__(__self__, __name__, __opts__=None, connections_bandwidth=None, force_destroy=None, location=None, name=None, number_of_connections=None, tags=None):
        """Create a LinkAggregationGroup resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not connections_bandwidth:
            raise TypeError('Missing required property connections_bandwidth')
        elif not isinstance(connections_bandwidth, basestring):
            raise TypeError('Expected property connections_bandwidth to be a basestring')
        __self__.connections_bandwidth = connections_bandwidth
        """
        The bandwidth of the individual physical connections bundled by the LAG. Available values: 1Gbps, 10Gbps. Case sensitive.
        """
        __props__['connectionsBandwidth'] = connections_bandwidth

        if force_destroy and not isinstance(force_destroy, bool):
            raise TypeError('Expected property force_destroy to be a bool')
        __self__.force_destroy = force_destroy
        """
        A boolean that indicates all connections associated with the LAG should be deleted so that the LAG can be destroyed without error. These objects are *not* recoverable.
        """
        __props__['forceDestroy'] = force_destroy

        if not location:
            raise TypeError('Missing required property location')
        elif not isinstance(location, basestring):
            raise TypeError('Expected property location to be a basestring')
        __self__.location = location
        """
        The AWS Direct Connect location in which the LAG should be allocated. See [DescribeLocations](https://docs.aws.amazon.com/directconnect/latest/APIReference/API_DescribeLocations.html) for the list of AWS Direct Connect locations. Use `locationCode`.
        """
        __props__['location'] = location

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        The name of the LAG.
        """
        __props__['name'] = name

        if number_of_connections and not isinstance(number_of_connections, int):
            raise TypeError('Expected property number_of_connections to be a int')
        __self__.number_of_connections = number_of_connections
        """
        The number of physical connections initially provisioned and bundled by the LAG. Use `aws_dx_connection` and `aws_dx_connection_association` resources instead. Default connections will be removed as part of LAG creation automatically in future versions.
        """
        __props__['numberOfConnections'] = number_of_connections

        if tags and not isinstance(tags, dict):
            raise TypeError('Expected property tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags to assign to the resource.
        """
        __props__['tags'] = tags

        __self__.arn = pulumi.runtime.UNKNOWN
        """
        The ARN of the LAG.
        """

        super(LinkAggregationGroup, __self__).__init__(
            'aws:directconnect/linkAggregationGroup:LinkAggregationGroup',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'arn' in outs:
            self.arn = outs['arn']
        if 'connectionsBandwidth' in outs:
            self.connections_bandwidth = outs['connectionsBandwidth']
        if 'forceDestroy' in outs:
            self.force_destroy = outs['forceDestroy']
        if 'location' in outs:
            self.location = outs['location']
        if 'name' in outs:
            self.name = outs['name']
        if 'numberOfConnections' in outs:
            self.number_of_connections = outs['numberOfConnections']
        if 'tags' in outs:
            self.tags = outs['tags']
