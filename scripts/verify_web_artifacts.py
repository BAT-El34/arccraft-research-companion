import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
registry=json.loads((ROOT/'artifacts/web-registry.json').read_text(encoding='utf-8'))
for row in registry['artifacts']:
    assert row['science_commit'] and row['version'] and row['proof_status'] and row['license']
    for p in [ROOT/row['path'],ROOT/'public'/row['url'].lstrip('/')]:
        assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],str(p)
assert registry['release_status']!='PUBLISHED' or registry['archive_doi']
print(f"PASS: {len(registry['artifacts'])} source/download byte checksums and provenance records")
