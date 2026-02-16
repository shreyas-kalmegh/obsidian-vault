# Flink Checkpointing — Practical Examples

## Local setup
- Run a single-node Flink cluster via Docker
- Use the RocksDB state backend and configure checkpoint dir to local filesystem or S3-compatible storage

## Example config
```yaml
state.backend: rocksdb
state.checkpoints.dir: file:///tmp/flink-checkpoints
execution.checkpointing.interval: 30s
```
