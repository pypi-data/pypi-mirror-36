# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class TopicSubscription(pulumi.CustomResource):
    """
      Provides a resource for subscribing to SNS topics. Requires that an SNS topic exist for the subscription to attach to.
    This resource allows you to automatically place messages sent to SNS topics in SQS queues, send them as HTTP(S) POST requests
    to a given endpoint, send SMS messages, or notify devices / applications. The most likely use case for Terraform users will
    probably be SQS queues.
    
    ~> **NOTE:** If the SNS topic and SQS queue are in different AWS regions, it is important for the "aws_sns_topic_subscription" to use an AWS provider that is in the same region of the SNS topic. If the "aws_sns_topic_subscription" is using a provider with a different region than the SNS topic, terraform will fail to create the subscription.
    
    ~> **NOTE:** Setup of cross-account subscriptions from SNS topics to SQS queues requires Terraform to have access to BOTH accounts.
    
    ~> **NOTE:** If SNS topic and SQS queue are in different AWS accounts but the same region it is important for the "aws_sns_topic_subscription" to use the AWS provider of the account with the SQS queue. If "aws_sns_topic_subscription" is using a Provider with a different account than the SNS topic, terraform creates the subscriptions but does not keep state and tries to re-create the subscription at every apply.
    
    ~> **NOTE:** If SNS topic and SQS queue are in different AWS accounts and different AWS regions it is important to recognize that the subscription needs to be initiated from the account with the SQS queue but in the region of the SNS topic.
    """
    def __init__(__self__, __name__, __opts__=None, confirmation_timeout_in_minutes=None, delivery_policy=None, endpoint=None, endpoint_auto_confirms=None, filter_policy=None, protocol=None, raw_message_delivery=None, topic=None):
        """Create a TopicSubscription resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if confirmation_timeout_in_minutes and not isinstance(confirmation_timeout_in_minutes, int):
            raise TypeError('Expected property confirmation_timeout_in_minutes to be a int')
        __self__.confirmation_timeout_in_minutes = confirmation_timeout_in_minutes
        """
        Integer indicating number of minutes to wait in retying mode for fetching subscription arn before marking it as failure. Only applicable for http and https protocols (default is 1 minute).
        """
        __props__['confirmationTimeoutInMinutes'] = confirmation_timeout_in_minutes

        if delivery_policy and not isinstance(delivery_policy, basestring):
            raise TypeError('Expected property delivery_policy to be a basestring')
        __self__.delivery_policy = delivery_policy
        __props__['deliveryPolicy'] = delivery_policy

        if not endpoint:
            raise TypeError('Missing required property endpoint')
        elif not isinstance(endpoint, basestring):
            raise TypeError('Expected property endpoint to be a basestring')
        __self__.endpoint = endpoint
        """
        The endpoint to send data to, the contents will vary with the protocol. (see below for more information)
        """
        __props__['endpoint'] = endpoint

        if endpoint_auto_confirms and not isinstance(endpoint_auto_confirms, bool):
            raise TypeError('Expected property endpoint_auto_confirms to be a bool')
        __self__.endpoint_auto_confirms = endpoint_auto_confirms
        """
        Boolean indicating whether the end point is capable of [auto confirming subscription](http://docs.aws.amazon.com/sns/latest/dg/SendMessageToHttp.html#SendMessageToHttp.prepare) e.g., PagerDuty (default is false)
        """
        __props__['endpointAutoConfirms'] = endpoint_auto_confirms

        if filter_policy and not isinstance(filter_policy, basestring):
            raise TypeError('Expected property filter_policy to be a basestring')
        __self__.filter_policy = filter_policy
        """
        The text of a filter policy to the topic subscription.
        """
        __props__['filterPolicy'] = filter_policy

        if not protocol:
            raise TypeError('Missing required property protocol')
        elif not isinstance(protocol, basestring):
            raise TypeError('Expected property protocol to be a basestring')
        __self__.protocol = protocol
        """
        The protocol to use. The possible values for this are: `sqs`, `sms`, `lambda`, `application`. (`http` or `https` are partially supported, see below) (`email` is option but unsupported, see below).
        """
        __props__['protocol'] = protocol

        if raw_message_delivery and not isinstance(raw_message_delivery, bool):
            raise TypeError('Expected property raw_message_delivery to be a bool')
        __self__.raw_message_delivery = raw_message_delivery
        """
        Boolean indicating whether or not to enable raw message delivery (the original message is directly passed, not wrapped in JSON with the original message in the message property) (default is false).
        """
        __props__['rawMessageDelivery'] = raw_message_delivery

        if not topic:
            raise TypeError('Missing required property topic')
        elif not isinstance(topic, basestring):
            raise TypeError('Expected property topic to be a basestring')
        __self__.topic = topic
        """
        The ARN of the SNS topic to subscribe to
        """
        __props__['topic'] = topic

        __self__.arn = pulumi.runtime.UNKNOWN
        """
        The ARN of the subscription stored as a more user-friendly property
        """

        super(TopicSubscription, __self__).__init__(
            'aws:sns/topicSubscription:TopicSubscription',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'arn' in outs:
            self.arn = outs['arn']
        if 'confirmationTimeoutInMinutes' in outs:
            self.confirmation_timeout_in_minutes = outs['confirmationTimeoutInMinutes']
        if 'deliveryPolicy' in outs:
            self.delivery_policy = outs['deliveryPolicy']
        if 'endpoint' in outs:
            self.endpoint = outs['endpoint']
        if 'endpointAutoConfirms' in outs:
            self.endpoint_auto_confirms = outs['endpointAutoConfirms']
        if 'filterPolicy' in outs:
            self.filter_policy = outs['filterPolicy']
        if 'protocol' in outs:
            self.protocol = outs['protocol']
        if 'rawMessageDelivery' in outs:
            self.raw_message_delivery = outs['rawMessageDelivery']
        if 'topic' in outs:
            self.topic = outs['topic']
