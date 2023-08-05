# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Notification(pulumi.CustomResource):
    """
    Provides an AutoScaling Group with Notification support, via SNS Topics. Each of
    the `notifications` map to a [Notification Configuration][2] inside Amazon Web
    Services, and are applied to each AutoScaling Group you supply.
    """
    def __init__(__self__, __name__, __opts__=None, group_names=None, notifications=None, topic_arn=None):
        """Create a Notification resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not group_names:
            raise TypeError('Missing required property group_names')
        elif not isinstance(group_names, list):
            raise TypeError('Expected property group_names to be a list')
        __self__.group_names = group_names
        """
        A list of AutoScaling Group Names
        """
        __props__['groupNames'] = group_names

        if not notifications:
            raise TypeError('Missing required property notifications')
        elif not isinstance(notifications, list):
            raise TypeError('Expected property notifications to be a list')
        __self__.notifications = notifications
        """
        A list of Notification Types that trigger
        notifications. Acceptable values are documented [in the AWS documentation here][1]
        """
        __props__['notifications'] = notifications

        if not topic_arn:
            raise TypeError('Missing required property topic_arn')
        elif not isinstance(topic_arn, basestring):
            raise TypeError('Expected property topic_arn to be a basestring')
        __self__.topic_arn = topic_arn
        """
        The Topic ARN for notifications to be sent through
        """
        __props__['topicArn'] = topic_arn

        super(Notification, __self__).__init__(
            'aws:autoscaling/notification:Notification',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'groupNames' in outs:
            self.group_names = outs['groupNames']
        if 'notifications' in outs:
            self.notifications = outs['notifications']
        if 'topicArn' in outs:
            self.topic_arn = outs['topicArn']
