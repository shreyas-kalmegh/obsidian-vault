#!/usr/bin/env python3
"""
master_to_vault.py (final, improved)

Converts a single master markdown file containing many ---FILE: <path> blocks
into an Obsidian-ready vault folder.

Features:
- Supports text blocks started with ---FILE: <path>
- Supports binary blocks started with ---FILE-BINARY: <path>, <line_count>
  where the next <line_count> lines are base64 and followed by ---END_FILE---
- Preserves UTF-8, normalizes newlines to LF
- Optional --overwrite to replace existing files
- Optional --dry-run to report actions without writing
- Optional --obsidian to create a minimal .obsidian config and recommended plugins list
- Optional --progress to print per-file creation messages
- Optional --map to apply link mapping (TSV: source<TAB>target)
- Handles duplicate target paths and reports them
- Creates directories as needed
- Safe: will not overwrite files unless --overwrite is set

Usage:
    python3 master_to_vault.py master.md outdir [--overwrite] [--dry-run] [--obsidian] [--map linkmap.tsv] [--progress]

Author: Generated for Personal Knowledge System
"""

import re
import sys
import argparse
from pathlib import Path
import base64
import csv
import os

FILE_START_RE = re.compile(r'^---FILE:\s*(.+)\s*$')
FILE_BINARY_START_RE = re.compile(r'^---FILE-BINARY:\s*(.+),\s*(\d+)\s*$')
FILE_END_MARKER = '---END_FILE---'

def sanitize_relpath(p: str) -> str:
    # Normalize path to POSIX style and strip leading/trailing spaces
    pp = p.strip().replace('\\', '/')
    # Avoid absolute paths
    if pp.startswith('/') or (len(pp) > 1 and pp[1] == ':'):
        pp = pp.replace(':', '')
        pp = pp.lstrip('/\\')
    # Prevent path traversal
    pp = str(PurePosixPath(pp))
    if pp.startswith('..'):
        raise ValueError(f"Refusing path traversal in file path: {p}")
    return pp

def load_link_map(mapfile: Path):
    mapping = {}
    if not mapfile.exists():
        return mapping
    with mapfile.open('r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) >= 2:
                mapping[row[0].strip()] = row[1].strip()
    return mapping

def apply_link_map(content: str, mapping: dict):
    if not mapping:
        return content
    # Replace wikilinks [[Key]] with mapped path if present
    def repl(m):
        key = m.group(1).strip()
        return "[[" + mapping.get(key, key) + "]]"
    return re.sub(r'\[\[([^\]]+)\]\]', repl, content)

def parse_master(master_text: str):
    """
    Yields tuples: (type, relpath, payload)
    type: 'text' or 'binary'
    relpath: relative target path (POSIX)
    payload: for text -> content str, for binary -> base64 str
    """
    lines = master_text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m_bin = FILE_BINARY_START_RE.match(line)
        if m_bin:
            relpath = sanitize_relpath(m_bin.group(1))
            line_count = int(m_bin.group(2))
            i += 1
            b64_lines = []
            for _ in range(line_count):
                if i >= n:
                    raise ValueError(f"Unexpected EOF in binary block for {relpath}")
                b64_lines.append(lines[i])
                i += 1
            if i >= n or lines[i].strip() != FILE_END_MARKER:
                raise ValueError(f"Missing {FILE_END_MARKER} after binary block {relpath}")
            i += 1
            yield ('binary', relpath, '\n'.join(b64_lines))
            continue

        m = FILE_START_RE.match(line)
        if not m:
            i += 1
            continue
        relpath = sanitize_relpath(m.group(1))
        i += 1
        content_lines = []
        while i < n and lines[i].strip() != FILE_END_MARKER:
            content_lines.append(lines[i])
            i += 1
        if i >= n:
            raise ValueError(f"Missing {FILE_END_MARKER} for file block starting with: {relpath}")
        i += 1
        content = "\n".join(content_lines).rstrip() + "\n"
        yield ('text', relpath, content)

def write_files(blocks, out_root: Path, overwrite=False, dry_run=False, link_map=None, progress=False):
    created = []
    skipped = []
    errors = []
    seen = set()
    for btype, relpath, payload in blocks:
        target = out_root / relpath
        if str(target) in seen:
            errors.append(f"Duplicate target path detected: {relpath}")
            continue
        seen.add(str(target))
        if btype == 'binary':
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and not overwrite:
                skipped.append(str(target))
                if progress:
                    print(f"SKIP (exists): {target}")
                continue
            if dry_run:
                created.append(str(target))
                if progress:
                    print(f"DRY (binary): {target}")
                continue
            try:
                with target.open('wb') as f:
                    f.write(base64.b64decode(payload.encode('utf-8')))
                created.append(str(target))
                if progress:
                    print(f"CREATED (binary): {target}")
            except Exception as e:
                errors.append(f"Error writing binary {target}: {e}")
            continue
        # text
        content = payload
        if link_map:
            content = apply_link_map(content, link_map)
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not overwrite:
            skipped.append(str(target))
            if progress:
                print(f"SKIP (exists): {target}")
            continue
        if dry_run:
            created.append(str(target))
            if progress:
                print(f"DRY (text): {target}")
            continue
        try:
            with target.open('w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            created.append(str(target))
            if progress:
                print(f"CREATED (text): {target}")
        except Exception as e:
            errors.append(f"Error writing file {target}: {e}")
    return created, skipped, errors

def create_obsidian_stub(out_root: Path):
    obs = out_root / ".obsidian"
    obs.mkdir(parents=True, exist_ok=True)
    (obs / "config").write_text("{}", encoding='utf-8')
    # recommended plugins list (manifest only)
    plugins = {
        "plugins.json": {
            "recommended": [
                "templater",
                "dataview",
                "obsidian-spaced-repetition",
                "calendar",
                "daily-notes"
            ]
        }
    }
    try:
        import json
        for fname, obj in plugins.items():
            (obs / fname).write_text(json.dumps(obj, indent=2), encoding='utf-8')
    except Exception:
        # fallback simple file
        (obs / "plugins-recommended.txt").write_text("\\n".join(plugins["plugins.json"]["recommended"]), encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description='Convert master markdown to Obsidian vault folder.')
    parser.add_argument('master', help='Master markdown file (input)')
    parser.add_argument('outdir', help='Output vault directory (created if missing)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files')
    parser.add_argument('--dry-run', action='store_true', help='Do not write files, show what would be done')
    parser.add_argument('--obsidian', action='store_true', help='Create minimal .obsidian folder with recommended plugins')
    parser.add_argument('--map', help='Optional tab-separated link mapping file (source<TAB>target)', default=None)
    parser.add_argument('--progress', action='store_true', help='Show progress for each file')
    args = parser.parse_args()

    master_path = Path(args.master)
    if not master_path.exists():
        print(f"Error: master file {master_path} not found.", file=sys.stderr)
        sys.exit(2)

    out_root = Path(args.outdir)
    out_root.mkdir(parents=True, exist_ok=True)

    link_map = {}
    if args.map:
        link_map = load_link_map(Path(args.map))
        print(f"Loaded link map with {len(link_map)} entries.")

    text = master_path.read_text(encoding='utf-8')
    blocks = list(parse_master(text))
    if not blocks:
        print("No file blocks found in master file. Make sure you use ---FILE: path markers.", file=sys.stderr)
        sys.exit(3)

    created, skipped, errors = write_files(blocks, out_root, overwrite=args.overwrite, dry_run=args.dry_run, link_map=link_map, progress=args.progress)

    print(f"Completed conversion. Created {len(created)} files, skipped {len(skipped)} existing files, errors: {len(errors)}")
    if created:
        print("Example created files:")
        for p in created[:40]:
            print("  ", p)
    if skipped:
        print("Example skipped files:")
        for p in skipped[:40]:
            print("  ", p)
    if errors:
        print("Errors:")
        for e in errors[:20]:
            print("  ", e)

    if args.obsidian and not args.dry_run:
        create_obsidian_stub(out_root)
        print("Created .obsidian stub with recommended plugins.")

if __name__ == '__main__':
    main()
