from aws_cdk import (
    # Duration,
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecs_patterns as ecs_patterns,
    CfnOutput
)
from constructs import Construct
import os

class InfraStack(Stack):
    IMAGE = ecs.ContainerImage.from_asset(
        os.path.join(os.path.dirname(__file__),
                     '../../service')
        )

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # The code that defines your stack goes here

        vpc = ec2.Vpc(self, "MyStackVPC", max_azs=3)     # default is all AZs in region

        cluster = ecs.Cluster(self, "MyStackCluster", vpc=vpc)

        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 
            "MyFargateService",
            cluster=cluster,            # Required
            cpu=256,                    # Default is 256
            desired_count=1,            # Default is 1
            task_image_options=
                ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                    image = self.IMAGE),
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                cpu_architecture=ecs.CpuArchitecture.ARM64
                # Specify ARM architecture since my docker is built on M1 chip
            ),
            memory_limit_mib=512,     # Default is 512
            public_load_balancer=True # Default is False
        )
        # Outputs Sections
        CfnOutput(
            self, "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name,
            description="DNS Name of the load balancer"
        )
        
        CfnOutput(
            self, "ServiceArn",
            value=fargate_service.service.service_arn,
            description="ARN of the ECS Service"
        )
        
        CfnOutput(
            self, "ClusterName",
            value=cluster.cluster_name,
            description="Name of the ECS Cluster"
        )
        