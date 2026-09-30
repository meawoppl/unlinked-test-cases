#!/usr/bin/env python3
"""Verify fixture integrity, or restore pinned upstream bytes without executing them."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MAX_RESOURCE_BYTES = 16 * 1024 * 1024
MAX_TOTAL_BYTES = 128 * 1024 * 1024


def resources(manifest):
    for document in manifest.get('provenance_documents', []):
        yield document['path'], document['sha256'], document['download_url']
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
    total_bytes = 0
    for relative, expected, url in resources(manifest):
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT):
            raise SystemExit(f'Unsafe manifest path: {relative}')
        if path.exists() and path.stat().st_size > MAX_RESOURCE_BYTES:
            raise SystemExit(f'Resource exceeds byte limit: {relative}')
        if url and not url.startswith('https://raw.githubusercontent.com/'):
            raise SystemExit(f'Unexpected upstream host: {relative}')
        if args.command == 'refresh' and url:
            # Only write bytes after verifying the pinned digest.
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read(MAX_RESOURCE_BYTES + 1)
            if len(data) > MAX_RESOURCE_BYTES:
                raise SystemExit(f'Download exceeds byte limit: {relative}')
            if hashlib.sha256(data).hexdigest() != expected:
                raise SystemExit(f'Upstream checksum mismatch: {relative}')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit(f'Missing or modified resource: {relative}')
        total_bytes += path.stat().st_size
        if total_bytes > MAX_TOTAL_BYTES:
            raise SystemExit('Corpus exceeds total byte limit')
        count += 1
    listed = {fixture['path'] for fixture in manifest['fixtures']}
    actual = {str(p.relative_to(ROOT)) for p in (ROOT / 'fixtures').rglob('*') if p.suffix in {'.m', '.mdl', '.slx'}}
    if listed != actual:
        raise SystemExit(f'Manifest mismatch: {listed ^ actual}')
    print(f'Verified {len(listed)} fixtures and {count} total resources; no imported code executed.')


if __name__ == '__main__':
    main()
