"""Portable canonical replay. Does not overwrite golden artifacts. Requires only NumPy."""
import dataclasses, hashlib, json, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from arccraft import engine

def normalize(value):
    if isinstance(value,dict):return {k:normalize(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [normalize(v) for v in value]
    if isinstance(value,float) and not np.isfinite(value):return None
    return value

def main():
    manifest=json.loads((ROOT/'artifacts/manifest.json').read_text(encoding='utf-8'))
    actual_engine=hashlib.sha256((ROOT/'arccraft/engine.py').read_bytes()).hexdigest()
    if actual_engine!=manifest['engine_sha256']:raise ValueError('Scientific engine differs from recorded candidate')
    streams=engine.construire_flux_nommes(20260825)
    worlds=engine.generer_mondes(streams['world'],n=10000)
    validation=engine.valider_mondes(worlds)
    results=engine.simuler_trajectoires(engine.product,worlds,validation,streams['claims'],streams['behaviour'])
    payload=normalize([dataclasses.asdict(x) for x in results])
    raw=json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
    digest=hashlib.sha256(raw).hexdigest()
    expected=manifest['canonical_full_precision_semantic_sha256']
    receipt={'mode':'LOCAL_CANDIDATE_REPLAY','published':False,'matches_full_precision_golden':digest==expected,
        'source_commit':manifest['source_commit'],'engine_sha256':actual_engine,'output_semantic_sha256':digest,
        'master_seed':20260825,'worlds':10000,'named_streams':engine.decrire_flux_nommes(streams),
        'python':sys.version,'numpy':np.__version__,'warning':'Local computational verification does not establish empirical validation.'}
    print(json.dumps(receipt,indent=2,allow_nan=False))
    raise SystemExit(0 if digest==expected else 1)

if __name__=='__main__':main()
