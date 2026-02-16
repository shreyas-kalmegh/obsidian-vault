# DDIA — Chapter 5: Replication

## Summary
Replication ensures multiple copies of data exist across machines to tolerate failures. Covers leader-follower, consensus protocols, and replication lag.

## Key points
- Synchronous vs asynchronous replication tradeoffs
- Replication lag & staleness
- Use cases: read scalability, fault tolerance

## Flashcards
Front:: What's the difference between synchronous and asynchronous replication?  
Back:: Synchronous commits on all replicas before acknowledging; asynchronous returns after leader commits.
