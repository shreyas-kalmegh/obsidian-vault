# Data Modelling Context (Low-Token Bootstrap)

## Scope
This folder contains structured notes for dimensional modeling:
- `01-Core-Concepts`
- `02-Kimball`
- `03-Modern-Lakehouse`
- `04-Advanced`
- `90-Interview-Prep`

## Authoring Goal
- Medium depth, practical, interview + real-world useful
- Not a cheatsheet
- Include examples where useful (SQL, schema snippets, scenarios)

## Writing Style
- Use clear sections: `Overview`, key concepts, examples, mistakes, checklist
- Prefer concise, high-signal bullets over long prose
- Keep terminology consistent across files

## Canonical Concepts to Keep Consistent
- Grain-first modeling
- Facts vs dimensions separation
- Conformed dimensions across marts
- SCD choice per attribute (not blindly per table)
- Medallion contracts: Bronze (raw), Silver (canonical), Gold (business)
- Incremental + replay/backfill design for reliability

## Important Cross-Links
- `01-Core-Concepts/grain.md`
- `01-Core-Concepts/scd-types.md`
- `02-Kimball/kimball-principles.md`
- `03-Modern-Lakehouse/medallion-architecture.md`
- `03-Modern-Lakehouse/late-arriving-data.md`

## Session Bootstrap Prompt (Copy/Paste)
```text
Read only:
- 04-Data Engineering Library/Data Modelling/CONTEXT.md
- notes/session-handoff.md
- files I mention next

Task scope is only inside:
04-Data Engineering Library/Data Modelling

Do not scan the full repo unless needed.
Keep edits medium-depth with practical examples (not cheatsheet style).
```

## Handoff Reminder
At end of session, update `notes/session-handoff.md` with:
- objective
- files changed
- open questions
- next steps
