# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class LifecyclePolicy(pulumi.CustomResource):
    """
    Provides an ECR lifecycle policy.
    """
    def __init__(__self__, __name__, __opts__=None, policy=None, repository=None):
        """Create a LifecyclePolicy resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not policy:
            raise TypeError('Missing required property policy')
        elif not isinstance(policy, basestring):
            raise TypeError('Expected property policy to be a basestring')
        __self__.policy = policy
        """
        The policy document. This is a JSON formatted string. See more details about [Policy Parameters](http://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html#lifecycle_policy_parameters) in the official AWS docs.
        """
        __props__['policy'] = policy

        if not repository:
            raise TypeError('Missing required property repository')
        elif not isinstance(repository, basestring):
            raise TypeError('Expected property repository to be a basestring')
        __self__.repository = repository
        """
        Name of the repository to apply the policy.
        """
        __props__['repository'] = repository

        __self__.registry_id = pulumi.runtime.UNKNOWN
        """
        The registry ID where the repository was created.
        """

        super(LifecyclePolicy, __self__).__init__(
            'aws:ecr/lifecyclePolicy:LifecyclePolicy',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'policy' in outs:
            self.policy = outs['policy']
        if 'registryId' in outs:
            self.registry_id = outs['registryId']
        if 'repository' in outs:
            self.repository = outs['repository']
