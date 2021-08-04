from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_elasticloadbalancingv2 as elbv2,
)

class Application(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, bmt_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # target group 생성 - IP로
        # ALB 생성
        
        cluster = ecs.Cluster(self,"ObservationCluster",
            enable_fargate_capacity_providers=True,
            vpc=bmt_vpc
        )
        
        fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
            memory_limit_mib=1024,
            cpu=512
        )
        
        web_container = fargate_task_definition.add_container("WebContainer",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            logging=ecs.LogDrivers.aws_logs(stream_prefix="observation-log-stream"),
            port_mappings=[{"containerPort": 80}], # it makes me crazy!!!
            memory_limit_mib=512,
            cpu=256
        )
        
        # Instantiate an Amazon ECS Service
        ecs_service = ecs.FargateService(self, "ECSService",
            cluster=cluster,
            task_definition=fargate_task_definition,
            desired_count=3
        )

        lb = elbv2.ApplicationLoadBalancer(self, "ServiceLB", vpc=bmt_vpc, internet_facing=True)
        listener = lb.add_listener("Listener", port=80)
        ecs_service.register_load_balancer_targets(
        ecs.EcsTarget(
                container_name="WebContainer",
                container_port=80,
                new_target_group_id="ECSTarget",
                listener=ecs.ListenerConfig.application_listener(listener,
                    protocol=elbv2.ApplicationProtocol.HTTP
                )
            )
        )