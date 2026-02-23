# Medallion Architecture

## Layers
- Bronze: raw ingestion, minimally transformed
- Silver: cleaned, standardized, deduplicated
- Gold: business-ready marts and dimensional models

## Senior Focus
- Make pipelines idempotent
- Handle schema evolution safely
- Keep lineage from Bronze to Gold

## Checklist
- [ ] Layer contracts documented
- [ ] Quality checks per layer
- [ ] Replay/backfill approach defined

## Common Mistakes
- Mixing business metrics in Silver
- Skipping reproducibility for backfills

## Interview Prompts
- How do you map Medallion to Kimball dimensions/facts?

## Related Notes
- [[gold-layer-dimensional-models]]
- [[cdc-and-incremental-modeling]]
