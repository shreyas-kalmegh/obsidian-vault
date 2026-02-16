# DDIA — Chapter 3: Storage & Retrieval

## Summary
Examines storage engines, indexing, B-Trees, LSM trees, and access patterns.

## Key concepts
- B-Tree: balanced tree for reads/writes; used in many databases.
- LSM-tree: optimized for high write throughput by sequential writes to logs.
- Storage vs retrieval tradeoffs: memory indexing vs disk IO.

## Flashcards
Front:: When is an LSM tree a better fit than a B-Tree?  
Back:: When the workload is write-heavy and can benefit from sequential writes and compaction.

## Related notes
- [[03-Technical Knowledge Base/Data Structures/LSM Trees - Overview.md]]
- [[03-Technical Knowledge Base/Data Structures/B-Tree - Overview.md]]
