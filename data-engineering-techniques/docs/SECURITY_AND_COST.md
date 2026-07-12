# Security and Cost Controls

- Use private subnets and block public S3 access.
- Use IAM roles, not long-lived access keys.
- Encrypt S3 and EBS; use KMS where required.
- Store logs in S3 and CloudWatch.
- Enable auto-termination for labs.
- Use small On-Demand core nodes for predictable labs; add task nodes or Spot only when interruption is acceptable.
- Tag all resources.
- Destroy CDK resources after use; retained S3 buckets may require manual cleanup.
