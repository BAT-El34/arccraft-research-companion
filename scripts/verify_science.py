"""Generate candidate golden outputs and verify registered evidence without overwriting it."""
import dataclasses, hashlib, importlib.metadata, json, platform, sys
from pathlib import Path
import numpy as np
import pandas as pd
from prepare_phase0 import ROOT, sha, write
sys.path.insert(0,str(ROOT))
from arccraft import engine as e
from arccraft.motor import arccraft_empirical_motor
from run_ablation import run_once, fingerprint

CHECKS=[]
def check(name,passed,detail=None):
    CHECKS.append({'name':name,'passed':bool(passed),'detail':detail})

def safe(obj):
    if isinstance(obj,dict):return {k:safe(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [safe(v) for v in obj]
    if isinstance(obj,float) and not np.isfinite(obj):return None
    if isinstance(obj,np.generic):return safe(obj.item())
    return obj

def canonical_bytes(obj):
    return json.dumps(safe(obj),sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()

def main():
    research=ROOT/'evidence/research'; replay=ROOT/'audit/replay'
    original=pd.read_csv(research/'25_ARCCRAFT_ABLATION_RESULTS.csv')
    rerun=pd.read_csv(replay/'25_ARCCRAFT_ABLATION_RESULTS.csv')
    check('15 registered fingerprints match original paper evidence',original.fingerprint.tolist()==rerun.fingerprint.tolist())
    check('15 same-seed fingerprint replays',len(rerun)==15 and rerun.exact_replay.all())
    deterministic=[c for c in original if not c.endswith('_seconds')]
    check('All non-timing ablation columns match',original[deterministic].equals(rerun[deterministic]))
    iso=pd.read_csv(replay/'27_STREAM_ISOLATION_TEST.csv')
    check('Isolation fingerprints match paper evidence',iso.equals(pd.read_csv(research/'27_STREAM_ISOLATION_TEST.csv')))
    seed=20260825
    metrics,results=run_once('full',seed)
    _,repeat=run_once('full',seed)
    payload=[dataclasses.asdict(x) for x in results]
    repeat_payload=[dataclasses.asdict(x) for x in repeat]
    raw_hash=hashlib.sha256(canonical_bytes(payload)).hexdigest()
    check('Canonical raw full precision serialization identical on repeat',canonical_bytes(payload)==canonical_bytes(repeat_payload))
    flux=e.construire_flux_nommes(seed); worlds=e.generer_mondes(flux['world'],n=10000); validation=e.valider_mondes(worlds)
    before={k:v.copy() for k,v in validation.etat_valide.items()}
    e.simuler_trajectoires(e.product,worlds,validation,flux['claims'],flux['behaviour'])
    check('Validator arrays immutable',all(np.array_equal(before[k],v,equal_nan=True) for k,v in validation.etat_valide.items()))
    check('Canonical PASS REPAIR REJECT counts',[metrics[k] for k in ['pass_worlds','repair_worlds','reject_worlds']]==[8037,1958,5])
    atlas=e.construire_failure_atlas(results,seed,e.decrire_flux_nommes(flux))
    check('Atlas includes 3588 traceability, one ratio failure and five rejects',len(atlas)==3594 and metrics['traceability_failures']==3588 and metrics['combined_ratio_failures']==1)
    check('Atlas JSON strict',bool(json.loads(canonical_bytes(atlas))))
    reverse=e.recherche_stress_inverse(e.product,seed)
    check('Reverse stress matches manuscript rounding',reverse['world_id_perturbation']==196 and round(reverse['distance_standardisee'],4)==1.0123 and round(reverse['combined_ratio'],4)==.4017 and round(reverse['tracabilite_score'],4)==.9321)
    _,other=run_once('full',314159)
    atlas_other=e.construire_failure_atlas(other,314159,e.decrire_flux_nommes(e.construire_flux_nommes(314159)))
    check('Atlas records actual nondefault seed',len(atlas_other)>0 and all(x['seed_master']==314159 for x in atlas_other))
    write(ROOT/'artifacts/candidate/canonical-worlds.json',safe(payload))
    write(ROOT/'artifacts/candidate/failure-atlas.json',safe(atlas))
    classes=e.agreger_par_classe(results)
    pd.DataFrame([{'scenario_class':k,**v} for k,v in classes.items()]).to_csv(ROOT/'artifacts/candidate/scenario-classes-10000.csv',index=False)
    write(ROOT/'artifacts/candidate/reverse-stress.json',reverse)
    pd.DataFrame([{'failure_gate':k,'count':v} for k,v in e.synthese_failure_atlas(atlas).items()]).to_csv(ROOT/'artifacts/candidate/failure-atlas-counts-10000.csv',index=False)
    expected=pd.read_csv(research/'11_STRESS_SURFACE_RESULTS.csv')
    stress=[]
    for i,fm in enumerate([.75,1.,1.25,1.5,1.75]):
        for j,sm in enumerate([.75,1.,1.25,1.5,1.75]):
            result=arccraft_empirical_motor(n_simulations=20000,seed=10000+i*100+j,frequency_multiplier=fm,severity_multiplier=sm)
            lr=result['predicted_loss_ratio']
            row={'frequency_multiplier':fm,'severity_multiplier':sm,'mean_loss_ratio':lr['mean'],'q025':lr['q025'],'q975':lr['q975']}
            stress.append(row)
    stress=pd.DataFrame(stress)
    check('25 registered motor stress means and intervals',np.allclose(stress.to_numpy(),expected[stress.columns].to_numpy(),rtol=1e-12,atol=1e-12),{'rtol':1e-12,'atol':1e-12})
    stress.to_csv(ROOT/'artifacts/candidate/stress-surface.csv',index=False)
    motor=arccraft_empirical_motor(n_simulations=50000,seed=42)
    write(ROOT/'artifacts/candidate/motor-forecast.json',motor)
    original_rolling=pd.read_csv(research/'09_ROLLING_ORIGIN_RESULTS.csv').iloc[-1]
    check('Motor registered 2024 forecast',np.isclose(motor['predicted_claim_count']['mean'],original_rolling.predicted_claims,rtol=0,atol=1e-9) and np.isclose(motor['predicted_incurred']['mean'],original_rolling.predicted_incurred,rtol=0,atol=1e-7))
    check('2024 observed counts and incurred',[motor['validation']['observed_claims'],motor['validation']['observed_incurred']]==[39276.,38106351.28])
    check('Partial external validation remains explicit',not motor['validation']['observed_claims_in_95_interval'] and not motor['validation']['observed_incurred_in_95_interval'] and motor['combined_ratio'] is None)
    runtime={'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'architecture':platform.machine(),'dependencies':{p:importlib.metadata.version(p) for p in ['numpy','pandas','scipy','matplotlib','fastapi','nbclient','nbformat']}}
    write(ROOT/'audit/runtime.json',runtime)
    summary={'status':'PASS' if all(c['passed'] for c in CHECKS) else 'FAIL','checks':CHECKS,'canonical_fingerprint_rounded_12':fingerprint(results),'canonical_raw_semantic_sha256':raw_hash,
        'engine_sha256':sha(ROOT/'arccraft/engine.py'),'runtime':runtime,'timing_policy':'Original observed timings are historical evidence. New wall times are not equality targets and ran under concurrent audit load.',
        'fingerprint_contract':'Historical paper SHA-256 rounds combined_ratio and tracabilite_score to 12 decimal places; raw full precision equality separately tested for the canonical run only.'}
    write(ROOT/'audit/scientific-checks.json',summary)
    print(json.dumps({k:summary[k] for k in ['status','checks','canonical_fingerprint_rounded_12']},indent=2))
    raise SystemExit(0 if summary['status']=='PASS' else 1)

if __name__=='__main__':main()
