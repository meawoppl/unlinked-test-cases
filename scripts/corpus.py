#!/usr/bin/env python3
"""Verify fixture integrity, or restore pinned upstream bytes without executing them."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def resources(manifest):
    for source in manifest['sources'].values():
        yield source['license_path'], source['license_sha256'], source['license_url']
    for fixture in manifest['fixtures']:
        yield fixture['path'], fixture['sha256'], fixture['download_url']
        if fixture['expected_outputs']:
            expected = fixture['expected_outputs']
            yield expected['path'], expected['sha256'], None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['verify', 'refresh'])
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    count = 0
    for relative, expected, url in resources(manifest):
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT):
            raise SystemExit(f'Unsafe manifest path: {relative}')
        if args.command == 'refresh' and url:
            # Only write bytes after verifying the pinned digest.
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read(16 * 1024 * 1024 + 1)
            if hashlib.sha256(data).hexdigest() != expected:
                raise SystemExit(f'Upstream checksum mismatch: {relative}')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit(f'Missing or modified resource: {relative}')
        count += 1
    listed = {fixture['path'] for fixture in manifest['fixtures']}
    actual = {str(p.relative_to(ROOT)) for p in (ROOT / 'fixtures').rglob('*') if p.suffix in {'.m', '.mdl', '.slx'}}
    if listed != actual:
        raise SystemExit(f'Manifest mismatch: {listed ^ actual}')
    print(f'Verified {len(listed)} fixtures and {count} total resources; no imported code executed.')


if __name__ == '__main__':
    main()
