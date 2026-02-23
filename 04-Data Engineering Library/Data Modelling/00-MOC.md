# Data Modelling MOC

## How to Use
- Start at [[00-Roadmap]].
- Use this page as a quick jump index by topic.
- Track progress with the Status column.

## Core Concepts
| Topic | Note | Why It Matters | Status |
|---|---|---|---|
| Grain | [[01-Core-Concepts/grain|grain]] | Prevents metric ambiguity and double-counting | Not Started |
| Facts vs Dimensions | [[01-Core-Concepts/facts-vs-dimensions|facts-vs-dimensions]] | Correct analytical modeling boundaries | Not Started |
| Fact Table Types | [[01-Core-Concepts/fact-table-types|fact-table-types]] | Align table design with query patterns | Not Started |
| SCD Types | [[01-Core-Concepts/scd-types|scd-types]] | Handle dimension change history correctly | Not Started |
| Surrogate vs Natural Keys | [[01-Core-Concepts/surrogate-vs-natural-keys|surrogate-vs-natural-keys]] | Stable joins and versioning strategy | Not Started |

## Kimball
| Topic | Note | Why It Matters | Status |
|---|---|---|---|
| Kimball Principles | [[02-Kimball/kimball-principles|kimball-principles]] | End-to-end dimensional modeling method | Not Started |
| Conformed Dimensions | [[02-Kimball/conformed-dimensions|conformed-dimensions]] | Metric consistency across marts | Not Started |
| Bus Matrix | [[02-Kimball/bus-matrix|bus-matrix]] | Delivery planning and model coverage | Not Started |
| Star vs Snowflake | [[02-Kimball/star-vs-snowflake|star-vs-snowflake]] | Performance vs normalization tradeoff | Not Started |

## Modern Lakehouse
| Topic | Note | Why It Matters | Status |
|---|---|---|---|
| Medallion Architecture | [[03-Modern-Lakehouse/medallion-architecture|medallion-architecture]] | Layered reliability and maintainability | Not Started |
| CDC and Incremental | [[03-Modern-Lakehouse/cdc-and-incremental-modeling|cdc-and-incremental-modeling]] | Scalable low-latency updates | Not Started |
| Late-Arriving Data | [[03-Modern-Lakehouse/late-arriving-data|late-arriving-data]] | Correctness under delayed events | Not Started |
| Gold Layer Models | [[03-Modern-Lakehouse/gold-layer-dimensional-models|gold-layer-dimensional-models]] | Business-ready serving models | Not Started |

## Advanced
| Topic | Note | Why It Matters | Status |
|---|---|---|---|
| Data Vault vs Kimball | [[04-Advanced/data-vault-vs-kimball|data-vault-vs-kimball]] | Architecture pattern selection | Not Started |
| Semantic Layer | [[04-Advanced/semantic-layer|semantic-layer]] | Metric consistency and governance | Not Started |
| Performance and Cost | [[04-Advanced/performance-and-cost|performance-and-cost]] | Practical production optimization | Not Started |
| Governance and Lineage | [[04-Advanced/governance-and-lineage|governance-and-lineage]] | Trust, ownership, and compliance | Not Started |

## Interview Prep
| Topic | Note | Why It Matters | Status |
|---|---|---|---|
| Scenario Questions | [[90-Interview-Prep/scenario-questions|scenario-questions]] | Practice senior-level reasoning | Not Started |
| Design Case Studies | [[90-Interview-Prep/design-case-studies|design-case-studies]] | Structured architecture storytelling | Not Started |
| Anti-Patterns | [[90-Interview-Prep/anti-patterns|anti-patterns]] | Spot risks and propose fixes quickly | Not Started |

## Related Notes
- [[00-Roadmap]]
