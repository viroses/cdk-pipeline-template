from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
)

class Application(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, bmt_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        cluster = ecs.Cluster(self,"ObservationCluster", vpc=bmt_vpc)