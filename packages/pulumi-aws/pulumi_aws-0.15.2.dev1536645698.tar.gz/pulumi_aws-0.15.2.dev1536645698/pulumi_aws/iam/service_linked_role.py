# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class ServiceLinkedRole(pulumi.CustomResource):
    """
    Provides an [IAM service-linked role](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html).
    """
    def __init__(__self__, __name__, __opts__=None, aws_service_name=None, custom_suffix=None, description=None):
        """Create a ServiceLinkedRole resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not aws_service_name:
            raise TypeError('Missing required property aws_service_name')
        elif not isinstance(aws_service_name, basestring):
            raise TypeError('Expected property aws_service_name to be a basestring')
        __self__.aws_service_name = aws_service_name
        """
        The AWS service to which this role is attached. You use a string similar to a URL but without the `http://` in front. For example: `elasticbeanstalk.amazonaws.com`. To find the full list of services that support service-linked roles, check [the docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html).
        """
        __props__['awsServiceName'] = aws_service_name

        if custom_suffix and not isinstance(custom_suffix, basestring):
            raise TypeError('Expected property custom_suffix to be a basestring')
        __self__.custom_suffix = custom_suffix
        """
        Additional string appended to the role name. Not all AWS services support custom suffixes.
        """
        __props__['customSuffix'] = custom_suffix

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        """
        The description of the role.
        """
        __props__['description'] = description

        __self__.arn = pulumi.runtime.UNKNOWN
        """
        The Amazon Resource Name (ARN) specifying the role.
        """
        __self__.create_date = pulumi.runtime.UNKNOWN
        """
        The creation date of the IAM role.
        """
        __self__.name = pulumi.runtime.UNKNOWN
        """
        The name of the role.
        """
        __self__.path = pulumi.runtime.UNKNOWN
        """
        The path of the role.
        """
        __self__.unique_id = pulumi.runtime.UNKNOWN
        """
        The stable and unique string identifying the role.
        """

        super(ServiceLinkedRole, __self__).__init__(
            'aws:iam/serviceLinkedRole:ServiceLinkedRole',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'arn' in outs:
            self.arn = outs['arn']
        if 'awsServiceName' in outs:
            self.aws_service_name = outs['awsServiceName']
        if 'createDate' in outs:
            self.create_date = outs['createDate']
        if 'customSuffix' in outs:
            self.custom_suffix = outs['customSuffix']
        if 'description' in outs:
            self.description = outs['description']
        if 'name' in outs:
            self.name = outs['name']
        if 'path' in outs:
            self.path = outs['path']
        if 'uniqueId' in outs:
            self.unique_id = outs['uniqueId']
