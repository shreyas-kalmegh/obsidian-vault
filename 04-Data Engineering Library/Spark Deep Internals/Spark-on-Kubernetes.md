# Spark on Kubernetes

## Overview
Running Spark on Kubernetes means Spark applications are executed as Kubernetes-managed containers, with the driver and executors typically running as pods. Spark still behaves like Spark, but cluster operations, networking, storage, and resource management are expressed through Kubernetes primitives instead of YARN-style containers and node managers.

High-level idea:
- Spark driver coordinates the application
- executors run as Kubernetes pods
- Kubernetes schedules those pods onto cluster nodes
- Spark and Kubernetes cooperate: Spark handles distributed compute logic, Kubernetes handles container orchestration and resource placement

Why it matters:
- many teams now run Spark in containerized platform environments
- performance and reliability depend not just on Spark configs, but also on pod scheduling, storage classes, node pressure, and network policy
- debugging Spark on Kubernetes requires understanding both the Spark plan and the Kubernetes runtime environment

Interview-safe line:
- "Spark on Kubernetes keeps Spark's driver/executor model but maps those processes onto pods, so Spark tuning and Kubernetes operations both matter."

## Core Deployment Model

### Driver pod
The driver is the control plane for the Spark application. On Kubernetes it usually runs as its own pod.

Driver responsibilities:
- plan and schedule Spark tasks
- request executor pods
- coordinate shuffle metadata and stage execution
- expose logs and application status

Why driver placement matters:
- if the driver pod dies, the application usually dies
- driver networking and service exposure affect executor communication
- driver CPU and memory sizing matter for large jobs with many tasks or complex plans

### Executor pods
Executors run as separate pods created for the application.

Executor responsibilities:
- execute tasks
- hold cached data
- participate in shuffle
- report status back to the driver

Why executors matter on Kubernetes:
- pod startup latency affects elasticity
- pod eviction and node instability can look like Spark failures
- executor memory settings must align with container limits, not just Spark defaults

## How Spark Maps to Kubernetes Primitives

Spark concepts to Kubernetes concepts:
- driver process -> driver pod
- executor process -> executor pod
- application resources -> CPU/memory requests and limits
- local disk use -> container filesystem or attached volumes
- service discovery -> Kubernetes services/DNS

Useful mental model:
- Spark still decides "how many executors do I want?"
- Kubernetes decides "where can these pods run?"

This means performance depends on both:
- Spark plan quality and partitioning
- Kubernetes scheduler success and node capacity

## Driver Placement and Networking
The driver must be reachable by executors. This is one of the most important operational differences when running Spark on Kubernetes.

Why it matters:
- executors need to register with and communicate back to the driver
- misconfigured services, DNS, or network policy can prevent executors from connecting
- driver restarts or pod rescheduling can break application stability

Common operational patterns:
- cluster mode with driver inside Kubernetes
- client mode with driver outside the cluster or in a different environment

Practical rule:
- networking is usually simpler and more reliable when the driver is inside the same Kubernetes cluster

## Resource Requests and Limits
Kubernetes uses requests and limits for CPU and memory, and Spark has its own executor/driver memory model. These must align.

Why this matters:
- Spark may think an executor has enough memory, but the pod can still be OOM-killed if the Kubernetes memory limit is too low
- CPU throttling can reduce task throughput even if Spark looks correctly sized on paper

Important concepts:
- request: what the scheduler reserves
- limit: hard cap the container cannot exceed

Practical takeaway:
- Spark memory, memory overhead, and container limits must be sized together

## Memory Overhead on Kubernetes
Container memory use includes more than just JVM heap.

It can include:
- JVM heap
- off-heap memory
- Python worker memory
- native libraries
- memory overhead for shuffle, networking, and metadata

Why this matters:
- executor pods are commonly killed because total container memory exceeds the limit even when heap usage alone looks reasonable
- memory overhead settings are especially important for PySpark and shuffle-heavy workloads

Common symptom:
- pod `OOMKilled` in Kubernetes even though Spark logs suggest generic executor loss

## Dynamic Allocation
Dynamic allocation lets Spark add or remove executors based on workload demand. On Kubernetes, this translates into creating and deleting executor pods.

Benefits:
- better resource efficiency
- scale out during wide stages
- shrink during lighter phases

Operational tradeoffs:
- pod startup time can slow scale-out responsiveness
- executor churn can interact with shuffle and caching behavior
- cluster autoscaling and Spark dynamic allocation may amplify each other's delays

Practical takeaway:
- dynamic allocation works well when pod startup is reasonably fast and shuffle file availability is handled correctly

## Shuffle and Local Storage Concerns
Shuffle is especially sensitive on Kubernetes because executors often rely on ephemeral container-local storage unless persistent volumes or carefully designed storage strategies are used.

Why it matters:
- shuffle files may disappear when executor pods terminate
- disk pressure on nodes can cause eviction or degraded I/O
- local ephemeral storage can become a hidden bottleneck

Important operational concern:
- if executor churn is high, shuffle reliability depends on how the environment preserves or recomputes shuffle data

Practical rule:
- treat local disk and ephemeral storage as first-class resources for Spark on Kubernetes

## Pod Scheduling Realities
Spark can request executors, but Kubernetes may not schedule them immediately.

Common causes of pending executor pods:
- insufficient CPU or memory on nodes
- taints/tolerations mismatch
- node selector or affinity rules too restrictive
- cluster autoscaler lag
- quota limits

What this looks like from Spark:
- delayed executor registration
- stalled scale-out
- slower-than-expected stage startup

This is a key difference from reasoning only in Spark terms: sometimes the "Spark problem" is really a Kubernetes scheduling problem.

## Networking Constraints
Spark workloads can generate significant network traffic through:
- shuffle
- broadcast
- driver/executor coordination
- remote storage access

Kubernetes-specific issues include:
- network policies blocking needed traffic
- service discovery problems
- cross-zone latency
- container network overlay overhead

Practical takeaway:
- wide shuffles on Kubernetes are still wide shuffles, but now they also depend on the cluster network fabric and pod placement

## Images and Dependency Packaging
Spark on Kubernetes usually relies on container images to package runtime dependencies.

Why this matters:
- missing JARs, Python libraries, or Hadoop/cloud connectors become image problems
- large images increase startup time
- inconsistent images across environments create hard-to-debug runtime differences

Good practice:
- keep images reproducible
- include required dependencies explicitly
- avoid relying on ad hoc manual environment setup

## Logging and Observability
On Kubernetes, logs and diagnostics often span both Spark and Kubernetes tooling.

You may need:
- Spark UI
- driver logs
- executor pod logs
- pod events
- node-level signals such as disk or memory pressure

Why it matters:
- some failures appear in Spark as generic executor loss, but the real cause is visible only in Kubernetes events

Examples:
- `OOMKilled`
- pod eviction due to node disk pressure
- image pull failure
- pending pods from quota or scheduler constraints

## Common Failure Modes

### Executor pod OOMKilled
Symptoms:
- executors disappear abruptly
- task retries increase
- Kubernetes shows `OOMKilled`

Likely causes:
- memory overhead too low
- heavy shuffle or Python memory use
- broadcast or cache footprint too large

### Pending executor pods
Symptoms:
- application waits for resources
- fewer executors than requested
- long delay before stage parallelism ramps up

Likely causes:
- insufficient cluster capacity
- requests too large
- quota, affinity, or autoscaler delay

### Driver connectivity issues
Symptoms:
- executors fail to register
- executor/driver communication errors
- application starts but does not scale correctly

Likely causes:
- wrong driver service configuration
- DNS or networking issues
- network policies blocking traffic

### Local storage exhaustion
Symptoms:
- spill or shuffle failures
- pod eviction
- degraded task performance

Likely causes:
- insufficient ephemeral storage
- large shuffle writes
- oversized spills from memory pressure

## Tuning Levers

### Spark-side levers
- executor cores and memory
- driver memory and CPU
- shuffle partition sizing
- broadcast thresholds
- AQE and dynamic allocation settings

### Kubernetes-side levers
- CPU/memory requests and limits
- node pool sizing
- autoscaler behavior
- affinity, tolerations, and topology placement
- ephemeral storage sizing and volume strategy

Practical rule:
- tune Spark and Kubernetes together; fixing only one side often leaves the real bottleneck untouched

## What to Inspect When Jobs Are Slow
1. Check the Spark plan and stage metrics first.
2. Confirm executors are launching at the rate Spark expects.
3. Inspect pending pods, pod evictions, and `OOMKilled` events.
4. Look at shuffle-heavy stages for disk and network stress.
5. Verify driver connectivity and service configuration.
6. Compare Spark executor sizing with actual pod requests/limits.

## Common Misunderstandings
- "Spark on Kubernetes is just Spark with a different submit command"
  - The execution engine is Spark, but operational behavior depends heavily on Kubernetes scheduling, networking, and storage.

- "If pods are running, the job is healthy"
  - Pods may run while being CPU-throttled, memory-constrained, or unable to communicate correctly.

- "Executor memory setting alone controls memory risk"
  - Container limits, overhead memory, off-heap use, and Python memory all matter.

- "Dynamic allocation automatically saves money and improves performance"
  - It helps in many environments, but slow pod startup and executor churn can reduce the benefit.

## Interview Angle

### Good concise answer
- "Spark on Kubernetes runs the driver and executors as pods, so Spark planning still matters, but pod scheduling, container memory limits, networking, and local storage now directly affect job reliability and performance."

### Stronger follow-up answer
- "The main operational differences are that executor startup depends on Kubernetes scheduling, pod memory limits can cause `OOMKilled` failures, and shuffle plus ephemeral storage behavior become critical for reliability."

## Why It Matters
Understanding Spark on Kubernetes helps you:
- connect Spark performance issues with pod-level operational causes
- size executors and drivers correctly in containerized environments
- diagnose pod scheduling, network, and storage failures that look like generic Spark instability
- operate Spark in modern platform teams more confidently

## Related
- [[04-Data Engineering Library/Spark Deep Internals/AQE-Mechanics.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Shuffle-Fetch-Protocol.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Broadcast-Mechanics.md]]
- [[04-Data Engineering Library/Spark Deep Internals/Spark-Performance-Tuning-Guide.md]]
