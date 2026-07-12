events = LOAD '$INPUT' USING PigStorage(',') AS
(event_id:long, customer_id:long, region:chararray, event_type:chararray, amount:double, event_ts:chararray);
clean = FILTER events BY event_id IS NOT NULL;
grouped = GROUP clean BY (region, event_type);
summary = FOREACH grouped GENERATE FLATTEN(group), COUNT(clean) AS event_count, SUM(clean.amount) AS total_amount;
STORE summary INTO '$OUTPUT' USING PigStorage(',');
