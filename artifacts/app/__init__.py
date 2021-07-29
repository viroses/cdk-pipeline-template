from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
)

class Application(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, bmt_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        cluster = ecs.Cluster(self,"ObservationCluster", 
            enable_fargate_capacity_providers=True,
            vpc=bmt_vpc
        )
        
        # # Add capacity to it
        # cluster.add_capacity("DefaultAutoScalingGroupCapacity",
        #     instance_type=ec2.InstanceType("t2.xlarge"),
        #     desired_capacity=3
        # )
        
        # task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
        
        # task_definition.add_container("DefaultContainer",
        #     image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        #     memory_limit_mi_b=512
        # )
        
        fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
            memory_limit_mib=512,
            cpu=256
        )
        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        web_container = fargate_task_definition.add_container("WebContainer",
            # Use an image from DockerHub
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        )
        
        log_container = fargate_task_definition.add_firelens_log_router("LogContainer",
            firelens_config=ecs.FirelensConfig(
                type=ecs.FirelensLogRouterType.FLUENTBIT
            ),
            image=ecs.ContainerImage.from_registry("906394416424.dkr.ecr.ap-northeast-2.amazonaws.com/aws-for-fluent-bit:latest")
        )
        
        # Instantiate an Amazon ECS Service
        ecs_service = ecs.FargateService(self, "Service",
            cluster=cluster,
            task_definition=fargate_task_definition,
            desired_count=3
        )