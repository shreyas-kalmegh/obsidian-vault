# Context (Token-Efficient Root Bootstrap)

## Purpose
This file defines how Codex should work in this vault without scanning the entire repository.

## Canonical entrypoint
- Read this file first.
- Read `AGENTS.md` second.
- Read only user-specified paths after that.

## Hard scan limits
1. Do not run full-repo discovery by default (`rg --files`, recursive `find`, global indexing).
2. Do not open unrelated folders "just in case."
3. If the user did not provide a target path, ask for one concise path clarification.
4. Expand scope only when the user explicitly says to scan broader areas.

## Allowed default behavior
- Read only:
  - `CONTEXT.md`
  - `AGENTS.md`
  - the exact files/directories explicitly mentioned by the user
- Keep edits constrained to the requested scope.

## Working contract for Codex threads
- Assume narrow scope unless user says otherwise.
- Prefer direct file opens over broad search.
- Summarize touched files at the end of each task.
- If broader context is required, request permission before scanning additional directories.

## Optional starter prompt for new Codex thread
```text
Read only CONTEXT.md and AGENTS.md first.
Then read only the exact file(s) or folder(s) I explicitly mention.
Do not scan the full repo or run broad discovery commands unless I ask.
```
