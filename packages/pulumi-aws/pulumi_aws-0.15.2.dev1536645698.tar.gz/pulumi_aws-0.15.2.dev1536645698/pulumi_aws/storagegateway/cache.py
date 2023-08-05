# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Cache(pulumi.CustomResource):
    """
    Manages an AWS Storage Gateway cache.
    
    ~> **NOTE:** The Storage Gateway API provides no method to remove a cache disk. Destroying this Terraform resource does not perform any Storage Gateway actions.
    """
    def __init__(__self__, __name__, __opts__=None, disk_id=None, gateway_arn=None):
        """Create a Cache resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not disk_id:
            raise TypeError('Missing required property disk_id')
        elif not isinstance(disk_id, basestring):
            raise TypeError('Expected property disk_id to be a basestring')
        __self__.disk_id = disk_id
        """
        Local disk identifier. For example, `pci-0000:03:00.0-scsi-0:0:0:0`.
        """
        __props__['diskId'] = disk_id

        if not gateway_arn:
            raise TypeError('Missing required property gateway_arn')
        elif not isinstance(gateway_arn, basestring):
            raise TypeError('Expected property gateway_arn to be a basestring')
        __self__.gateway_arn = gateway_arn
        """
        The Amazon Resource Name (ARN) of the gateway.
        """
        __props__['gatewayArn'] = gateway_arn

        super(Cache, __self__).__init__(
            'aws:storagegateway/cache:Cache',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'diskId' in outs:
            self.disk_id = outs['diskId']
        if 'gatewayArn' in outs:
            self.gateway_arn = outs['gatewayArn']
