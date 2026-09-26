import argparse, concurrent.futures, hashlib, json, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
registry=json.loads((ROOT/'artifacts/web-registry.json').read_text(encoding='utf-8'))
for row in registry['artifacts']:
    assert row['science_commit'] and row['version'] and row['proof_status'] and row['license']
    for p in [ROOT/row['path'],ROOT/'public'/row['url'].lstrip('/')]:
        assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],str(p)
assert registry['release_status']!='PUBLISHED' or registry['archive_doi']
print(f"PASS: {len(registry['artifacts'])} source/download byte checksums and provenance records")

# Deployment exclusions can remove nested public copies even when local checks pass.
parser=argparse.ArgumentParser()
parser.add_argument('--base-url',help='Verify every registered download on this deployment as well.')
args=parser.parse_args()
if args.base_url:
    def verify_remote(row):
        url=args.base_url.rstrip('/')+row['url']
        with urllib.request.urlopen(url,timeout=45) as response:
            actual=hashlib.sha256(response.read()).hexdigest()
        assert actual==row['sha256'],f'Remote checksum mismatch: {url}'
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(verify_remote,registry['artifacts']))
    print(f"PASS: {len(registry['artifacts'])} remote download checksums at {args.base_url}")
