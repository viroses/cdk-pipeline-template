from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
)

class Application(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, bmt_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        cluster = ecs.Cluster(self,"ObservationCluster", 
            enable_fargate_capacity_providers=True,
            vpc=bmt_vpc
        )

        fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
            memory_limit_mib=512,
            cpu=256
        )
        
        # log_container = fargate_task_definition.add_firelens_log_router("LogContainer",
        #     firelens_config=ecs.FirelensConfig(
        #         type=ecs.FirelensLogRouterType.FLUENTBIT
        #     ),
        #     image=ecs.ContainerImage.from_ecr_repository(ecr.IRepository.repository_uri_for_tag("906394416424.dkr.ecr.ap-northeast-2.amazonaws.com/aws-for-fluent-bit")),
        #     logging=ecs.LogDrivers.aws_logs(stream_prefix="observation-log-stream")
        # )
        
        web_container = fargate_task_definition.add_container("WebContainer",
            # Use an image from DockerHub
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
            # logging=ecs.LogDrivers.firelens(
            #     options={
            #         "Name": "cloudwatch",
            #         "log_group_name": "observation-log",
            #         "region": "ap-northeast-2"
            #     }
    # )
        )

        
        
        # Instantiate an Amazon ECS Service
        ecs_service = ecs.FargateService(self, "Service",
            cluster=cluster,
            task_definition=fargate_task_definition,
            desired_count=3
        )