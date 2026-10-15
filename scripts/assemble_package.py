#!/usr/bin/env python3
"""Reassemble the release ZIP and verify its SHA-256, without extra dependencies."""
from pathlib import Path
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'package-parts/manifest.json').read_text())
out = ROOT / manifest['filename']
temporary = out.with_suffix(out.suffix + '.tmp')
full_hash = hashlib.sha256()
try:
    with temporary.open('wb') as target:
        for item in manifest['parts']:
            path = ROOT / 'package-parts' / item['name']
            data = path.read_bytes()
            if len(data) != item['size'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise ValueError(f'Part verification failed: {path.name}')
            target.write(data)
            full_hash.update(data)
    if temporary.stat().st_size != manifest['size'] or full_hash.hexdigest() != manifest['sha256']:
        raise ValueError('Complete ZIP verification failed')
    os.replace(temporary, out)
except Exception:
    temporary.unlink(missing_ok=True)
    raise
print(f'Verified package: {out.name} ({out.stat().st_size} bytes)')
