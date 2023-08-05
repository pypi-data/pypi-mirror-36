# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Service(pulumi.CustomResource):
    """
    -> **Note:** To prevent a race condition during service deletion, make sure to set `depends_on` to the related `aws_iam_role_policy`; otherwise, the policy may be destroyed too soon and the ECS service will then get stuck in the `DRAINING` state.
    
    Provides an ECS service - effectively a task that is expected to run until an error occurs or a user terminates it (typically a webserver or a database).
    
    See [ECS Services section in AWS developer guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html).
    """
    def __init__(__self__, __name__, __opts__=None, cluster=None, deployment_maximum_percent=None, deployment_minimum_healthy_percent=None, desired_count=None, health_check_grace_period_seconds=None, iam_role=None, launch_type=None, load_balancers=None, name=None, network_configuration=None, ordered_placement_strategies=None, placement_constraints=None, placement_strategies=None, scheduling_strategy=None, service_registries=None, task_definition=None, wait_for_steady_state=None):
        """Create a Service resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if cluster and not isinstance(cluster, basestring):
            raise TypeError('Expected property cluster to be a basestring')
        __self__.cluster = cluster
        """
        ARN of an ECS cluster
        """
        __props__['cluster'] = cluster

        if deployment_maximum_percent and not isinstance(deployment_maximum_percent, int):
            raise TypeError('Expected property deployment_maximum_percent to be a int')
        __self__.deployment_maximum_percent = deployment_maximum_percent
        """
        The upper limit (as a percentage of the service's desiredCount) of the number of running tasks that can be running in a service during a deployment. Not valid when using the `DAEMON` scheduling strategy.
        """
        __props__['deploymentMaximumPercent'] = deployment_maximum_percent

        if deployment_minimum_healthy_percent and not isinstance(deployment_minimum_healthy_percent, int):
            raise TypeError('Expected property deployment_minimum_healthy_percent to be a int')
        __self__.deployment_minimum_healthy_percent = deployment_minimum_healthy_percent
        """
        The lower limit (as a percentage of the service's desiredCount) of the number of running tasks that must remain running and healthy in a service during a deployment. Not valid when using the `DAEMON` scheduling strategy.
        """
        __props__['deploymentMinimumHealthyPercent'] = deployment_minimum_healthy_percent

        if desired_count and not isinstance(desired_count, int):
            raise TypeError('Expected property desired_count to be a int')
        __self__.desired_count = desired_count
        """
        The number of instances of the task definition to place and keep running. Defaults to 0. Do not specify if using the `DAEMON` scheduling strategy.
        """
        __props__['desiredCount'] = desired_count

        if health_check_grace_period_seconds and not isinstance(health_check_grace_period_seconds, int):
            raise TypeError('Expected property health_check_grace_period_seconds to be a int')
        __self__.health_check_grace_period_seconds = health_check_grace_period_seconds
        """
        Seconds to ignore failing load balancer health checks on newly instantiated tasks to prevent premature shutdown, up to 7200. Only valid for services configured to use load balancers.
        """
        __props__['healthCheckGracePeriodSeconds'] = health_check_grace_period_seconds

        if iam_role and not isinstance(iam_role, basestring):
            raise TypeError('Expected property iam_role to be a basestring')
        __self__.iam_role = iam_role
        """
        ARN of the IAM role that allows Amazon ECS to make calls to your load balancer on your behalf. This parameter is required if you are using a load balancer with your service, but only if your task definition does not use the `awsvpc` network mode. If using `awsvpc` network mode, do not specify this role. If your account has already created the Amazon ECS service-linked role, that role is used by default for your service unless you specify a role here.
        """
        __props__['iamRole'] = iam_role

        if launch_type and not isinstance(launch_type, basestring):
            raise TypeError('Expected property launch_type to be a basestring')
        __self__.launch_type = launch_type
        """
        The launch type on which to run your service. The valid values are `EC2` and `FARGATE`. Defaults to `EC2`.
        """
        __props__['launchType'] = launch_type

        if load_balancers and not isinstance(load_balancers, list):
            raise TypeError('Expected property load_balancers to be a list')
        __self__.load_balancers = load_balancers
        """
        A load balancer block. Load balancers documented below.
        """
        __props__['loadBalancers'] = load_balancers

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        The name of the service (up to 255 letters, numbers, hyphens, and underscores)
        """
        __props__['name'] = name

        if network_configuration and not isinstance(network_configuration, dict):
            raise TypeError('Expected property network_configuration to be a dict')
        __self__.network_configuration = network_configuration
        """
        The network configuration for the service. This parameter is required for task definitions that use the `awsvpc` network mode to receive their own Elastic Network Interface, and it is not supported for other network modes.
        """
        __props__['networkConfiguration'] = network_configuration

        if ordered_placement_strategies and not isinstance(ordered_placement_strategies, list):
            raise TypeError('Expected property ordered_placement_strategies to be a list')
        __self__.ordered_placement_strategies = ordered_placement_strategies
        """
        Service level strategy rules that are taken into consideration during task placement. List from top to bottom in order of precedence. The maximum number of `ordered_placement_strategy` blocks is `5`. Defined below.
        """
        __props__['orderedPlacementStrategies'] = ordered_placement_strategies

        if placement_constraints and not isinstance(placement_constraints, list):
            raise TypeError('Expected property placement_constraints to be a list')
        __self__.placement_constraints = placement_constraints
        """
        rules that are taken into consideration during task placement. Maximum number of
        `placement_constraints` is `10`. Defined below.
        """
        __props__['placementConstraints'] = placement_constraints

        if placement_strategies and not isinstance(placement_strategies, list):
            raise TypeError('Expected property placement_strategies to be a list')
        __self__.placement_strategies = placement_strategies
        """
        **Deprecated**, use `ordered_placement_strategy` instead.
        """
        __props__['placementStrategies'] = placement_strategies

        if scheduling_strategy and not isinstance(scheduling_strategy, basestring):
            raise TypeError('Expected property scheduling_strategy to be a basestring')
        __self__.scheduling_strategy = scheduling_strategy
        """
        The scheduling strategy to use for the service. The valid values are `REPLICA` and `DAEMON`. Defaults to `REPLICA`. Note that [*Fargate tasks do not support the `DAEMON` scheduling strategy*](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/scheduling_tasks.html).
        """
        __props__['schedulingStrategy'] = scheduling_strategy

        if service_registries and not isinstance(service_registries, dict):
            raise TypeError('Expected property service_registries to be a dict')
        __self__.service_registries = service_registries
        """
        The service discovery registries for the service. The maximum number of `service_registries` blocks is `1`.
        """
        __props__['serviceRegistries'] = service_registries

        if not task_definition:
            raise TypeError('Missing required property task_definition')
        elif not isinstance(task_definition, basestring):
            raise TypeError('Expected property task_definition to be a basestring')
        __self__.task_definition = task_definition
        """
        The family and revision (`family:revision`) or full ARN of the task definition that you want to run in your service.
        """
        __props__['taskDefinition'] = task_definition

        if wait_for_steady_state and not isinstance(wait_for_steady_state, bool):
            raise TypeError('Expected property wait_for_steady_state to be a bool')
        __self__.wait_for_steady_state = wait_for_steady_state
        """
        If `true`, Terraform will wait for the service to reach a steady state (like [`aws ecs wait services-stable`](https://docs.aws.amazon.com/cli/latest/reference/ecs/wait/services-stable.html)) before continuing. Default `false`.
        """
        __props__['waitForSteadyState'] = wait_for_steady_state

        super(Service, __self__).__init__(
            'aws:ecs/service:Service',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'cluster' in outs:
            self.cluster = outs['cluster']
        if 'deploymentMaximumPercent' in outs:
            self.deployment_maximum_percent = outs['deploymentMaximumPercent']
        if 'deploymentMinimumHealthyPercent' in outs:
            self.deployment_minimum_healthy_percent = outs['deploymentMinimumHealthyPercent']
        if 'desiredCount' in outs:
            self.desired_count = outs['desiredCount']
        if 'healthCheckGracePeriodSeconds' in outs:
            self.health_check_grace_period_seconds = outs['healthCheckGracePeriodSeconds']
        if 'iamRole' in outs:
            self.iam_role = outs['iamRole']
        if 'launchType' in outs:
            self.launch_type = outs['launchType']
        if 'loadBalancers' in outs:
            self.load_balancers = outs['loadBalancers']
        if 'name' in outs:
            self.name = outs['name']
        if 'networkConfiguration' in outs:
            self.network_configuration = outs['networkConfiguration']
        if 'orderedPlacementStrategies' in outs:
            self.ordered_placement_strategies = outs['orderedPlacementStrategies']
        if 'placementConstraints' in outs:
            self.placement_constraints = outs['placementConstraints']
        if 'placementStrategies' in outs:
            self.placement_strategies = outs['placementStrategies']
        if 'schedulingStrategy' in outs:
            self.scheduling_strategy = outs['schedulingStrategy']
        if 'serviceRegistries' in outs:
            self.service_registries = outs['serviceRegistries']
        if 'taskDefinition' in outs:
            self.task_definition = outs['taskDefinition']
        if 'waitForSteadyState' in outs:
            self.wait_for_steady_state = outs['waitForSteadyState']
