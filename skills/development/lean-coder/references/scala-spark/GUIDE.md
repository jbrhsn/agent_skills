# Scala and Spark

Read the job, schemas, Spark/Scala versions, cluster configuration, and sink contract before changing execution. Use [data engineering](../data-engineering/GUIDE.md) for grain, replay, backfill, and quality guarantees.

## Transformations

Prefer built-in SQL/DataFrame expressions when they express the semantics and allow optimizer visibility. Use UDFs or lower-level APIs when justified; test their null, serialization, and performance behavior. Keep transformations separable from reads/writes but test all three boundaries.

Choose explicit schemas and deterministic tie-breakers for deduplication/latest-event logic. Verify join cardinality, null behavior, timezone conversions, and decimals. Do not treat success of a Spark action as proof of data correctness.

## Execution

Inspect the physical plan and runtime metrics for skew, shuffle, spills, partition pruning, and task imbalance. Broadcast only when the build side fits executor memory under realistic concurrency. Cache reused expensive computations when measurements justify the memory cost, and unpersist when no longer needed; there is no universal cache-count limit.

Avoid collecting unbounded data on the driver. Partition and file sizes should fit workload, storage, and downstream access; indiscriminate repartitioning or coalesce(1) can create bottlenecks. Bound external calls from partitions and account for task retries/speculative execution duplicating side effects.

## Streaming and verification

Match watermarks, state retention, output mode, and checkpoint compatibility to late-data semantics. Test restarts and failures around sink commits. foreachBatch does not itself guarantee exactly-once effects; deduplication/transactional sink logic must establish that guarantee. See [Spark's streaming guide](https://spark.apache.org/docs/3.5.6/structured-streaming-programming-guide.html) and the project's matching version.

Use local Spark fixtures for transform semantics plus integration tests for source/sink, replay, and publication. Cluster performance requires representative volume, skew, and configuration. Redact sensitive rows from logs and inspection output.
