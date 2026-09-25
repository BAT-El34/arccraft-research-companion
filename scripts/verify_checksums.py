"""Fail closed when any registered artifact is missing or changed."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'artifacts/manifest.json').read_text(encoding='utf-8'))
failures=[]
for record in manifest['artifacts']:
    path=(ROOT/record['artifact_id']).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():failures.append(record['artifact_id']);continue
    with path.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    if digest!=record['sha256'] or path.stat().st_size!=record['bytes']:failures.append(record['artifact_id'])
print(json.dumps({'checked':len(manifest['artifacts']),'failed':failures},indent=2))
raise SystemExit(1 if failures else 0)
