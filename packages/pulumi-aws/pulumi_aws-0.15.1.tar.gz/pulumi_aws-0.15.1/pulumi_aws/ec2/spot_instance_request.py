# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class SpotInstanceRequest(pulumi.CustomResource):
    """
    Provides an EC2 Spot Instance Request resource. This allows instances to be
    requested on the spot market.
    
    By default Terraform creates Spot Instance Requests with a `persistent` type,
    which means that for the duration of their lifetime, AWS will launch an
    instance with the configured details if and when the spot market will accept
    the requested price.
    
    On destruction, Terraform will make an attempt to terminate the associated Spot
    Instance if there is one present.
    
    Spot Instances requests with a `one-time` type will close the spot request
    when the instance is terminated either by the request being below the current spot
    price availability or by a user.
    
    ~> **NOTE:** Because their behavior depends on the live status of the spot
    market, Spot Instance Requests have a unique lifecycle that makes them behave
    differently than other Terraform resources. Most importantly: there is __no
    guarantee__ that a Spot Instance exists to fulfill the request at any given
    point in time. See the [AWS Spot Instance
    documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html)
    for more information.
    
    """
    def __init__(__self__, __name__, __opts__=None, ami=None, associate_public_ip_address=None, availability_zone=None, block_duration_minutes=None, cpu_core_count=None, cpu_threads_per_core=None, credit_specification=None, disable_api_termination=None, ebs_block_devices=None, ebs_optimized=None, ephemeral_block_devices=None, get_password_data=None, iam_instance_profile=None, instance_initiated_shutdown_behavior=None, instance_interruption_behaviour=None, instance_type=None, ipv6_address_count=None, ipv6_addresses=None, key_name=None, launch_group=None, monitoring=None, network_interfaces=None, placement_group=None, private_ip=None, root_block_device=None, security_groups=None, source_dest_check=None, spot_price=None, spot_type=None, subnet_id=None, tags=None, tenancy=None, user_data=None, user_data_base64=None, valid_from=None, valid_until=None, volume_tags=None, vpc_security_group_ids=None, wait_for_fulfillment=None):
        """Create a SpotInstanceRequest resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not ami:
            raise TypeError('Missing required property ami')
        elif not isinstance(ami, basestring):
            raise TypeError('Expected property ami to be a basestring')
        __self__.ami = ami
        """
        The AMI to use for the instance.
        """
        __props__['ami'] = ami

        if associate_public_ip_address and not isinstance(associate_public_ip_address, bool):
            raise TypeError('Expected property associate_public_ip_address to be a bool')
        __self__.associate_public_ip_address = associate_public_ip_address
        """
        Associate a public ip address with an instance in a VPC.  Boolean value.
        """
        __props__['associatePublicIpAddress'] = associate_public_ip_address

        if availability_zone and not isinstance(availability_zone, basestring):
            raise TypeError('Expected property availability_zone to be a basestring')
        __self__.availability_zone = availability_zone
        """
        The AZ to start the instance in.
        """
        __props__['availabilityZone'] = availability_zone

        if block_duration_minutes and not isinstance(block_duration_minutes, int):
            raise TypeError('Expected property block_duration_minutes to be a int')
        __self__.block_duration_minutes = block_duration_minutes
        """
        The required duration for the Spot instances, in minutes. This value must be a multiple of 60 (60, 120, 180, 240, 300, or 360).
        The duration period starts as soon as your Spot instance receives its instance ID. At the end of the duration period, Amazon EC2 marks the Spot instance for termination and provides a Spot instance termination notice, which gives the instance a two-minute warning before it terminates.
        Note that you can't specify an Availability Zone group or a launch group if you specify a duration.
        """
        __props__['blockDurationMinutes'] = block_duration_minutes

        if cpu_core_count and not isinstance(cpu_core_count, int):
            raise TypeError('Expected property cpu_core_count to be a int')
        __self__.cpu_core_count = cpu_core_count
        """
        Sets the number of CPU cores for an instance. This option is 
        only supported on creation of instance type that support CPU Options
        [CPU Cores and Threads Per CPU Core Per Instance Type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html#cpu-options-supported-instances-values) - specifying this option for unsupported instance types will return an error from the EC2 API.
        """
        __props__['cpuCoreCount'] = cpu_core_count

        if cpu_threads_per_core and not isinstance(cpu_threads_per_core, int):
            raise TypeError('Expected property cpu_threads_per_core to be a int')
        __self__.cpu_threads_per_core = cpu_threads_per_core
        """
        If set to to 1, hyperthreading is disabled on the launcehd instance. Defaults to 2 if not set. See [Optimizing CPU Options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html) for more information.
        """
        __props__['cpuThreadsPerCore'] = cpu_threads_per_core

        if credit_specification and not isinstance(credit_specification, dict):
            raise TypeError('Expected property credit_specification to be a dict')
        __self__.credit_specification = credit_specification
        """
        Customize the credit specification of the instance. See Credit Specification below for more details.
        """
        __props__['creditSpecification'] = credit_specification

        if disable_api_termination and not isinstance(disable_api_termination, bool):
            raise TypeError('Expected property disable_api_termination to be a bool')
        __self__.disable_api_termination = disable_api_termination
        """
        If true, enables [EC2 Instance
        Termination Protection](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingDisableAPITermination)
        """
        __props__['disableApiTermination'] = disable_api_termination

        if ebs_block_devices and not isinstance(ebs_block_devices, list):
            raise TypeError('Expected property ebs_block_devices to be a list')
        __self__.ebs_block_devices = ebs_block_devices
        """
        Additional EBS block devices to attach to the
        instance.  See Block Devices below for details.
        """
        __props__['ebsBlockDevices'] = ebs_block_devices

        if ebs_optimized and not isinstance(ebs_optimized, bool):
            raise TypeError('Expected property ebs_optimized to be a bool')
        __self__.ebs_optimized = ebs_optimized
        """
        If true, the launched EC2 instance will be EBS-optimized.
        Note that if this is not set on an instance type that is optimized by default then
        this will show as disabled but if the instance type is optimized by default then
        there is no need to set this and there is no effect to disabling it.
        See the [EBS Optimized section](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSOptimized.html) of the AWS User Guide for more information.
        """
        __props__['ebsOptimized'] = ebs_optimized

        if ephemeral_block_devices and not isinstance(ephemeral_block_devices, list):
            raise TypeError('Expected property ephemeral_block_devices to be a list')
        __self__.ephemeral_block_devices = ephemeral_block_devices
        """
        Customize Ephemeral (also known as
        "Instance Store") volumes on the instance. See Block Devices below for details.
        """
        __props__['ephemeralBlockDevices'] = ephemeral_block_devices

        if get_password_data and not isinstance(get_password_data, bool):
            raise TypeError('Expected property get_password_data to be a bool')
        __self__.get_password_data = get_password_data
        """
        If true, wait for password data to become available and retrieve it. Useful for getting the administrator password for instances running Microsoft Windows. The password data is exported to the `password_data` attribute. See [GetPasswordData](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_GetPasswordData.html) for more information.
        """
        __props__['getPasswordData'] = get_password_data

        if iam_instance_profile and not isinstance(iam_instance_profile, basestring):
            raise TypeError('Expected property iam_instance_profile to be a basestring')
        __self__.iam_instance_profile = iam_instance_profile
        """
        The IAM Instance Profile to
        launch the instance with. Specified as the name of the Instance Profile. Ensure your credentials have the correct permission to assign the instance profile according to the [EC2 documentation](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html#roles-usingrole-ec2instance-permissions), notably `iam:PassRole`.
        * `ipv6_address_count`- (Optional) A number of IPv6 addresses to associate with the primary network interface. Amazon EC2 chooses the IPv6 addresses from the range of your subnet.
        """
        __props__['iamInstanceProfile'] = iam_instance_profile

        if instance_initiated_shutdown_behavior and not isinstance(instance_initiated_shutdown_behavior, basestring):
            raise TypeError('Expected property instance_initiated_shutdown_behavior to be a basestring')
        __self__.instance_initiated_shutdown_behavior = instance_initiated_shutdown_behavior
        """
        Shutdown behavior for the
        instance. Amazon defaults this to `stop` for EBS-backed instances and
        `terminate` for instance-store instances. Cannot be set on instance-store
        instances. See [Shutdown Behavior](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingInstanceInitiatedShutdownBehavior) for more information.
        """
        __props__['instanceInitiatedShutdownBehavior'] = instance_initiated_shutdown_behavior

        if instance_interruption_behaviour and not isinstance(instance_interruption_behaviour, basestring):
            raise TypeError('Expected property instance_interruption_behaviour to be a basestring')
        __self__.instance_interruption_behaviour = instance_interruption_behaviour
        """
        Indicates whether a Spot instance stops or terminates when it is interrupted. Default is `terminate` as this is the current AWS behaviour.
        """
        __props__['instanceInterruptionBehaviour'] = instance_interruption_behaviour

        if not instance_type:
            raise TypeError('Missing required property instance_type')
        elif not isinstance(instance_type, basestring):
            raise TypeError('Expected property instance_type to be a basestring')
        __self__.instance_type = instance_type
        """
        The type of instance to start. Updates to this field will trigger a stop/start of the EC2 instance.
        """
        __props__['instanceType'] = instance_type

        if ipv6_address_count and not isinstance(ipv6_address_count, int):
            raise TypeError('Expected property ipv6_address_count to be a int')
        __self__.ipv6_address_count = ipv6_address_count
        __props__['ipv6AddressCount'] = ipv6_address_count

        if ipv6_addresses and not isinstance(ipv6_addresses, list):
            raise TypeError('Expected property ipv6_addresses to be a list')
        __self__.ipv6_addresses = ipv6_addresses
        """
        Specify one or more IPv6 addresses from the range of the subnet to associate with the primary network interface
        """
        __props__['ipv6Addresses'] = ipv6_addresses

        if key_name and not isinstance(key_name, basestring):
            raise TypeError('Expected property key_name to be a basestring')
        __self__.key_name = key_name
        """
        The key name of the Key Pair to use for the instance; which can be managed using the `aws_key_pair` resource.
        """
        __props__['keyName'] = key_name

        if launch_group and not isinstance(launch_group, basestring):
            raise TypeError('Expected property launch_group to be a basestring')
        __self__.launch_group = launch_group
        """
        A launch group is a group of spot instances that launch together and terminate together.
        If left empty instances are launched and terminated individually.
        """
        __props__['launchGroup'] = launch_group

        if monitoring and not isinstance(monitoring, bool):
            raise TypeError('Expected property monitoring to be a bool')
        __self__.monitoring = monitoring
        """
        If true, the launched EC2 instance will have detailed monitoring enabled. (Available since v0.6.0)
        """
        __props__['monitoring'] = monitoring

        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError('Expected property network_interfaces to be a list')
        __self__.network_interfaces = network_interfaces
        """
        Customize network interfaces to be attached at instance boot time. See Network Interfaces below for more details.
        """
        __props__['networkInterfaces'] = network_interfaces

        if placement_group and not isinstance(placement_group, basestring):
            raise TypeError('Expected property placement_group to be a basestring')
        __self__.placement_group = placement_group
        """
        The Placement Group to start the instance in.
        """
        __props__['placementGroup'] = placement_group

        if private_ip and not isinstance(private_ip, basestring):
            raise TypeError('Expected property private_ip to be a basestring')
        __self__.private_ip = private_ip
        """
        Private IP address to associate with the
        instance in a VPC.
        """
        __props__['privateIp'] = private_ip

        if root_block_device and not isinstance(root_block_device, dict):
            raise TypeError('Expected property root_block_device to be a dict')
        __self__.root_block_device = root_block_device
        """
        Customize details about the root block
        device of the instance. See Block Devices below for details.
        """
        __props__['rootBlockDevice'] = root_block_device

        if security_groups and not isinstance(security_groups, list):
            raise TypeError('Expected property security_groups to be a list')
        __self__.security_groups = security_groups
        """
        A list of security group names to associate with.
        """
        __props__['securityGroups'] = security_groups

        if source_dest_check and not isinstance(source_dest_check, bool):
            raise TypeError('Expected property source_dest_check to be a bool')
        __self__.source_dest_check = source_dest_check
        """
        Controls if traffic is routed to the instance when
        the destination address does not match the instance. Used for NAT or VPNs. Defaults true.
        """
        __props__['sourceDestCheck'] = source_dest_check

        if spot_price and not isinstance(spot_price, basestring):
            raise TypeError('Expected property spot_price to be a basestring')
        __self__.spot_price = spot_price
        """
        The maximum price to request on the spot market.
        """
        __props__['spotPrice'] = spot_price

        if spot_type and not isinstance(spot_type, basestring):
            raise TypeError('Expected property spot_type to be a basestring')
        __self__.spot_type = spot_type
        """
        If set to `one-time`, after
        the instance is terminated, the spot request will be closed.
        """
        __props__['spotType'] = spot_type

        if subnet_id and not isinstance(subnet_id, basestring):
            raise TypeError('Expected property subnet_id to be a basestring')
        __self__.subnet_id = subnet_id
        """
        The VPC Subnet ID to launch in.
        """
        __props__['subnetId'] = subnet_id

        if tags and not isinstance(tags, dict):
            raise TypeError('Expected property tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags to assign to the resource.
        """
        __props__['tags'] = tags

        if tenancy and not isinstance(tenancy, basestring):
            raise TypeError('Expected property tenancy to be a basestring')
        __self__.tenancy = tenancy
        """
        The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of dedicated runs on single-tenant hardware. The host tenancy is not supported for the import-instance command.
        """
        __props__['tenancy'] = tenancy

        if user_data and not isinstance(user_data, basestring):
            raise TypeError('Expected property user_data to be a basestring')
        __self__.user_data = user_data
        """
        The user data to provide when launching the instance. Do not pass gzip-compressed data via this argument; see `user_data_base64` instead.
        """
        __props__['userData'] = user_data

        if user_data_base64 and not isinstance(user_data_base64, basestring):
            raise TypeError('Expected property user_data_base64 to be a basestring')
        __self__.user_data_base64 = user_data_base64
        """
        Can be used instead of `user_data` to pass base64-encoded binary data directly. Use this instead of `user_data` whenever the value is not a valid UTF-8 string. For example, gzip-encoded user data must be base64-encoded and passed via this argument to avoid corruption.
        """
        __props__['userDataBase64'] = user_data_base64

        if valid_from and not isinstance(valid_from, basestring):
            raise TypeError('Expected property valid_from to be a basestring')
        __self__.valid_from = valid_from
        """
        The start date and time of the request, in UTC [RFC3339](https://tools.ietf.org/html/rfc3339#section-5.8) format(for example, YYYY-MM-DDTHH:MM:SSZ). The default is to start fulfilling the request immediately.
        """
        __props__['validFrom'] = valid_from

        if valid_until and not isinstance(valid_until, basestring):
            raise TypeError('Expected property valid_until to be a basestring')
        __self__.valid_until = valid_until
        """
        The end date and time of the request, in UTC [RFC3339](https://tools.ietf.org/html/rfc3339#section-5.8) format(for example, YYYY-MM-DDTHH:MM:SSZ). At this point, no new Spot instance requests are placed or enabled to fulfill the request. The default end date is 7 days from the current date.
        """
        __props__['validUntil'] = valid_until

        if volume_tags and not isinstance(volume_tags, dict):
            raise TypeError('Expected property volume_tags to be a dict')
        __self__.volume_tags = volume_tags
        """
        A mapping of tags to assign to the devices created by the instance at launch time.
        """
        __props__['volumeTags'] = volume_tags

        if vpc_security_group_ids and not isinstance(vpc_security_group_ids, list):
            raise TypeError('Expected property vpc_security_group_ids to be a list')
        __self__.vpc_security_group_ids = vpc_security_group_ids
        """
        A list of security group IDs to associate with.
        """
        __props__['vpcSecurityGroupIds'] = vpc_security_group_ids

        if wait_for_fulfillment and not isinstance(wait_for_fulfillment, bool):
            raise TypeError('Expected property wait_for_fulfillment to be a bool')
        __self__.wait_for_fulfillment = wait_for_fulfillment
        """
        If set, Terraform will
        wait for the Spot Request to be fulfilled, and will throw an error if the
        timeout of 10m is reached.
        """
        __props__['waitForFulfillment'] = wait_for_fulfillment

        __self__.arn = pulumi.runtime.UNKNOWN
        __self__.instance_state = pulumi.runtime.UNKNOWN
        __self__.network_interface_id = pulumi.runtime.UNKNOWN
        __self__.password_data = pulumi.runtime.UNKNOWN
        __self__.primary_network_interface_id = pulumi.runtime.UNKNOWN
        __self__.private_dns = pulumi.runtime.UNKNOWN
        """
        The private DNS name assigned to the instance. Can only be
        used inside the Amazon EC2, and only available if you've enabled DNS hostnames
        for your VPC
        """
        __self__.public_dns = pulumi.runtime.UNKNOWN
        """
        The public DNS name assigned to the instance. For EC2-VPC, this
        is only available if you've enabled DNS hostnames for your VPC
        """
        __self__.public_ip = pulumi.runtime.UNKNOWN
        """
        The public IP address assigned to the instance, if applicable.
        """
        __self__.spot_bid_status = pulumi.runtime.UNKNOWN
        """
        The current [bid
        status](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-bid-status.html)
        of the Spot Instance Request.
        * `spot_request_state` The current [request
        state](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-requests.html#creating-spot-request-status)
        of the Spot Instance Request.
        """
        __self__.spot_instance_id = pulumi.runtime.UNKNOWN
        """
        The Instance ID (if any) that is currently fulfilling
        the Spot Instance request.
        """
        __self__.spot_request_state = pulumi.runtime.UNKNOWN

        super(SpotInstanceRequest, __self__).__init__(
            'aws:ec2/spotInstanceRequest:SpotInstanceRequest',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'ami' in outs:
            self.ami = outs['ami']
        if 'arn' in outs:
            self.arn = outs['arn']
        if 'associatePublicIpAddress' in outs:
            self.associate_public_ip_address = outs['associatePublicIpAddress']
        if 'availabilityZone' in outs:
            self.availability_zone = outs['availabilityZone']
        if 'blockDurationMinutes' in outs:
            self.block_duration_minutes = outs['blockDurationMinutes']
        if 'cpuCoreCount' in outs:
            self.cpu_core_count = outs['cpuCoreCount']
        if 'cpuThreadsPerCore' in outs:
            self.cpu_threads_per_core = outs['cpuThreadsPerCore']
        if 'creditSpecification' in outs:
            self.credit_specification = outs['creditSpecification']
        if 'disableApiTermination' in outs:
            self.disable_api_termination = outs['disableApiTermination']
        if 'ebsBlockDevices' in outs:
            self.ebs_block_devices = outs['ebsBlockDevices']
        if 'ebsOptimized' in outs:
            self.ebs_optimized = outs['ebsOptimized']
        if 'ephemeralBlockDevices' in outs:
            self.ephemeral_block_devices = outs['ephemeralBlockDevices']
        if 'getPasswordData' in outs:
            self.get_password_data = outs['getPasswordData']
        if 'iamInstanceProfile' in outs:
            self.iam_instance_profile = outs['iamInstanceProfile']
        if 'instanceInitiatedShutdownBehavior' in outs:
            self.instance_initiated_shutdown_behavior = outs['instanceInitiatedShutdownBehavior']
        if 'instanceInterruptionBehaviour' in outs:
            self.instance_interruption_behaviour = outs['instanceInterruptionBehaviour']
        if 'instanceState' in outs:
            self.instance_state = outs['instanceState']
        if 'instanceType' in outs:
            self.instance_type = outs['instanceType']
        if 'ipv6AddressCount' in outs:
            self.ipv6_address_count = outs['ipv6AddressCount']
        if 'ipv6Addresses' in outs:
            self.ipv6_addresses = outs['ipv6Addresses']
        if 'keyName' in outs:
            self.key_name = outs['keyName']
        if 'launchGroup' in outs:
            self.launch_group = outs['launchGroup']
        if 'monitoring' in outs:
            self.monitoring = outs['monitoring']
        if 'networkInterfaces' in outs:
            self.network_interfaces = outs['networkInterfaces']
        if 'networkInterfaceId' in outs:
            self.network_interface_id = outs['networkInterfaceId']
        if 'passwordData' in outs:
            self.password_data = outs['passwordData']
        if 'placementGroup' in outs:
            self.placement_group = outs['placementGroup']
        if 'primaryNetworkInterfaceId' in outs:
            self.primary_network_interface_id = outs['primaryNetworkInterfaceId']
        if 'privateDns' in outs:
            self.private_dns = outs['privateDns']
        if 'privateIp' in outs:
            self.private_ip = outs['privateIp']
        if 'publicDns' in outs:
            self.public_dns = outs['publicDns']
        if 'publicIp' in outs:
            self.public_ip = outs['publicIp']
        if 'rootBlockDevice' in outs:
            self.root_block_device = outs['rootBlockDevice']
        if 'securityGroups' in outs:
            self.security_groups = outs['securityGroups']
        if 'sourceDestCheck' in outs:
            self.source_dest_check = outs['sourceDestCheck']
        if 'spotBidStatus' in outs:
            self.spot_bid_status = outs['spotBidStatus']
        if 'spotInstanceId' in outs:
            self.spot_instance_id = outs['spotInstanceId']
        if 'spotPrice' in outs:
            self.spot_price = outs['spotPrice']
        if 'spotRequestState' in outs:
            self.spot_request_state = outs['spotRequestState']
        if 'spotType' in outs:
            self.spot_type = outs['spotType']
        if 'subnetId' in outs:
            self.subnet_id = outs['subnetId']
        if 'tags' in outs:
            self.tags = outs['tags']
        if 'tenancy' in outs:
            self.tenancy = outs['tenancy']
        if 'userData' in outs:
            self.user_data = outs['userData']
        if 'userDataBase64' in outs:
            self.user_data_base64 = outs['userDataBase64']
        if 'validFrom' in outs:
            self.valid_from = outs['validFrom']
        if 'validUntil' in outs:
            self.valid_until = outs['validUntil']
        if 'volumeTags' in outs:
            self.volume_tags = outs['volumeTags']
        if 'vpcSecurityGroupIds' in outs:
            self.vpc_security_group_ids = outs['vpcSecurityGroupIds']
        if 'waitForFulfillment' in outs:
            self.wait_for_fulfillment = outs['waitForFulfillment']
