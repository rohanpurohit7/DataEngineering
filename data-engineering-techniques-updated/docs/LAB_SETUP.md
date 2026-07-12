# AWS Lab Setup

## Network

- One VPC across two Availability Zones.
- Public subnets host NAT gateways only.
- EMR primary, core, and task nodes use private subnets.
- Security groups allow internal cluster communication.
- Administrators access services through AWS Systems Manager or controlled VPN/bastion patterns.
- S3 gateway endpoints are recommended to reduce NAT traffic.

## EMR node roles

- **Primary node:** NameNode, YARN ResourceManager, cluster coordination, client tools.
- **Core nodes:** HDFS DataNodes and YARN NodeManagers; store HDFS blocks and execute tasks.
- **Task nodes:** YARN compute capacity without HDFS data responsibility; useful for elastic scaling.

## Lab order

1. Deploy foundational AWS resources with CDK.
2. Upload sample data and jobs to S3.
3. Create EMR cluster.
4. Run Hadoop MapReduce.
5. Run Spark ETL.
6. Create Hive external/managed tables.
7. Execute Pig transformation.
8. Create and query HBase table.
9. Run Spark MLlib K-Means.
10. Inspect S3 outputs and CloudWatch logs.
11. Terminate cluster.
