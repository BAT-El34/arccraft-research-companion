"""Bounded public computations with evidence capture; no deployment changes."""
import json, sys, urllib.request, datetime, importlib.util
from prepare_phase0 import ROOT, LEGACY, sha, write

sys.path.insert(0,str(LEGACY))
from backend.model_service import arccraft_synthetic

def request(route,payload=None):
    req=urllib.request.Request('https://actuarial-digital-dashboard-rd-v3.vercel.app'+route,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={'Content-Type':'application/json','User-Agent':'ARCCRAFT-phase0-reproducibility-audit'})
    with urllib.request.urlopen(req,timeout=60) as response:
        raw=response.read()
        return {'status':response.status,'url':response.url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'headers':dict(response.headers),'body':json.loads(raw)}

def main():
    local=arccraft_synthetic(100,20260825)
    write(ROOT/'audit/public/local-100.json',local)
    spec=importlib.util.spec_from_file_location('audit_base_engine',ROOT/'.audit-private/base_engine.py')
    base=importlib.util.module_from_spec(spec); sys.modules[spec.name]=base; spec.loader.exec_module(base)
    flux=base.construire_flux_nommes(20260825); worlds=base.generer_mondes(flux['world'],n=100)
    validation=base.valider_mondes(worlds)
    results=base.simuler_trajectoires(base.product,worlds,validation,flux['claims'],flux['behaviour'])
    base_out={'reverse_stress':base.recherche_stress_inverse(base.product,flux),
        'failure_atlas_summary':base.synthese_failure_atlas(base.construire_failure_atlas(results,{k:k for k in flux})),
        'top_correlations':[{'variable':k,'rho_rank':v} for k,v in list(base.cribler_variables(results,worlds,validation).items())[:10]],
        'scenario_classes':base.agreger_par_classe(results)}
    write(ROOT/'audit/public/base-100.json',base_out)
    try:
        health=request('/api/health'); write(ROOT/'audit/public/health.json',health)
        public=request('/api/arccraft/simulate',{'n_worlds':100,'seed':20260825})
        write(ROOT/'audit/public/public-100.json',public)
        compare={'public_commit':'NOT_EXPOSED','base_commit':'b3df670227efa4aecf5383979b90f3eab15ae528',
            'public_matches_base':{k:public['body'][k]==v for k,v in base_out.items()},
            'public_matches_local':{k:public['body'][k]==local[k] for k in base_out},
            'reverse_public':public['body']['reverse_stress'],'reverse_base':base_out['reverse_stress'],'reverse_local':local['reverse_stress'],
            'scope':'100 worlds, seed 20260825; behavioural agreement cannot establish deployed source SHA.'}
    except Exception as e: compare={'error':str(e),'scope':'Public verification incomplete'}
    write(ROOT/'audit/public/reconciliation.json',compare); print(json.dumps(compare,indent=2))

if __name__=='__main__':main()
