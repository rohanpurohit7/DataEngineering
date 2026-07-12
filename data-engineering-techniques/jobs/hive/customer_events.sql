CREATE EXTERNAL TABLE IF NOT EXISTS customer_events (
  event_id BIGINT,
  customer_id BIGINT,
  region STRING,
  event_type STRING,
  amount DOUBLE,
  event_ts TIMESTAMP
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ('separatorChar'=',','skip.header.line.count'='1')
LOCATION '${hiveconf:INPUT_LOCATION}';

CREATE TABLE IF NOT EXISTS daily_event_summary
STORED AS PARQUET AS
SELECT to_date(event_ts) event_date, region, event_type,
       count(*) event_count, sum(amount) total_amount
FROM customer_events
GROUP BY to_date(event_ts), region, event_type;
