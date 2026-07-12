from aws_cdk import (
    Stack, Duration, RemovalPolicy,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    aws_logs as logs,
)
from constructs import Construct

class DataEngineeringStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self, "DataEngineeringVpc",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24
                ),
            ],
        )

        bucket = s3.Bucket(
            self, "DataLake",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            enforce_ssl=True,
            lifecycle_rules=[s3.LifecycleRule(
                id="archive-old-objects",
                enabled=True,
                transitions=[s3.Transition(
                    storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                    transition_after=Duration.days(30),
                )],
            )],
            removal_policy=RemovalPolicy.RETAIN,
        )

        log_group = logs.LogGroup(
            self, "EmrLogs",
            retention=logs.RetentionDays.ONE_MONTH,
            removal_policy=RemovalPolicy.DESTROY,
        )

        emr_service_role = iam.Role(
            self, "EmrServiceRole",
            assumed_by=iam.ServicePrincipal("elasticmapreduce.amazonaws.com"),
        )
        emr_service_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonElasticMapReduceRole")
        )

        ec2_role = iam.Role(
            self, "EmrEc2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )
        ec2_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonElasticMapReduceforEC2Role")
        )
        bucket.grant_read_write(ec2_role)

        iam.CfnInstanceProfile(
            self, "EmrInstanceProfile",
            roles=[ec2_role.role_name],
            instance_profile_name="DataEngineeringEmrEc2InstanceProfile",
        )

        self.bucket_name = bucket.bucket_name
        self.vpc_id = vpc.vpc_id
        self.private_subnet_ids = [s.subnet_id for s in vpc.private_subnets]
        self.log_group_name = log_group.log_group_name
