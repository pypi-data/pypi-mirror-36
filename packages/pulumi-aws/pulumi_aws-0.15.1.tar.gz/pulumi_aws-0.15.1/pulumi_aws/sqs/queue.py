# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Queue(pulumi.CustomResource):
    def __init__(__self__, __name__, __opts__=None, content_based_deduplication=None, delay_seconds=None, fifo_queue=None, kms_data_key_reuse_period_seconds=None, kms_master_key_id=None, max_message_size=None, message_retention_seconds=None, name=None, name_prefix=None, policy=None, receive_wait_time_seconds=None, redrive_policy=None, tags=None, visibility_timeout_seconds=None):
        """Create a Queue resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if content_based_deduplication and not isinstance(content_based_deduplication, bool):
            raise TypeError('Expected property content_based_deduplication to be a bool')
        __self__.content_based_deduplication = content_based_deduplication
        """
        Enables content-based deduplication for FIFO queues. For more information, see the [related documentation](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html#FIFO-queues-exactly-once-processing)
        """
        __props__['contentBasedDeduplication'] = content_based_deduplication

        if delay_seconds and not isinstance(delay_seconds, int):
            raise TypeError('Expected property delay_seconds to be a int')
        __self__.delay_seconds = delay_seconds
        """
        The time in seconds that the delivery of all messages in the queue will be delayed. An integer from 0 to 900 (15 minutes). The default for this attribute is 0 seconds.
        """
        __props__['delaySeconds'] = delay_seconds

        if fifo_queue and not isinstance(fifo_queue, bool):
            raise TypeError('Expected property fifo_queue to be a bool')
        __self__.fifo_queue = fifo_queue
        """
        Boolean designating a FIFO queue. If not set, it defaults to `false` making it standard.
        """
        __props__['fifoQueue'] = fifo_queue

        if kms_data_key_reuse_period_seconds and not isinstance(kms_data_key_reuse_period_seconds, int):
            raise TypeError('Expected property kms_data_key_reuse_period_seconds to be a int')
        __self__.kms_data_key_reuse_period_seconds = kms_data_key_reuse_period_seconds
        """
        The length of time, in seconds, for which Amazon SQS can reuse a data key to encrypt or decrypt messages before calling AWS KMS again. An integer representing seconds, between 60 seconds (1 minute) and 86,400 seconds (24 hours). The default is 300 (5 minutes).
        """
        __props__['kmsDataKeyReusePeriodSeconds'] = kms_data_key_reuse_period_seconds

        if kms_master_key_id and not isinstance(kms_master_key_id, basestring):
            raise TypeError('Expected property kms_master_key_id to be a basestring')
        __self__.kms_master_key_id = kms_master_key_id
        """
        The ID of an AWS-managed customer master key (CMK) for Amazon SQS or a custom CMK. For more information, see [Key Terms](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html#sqs-sse-key-terms).
        """
        __props__['kmsMasterKeyId'] = kms_master_key_id

        if max_message_size and not isinstance(max_message_size, int):
            raise TypeError('Expected property max_message_size to be a int')
        __self__.max_message_size = max_message_size
        """
        The limit of how many bytes a message can contain before Amazon SQS rejects it. An integer from 1024 bytes (1 KiB) up to 262144 bytes (256 KiB). The default for this attribute is 262144 (256 KiB).
        """
        __props__['maxMessageSize'] = max_message_size

        if message_retention_seconds and not isinstance(message_retention_seconds, int):
            raise TypeError('Expected property message_retention_seconds to be a int')
        __self__.message_retention_seconds = message_retention_seconds
        """
        The number of seconds Amazon SQS retains a message. Integer representing seconds, from 60 (1 minute) to 1209600 (14 days). The default for this attribute is 345600 (4 days).
        """
        __props__['messageRetentionSeconds'] = message_retention_seconds

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        This is the human-readable name of the queue. If omitted, Terraform will assign a random name.
        """
        __props__['name'] = name

        if name_prefix and not isinstance(name_prefix, basestring):
            raise TypeError('Expected property name_prefix to be a basestring')
        __self__.name_prefix = name_prefix
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        __props__['namePrefix'] = name_prefix

        if policy and not isinstance(policy, basestring):
            raise TypeError('Expected property policy to be a basestring')
        __self__.policy = policy
        """
        The JSON policy for the SQS queue
        """
        __props__['policy'] = policy

        if receive_wait_time_seconds and not isinstance(receive_wait_time_seconds, int):
            raise TypeError('Expected property receive_wait_time_seconds to be a int')
        __self__.receive_wait_time_seconds = receive_wait_time_seconds
        """
        The time for which a ReceiveMessage call will wait for a message to arrive (long polling) before returning. An integer from 0 to 20 (seconds). The default for this attribute is 0, meaning that the call will return immediately.
        """
        __props__['receiveWaitTimeSeconds'] = receive_wait_time_seconds

        if redrive_policy and not isinstance(redrive_policy, basestring):
            raise TypeError('Expected property redrive_policy to be a basestring')
        __self__.redrive_policy = redrive_policy
        """
        The JSON policy to set up the Dead Letter Queue, see [AWS docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/SQSDeadLetterQueue.html). **Note:** when specifying `maxReceiveCount`, you must specify it as an integer (`5`), and not a string (`"5"`).
        """
        __props__['redrivePolicy'] = redrive_policy

        if tags and not isinstance(tags, dict):
            raise TypeError('Expected property tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags to assign to the queue.
        """
        __props__['tags'] = tags

        if visibility_timeout_seconds and not isinstance(visibility_timeout_seconds, int):
            raise TypeError('Expected property visibility_timeout_seconds to be a int')
        __self__.visibility_timeout_seconds = visibility_timeout_seconds
        """
        The visibility timeout for the queue. An integer from 0 to 43200 (12 hours). The default for this attribute is 30. For more information about visibility timeout, see [AWS docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html).
        """
        __props__['visibilityTimeoutSeconds'] = visibility_timeout_seconds

        __self__.arn = pulumi.runtime.UNKNOWN
        """
        The ARN of the SQS queue
        """

        super(Queue, __self__).__init__(
            'aws:sqs/queue:Queue',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'arn' in outs:
            self.arn = outs['arn']
        if 'contentBasedDeduplication' in outs:
            self.content_based_deduplication = outs['contentBasedDeduplication']
        if 'delaySeconds' in outs:
            self.delay_seconds = outs['delaySeconds']
        if 'fifoQueue' in outs:
            self.fifo_queue = outs['fifoQueue']
        if 'kmsDataKeyReusePeriodSeconds' in outs:
            self.kms_data_key_reuse_period_seconds = outs['kmsDataKeyReusePeriodSeconds']
        if 'kmsMasterKeyId' in outs:
            self.kms_master_key_id = outs['kmsMasterKeyId']
        if 'maxMessageSize' in outs:
            self.max_message_size = outs['maxMessageSize']
        if 'messageRetentionSeconds' in outs:
            self.message_retention_seconds = outs['messageRetentionSeconds']
        if 'name' in outs:
            self.name = outs['name']
        if 'namePrefix' in outs:
            self.name_prefix = outs['namePrefix']
        if 'policy' in outs:
            self.policy = outs['policy']
        if 'receiveWaitTimeSeconds' in outs:
            self.receive_wait_time_seconds = outs['receiveWaitTimeSeconds']
        if 'redrivePolicy' in outs:
            self.redrive_policy = outs['redrivePolicy']
        if 'tags' in outs:
            self.tags = outs['tags']
        if 'visibilityTimeoutSeconds' in outs:
            self.visibility_timeout_seconds = outs['visibilityTimeoutSeconds']
