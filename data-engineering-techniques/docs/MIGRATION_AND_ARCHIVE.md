# Migration and Archive Plan

## Consolidated sources

- Hadoop MapReduce
- Apache Spark
- Hive
- Pig
- HBase
- Spark K-Means

## Archive sequence

1. Verify every master-repository notebook and job.
2. Deploy the AWS lab once and save non-sensitive logs.
3. Add a deprecation banner to each legacy README pointing to the master repository.
4. Archive the six legacy GitHub repositories.
5. Keep history read-only for provenance.

Do not archive before the master repository is published and validated.
