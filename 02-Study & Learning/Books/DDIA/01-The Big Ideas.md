# DDIA — Chapter 1: The Big Ideas

## Summary
This chapter introduces the central themes of the book:
- Reliable systems, scalable systems, simple systems.
- Data systems trade-offs: consistency vs availability, latency vs throughput.
- Separation between storage and processing.

## Key Concepts
- Reliability: correctness in presence of failures.
- Scalability: ability to handle growth cheaply.
- Simplicity: maintainability and understandability.
- Latency vs throughput tradeoff.

## My notes (interpreted)
- Building a mental hierarchy: start with simple, then reliable, then scalable.
- Many engineering decisions are about trade-offs, not absolutes.

## Flashcards
Front:: What are the three big themes Kleppmann uses to categorize data systems?  
Back:: Reliability, Scalability, Simplicity.

Front:: Why separate storage and processing?  
Back:: To allow different engines to optimize for different workloads and scale independently.

## Related atomic notes
- [[03-Technical Knowledge Base/Distributed Systems/CAP Theorem.md]]
- [[04-Data Engineering Library/Processing/Batch vs Streaming - Core Differences.md]]
