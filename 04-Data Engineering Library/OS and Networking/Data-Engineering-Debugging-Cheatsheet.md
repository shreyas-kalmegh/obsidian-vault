# Data Engineering Debugging Cheatsheet

## How To Use This Note
This is a practical command reference for debugging Kafka, Spark, JVM-based data services, Linux hosts, and containerized data platforms. The point is to know the first few commands that narrow the problem quickly.

## Linux First-Pass Checks
- `uptime` -> load average and system uptime
- `vmstat 1` -> CPU, run queue, memory, paging, and swap pressure
- `free -h` -> memory and swap summary
- `df -h` -> disk space
- `iostat -xz 1` -> disk utilization, queueing, and latency if installed
- `ss -s` -> socket summary
- `dmesg | tail -n 100` -> recent kernel or disk/network errors

## Process And JVM Inspection
- `ps -ef | rg "java|kafka|spark"` -> locate JVM-based processes
- `top -H -p <pid>` -> per-thread CPU view
- `jps -lv` -> JVM processes with arguments if JDK tools are installed
- `jstack <pid>` -> thread dump for lock contention or stuck threads
- `jcmd <pid> GC.heap_info` -> heap summary
- `jstat -gc <pid> 1000` -> GC behavior over time
- `lsof -p <pid>` -> files, sockets, and logs opened by a process

## Kafka Broker Debugging
- `kafka-topics.sh --bootstrap-server <broker:9092> --describe --topic <topic>` -> topic partition details
- `kafka-consumer-groups.sh --bootstrap-server <broker:9092> --describe --group <group>` -> consumer lag and partition ownership
- `kafka-configs.sh --bootstrap-server <broker:9092> --entity-type topics --entity-name <topic> --describe` -> topic config
- `kafka-log-dirs.sh --bootstrap-server <broker:9092> --describe` -> broker log directory usage
- `ss -ltnp | rg 9092` -> verify broker listen socket
- `tail -f server.log` -> broker log follow

## Kafka Command Patterns
### Check Whether Lag Is Real Or Assignment-Related
```bash
kafka-consumer-groups.sh --bootstrap-server <broker:9092> --describe --group <group>
```

What to look for:
- high `LAG` on a subset of partitions
- consumers missing assignments
- one consumer owning too many hot partitions

### Inspect Topic Shape
```bash
kafka-topics.sh --bootstrap-server <broker:9092> --describe --topic <topic>
```

What to look for:
- partition count
- replication factor
- leader spread
- under-replicated partitions

## Spark Debugging
- `spark-submit --verbose ...` -> show expanded submission details
- `yarn application -list` -> running applications on YARN if applicable
- `yarn logs -applicationId <appId>` -> fetch YARN logs
- `kubectl logs <driver-pod>` -> Spark driver logs on Kubernetes
- `kubectl logs <executor-pod>` -> executor logs on Kubernetes
- `jstack <driver-pid>` -> stuck driver threads
- `jstat -gc <pid> 1000` -> GC pressure on driver or executor JVM

## Spark Things To Verify First
- Is the driver healthy and making progress?
- Are executors being lost or restarted?
- Is shuffle spilling heavily to disk?
- Is skew causing one or two tasks to dominate stage time?
- Is object-store or metastore latency throttling task completion?

## Network And DNS Checks For Data Systems
- `nslookup <broker-host>` -> DNS resolution
- `dig <broker-host>` -> detailed DNS answers if installed
- `ping <host>` -> quick reachability and RTT
- `curl -v <url>` -> inspect HTTP dependencies such as schema registry or control plane
- `ss -tan | rg "<port>"` -> active TCP connections for a dependency

## Storage And File Checks
- `du -sh <dir>` -> directory size
- `find <path> -maxdepth 2 -type f | head` -> shallow file inspection
- `lsof +D <dir>` -> processes using files in a directory if supported
- `ls -lah <dir>` -> file timestamps and size

## HDFS Debugging
- `hdfs dfs -ls <path>` -> list files and directories in HDFS
- `hdfs dfs -du -h <path>` -> space usage for HDFS paths
- `hdfs dfs -count -h <path>` -> file, directory, and quota counts
- `hdfs dfs -cat <path>` -> print small file contents
- `hdfs dfs -tail <path>` -> tail an HDFS file
- `hdfs dfs -test -e <path>` -> check whether a path exists
- `hdfs fsck <path> -files -blocks -locations` -> inspect block health and placement
- `hdfs dfsadmin -report` -> cluster capacity and live/dead datanode summary
- `hdfs haadmin -getServiceState <namenode>` -> active or standby state in HA setups

## HDFS Things To Verify First
- Is the path actually present and readable?
- Are files still being written or left incomplete?
- Is block replication healthy?
- Is the NameNode healthy and, in HA mode, is the expected node active?
- Is the issue capacity, permissions, or block availability?

## Containers And Kubernetes
- `kubectl get pods -o wide` -> pod placement and status
- `kubectl describe pod <pod>` -> restarts, events, probe failures
- `kubectl logs <pod> --previous` -> logs from a crashed prior container
- `kubectl top pod` -> live pod CPU and memory if metrics are enabled
- `kubectl get events --sort-by=.lastTimestamp` -> recent cluster events

## Common Incident Recipes
### Consumer Lag Is Rising
```bash
kafka-consumer-groups.sh --bootstrap-server <broker:9092> --describe --group <group>
vmstat 1
top -H -p <consumer_pid>
```

Check:
- consumer group rebalances
- CPU starvation or GC pauses
- slow downstream sink
- one hot partition

### Broker Looks Slow
```bash
iostat -xz 1
ss -s
tail -f server.log
```

Check:
- disk queueing and await time
- network socket pressure
- ISR shrink or replication issues

### Spark Job Is Hanging
```bash
kubectl logs <driver-pod>
kubectl logs <executor-pod>
jstack <driver-pid>
```

Check:
- stage retries
- skewed tasks
- blocked driver threads
- object store or catalog timeouts

### HDFS Read Or Write Looks Broken
```bash
hdfs dfs -ls <path>
hdfs dfs -count -h <path>
hdfs fsck <path> -files -blocks -locations
hdfs dfsadmin -report
```

Check:
- missing path or wrong environment
- small-file explosion or quota issues
- under-replicated or missing blocks
- dead or decommissioned datanodes
- NameNode capacity or failover state problems

## Practical Interview Angle
- Start with system pressure before application theory.
- Separate "service is down" from "service is slow" from "dependency is slow."
- In Kafka incidents, determine whether the problem is broker-side, consumer-side, partition-skew, or downstream backpressure.
- In Spark incidents, determine whether the bottleneck is driver coordination, executor compute, shuffle IO, or an external dependency.
- In HDFS incidents, determine whether the problem is path correctness, permissions, NameNode health, block replication, or cluster capacity.

## Related
- [[04-Data Engineering Library/OS and Networking/Bash-Shell-Debugging-Cheatsheet.md]]
- [[04-Data Engineering Library/OS and Networking/Networking-Flow-Control-Congestion-Backpressure.md]]
- [[04-Data Engineering Library/OS and Networking/OS-Disk-IO-Page-Cache-Direct-IO.md]]
