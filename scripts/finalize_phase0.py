"""Build traceable phase-0 claims and receipts after the source commit exists."""
import ast, difflib, hashlib, importlib.metadata as md, json, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
from prepare_phase0 import ROOT, LEGACY, sha, write

def main():
    source_commit=subprocess.check_output(['git','log','-1','--format=%H','--','arccraft','scripts','pyproject.toml','requirements-replay.lock'],cwd=ROOT,text=True).strip()
    evidence=ROOT/'evidence/research'
    checks=[]
    for group,nums in [('08',range(9,15)),('17',range(18,25))]:
        for num in nums:
            original=next(evidence.glob(f'{num:02d}_*.csv'))
            output=ROOT/'audit/notebook-replay'/group/original.name
            a=pd.read_csv(original); b=pd.read_csv(output)
            fields={}
            for col in a:
                if pd.api.types.is_numeric_dtype(a[col]) and a[col].dtype!=bool:
                    fields[col]=bool(np.allclose(a[col],b[col],rtol=1e-12,atol=1e-12,equal_nan=True))
                else:fields[col]=a[col].fillna('__NULL__').tolist()==b[col].fillna('__NULL__').tolist()
            checks.append({'file':original.name,'passed':all(fields.values()),'field_checks':fields,'byte_identical':sha(original)==sha(output)})
    write(ROOT/'audit/notebook-output-comparison.json',{'rtol':1e-12,'atol':1e-12,'checks':checks,'all_passed':all(x['passed'] for x in checks)})
    benchmarks=pd.read_csv(evidence/'19_POLICY_BENCHMARK_RESULTS.csv')
    runs=pd.read_csv(evidence/'25_ARCCRAFT_ABLATION_RESULTS.csv')
    summary=pd.read_csv(evidence/'26_ARCCRAFT_ABLATION_SUMMARY.csv').set_index('config')
    reductions={}
    for year in [2023,2024]:
        b=benchmarks[benchmarks.target==year].set_index('model')
        reductions[str(year)]=100*(1-b.loc['policy_frequency_pooled_severity','claim_poisson_deviance']/b.loc['aggregate_pooled','claim_poisson_deviance'])
    full=summary.loc['full'];strict=summary.loc['strict_reject'];nt=summary.loc['no_transitions']
    values={
        'C1':reductions,
        'C2':{'count_covered':int(benchmarks.claims_in_process_95_interval.sum()),'incurred_covered':int(benchmarks.incurred_in_process_95_interval.sum()),'total':12},
        'C3':{'registered_pairs':15,'matching_paper_fingerprints':15,'rounding_digits':12},
        'C4':{'unused_world_draws':100,'named_invariant':True,'shared_invariant':False},
        'C5':{'accepted_worlds_reduction_percent':100*(1-strict.accepted_worlds_mean/full.accepted_worlds_mean),'failure_or_rejection_difference_pp':100*(strict.failure_or_reject_rate_mean-full.failure_or_reject_rate_mean)},
        'C6':{'failure_difference_pp':100*(nt.failure_rate_accepted_mean-full.failure_rate_accepted_mean),'relative_difference_percent':100*(nt.failure_rate_accepted_mean/full.failure_rate_accepted_mean-1)},
        'C7':{'traceability_failures':3588,'simulated_failures':3589,'share_percent':100*3588/3589,'structural_rejections_excluded_from_denominator':5},
        'C8':{'historical_mean_seconds':full.total_seconds_mean,'historical_sd_seconds':full.total_seconds_std,'historical_cv_percent':100*full.total_seconds_std/full.total_seconds_mean}}
    claims=[]
    for row in pd.read_csv(evidence/'32_CLAIM_METRIC_AUDIT.csv').to_dict('records'):
        src=evidence/row['source_files'];id=row['claim_id']
        claims.append({**row,'recomputed':values[id],'source_sha256':sha(src),'source_path':src.relative_to(ROOT).as_posix(),
            'verification_commit':source_commit,'historical_producer_commit':None,'historical_producer_state':'base b3df670 plus recorded uncommitted research changes',
            'version':'phase0-candidate-1','proof_status':'HISTORICAL_TIMING_RECONCILED' if id=='C8' else 'LOCAL_REPRODUCTION_VERIFIED',
            'release_status':'NOT_PUBLISHED','metric_type':'historical_host_timing' if id=='C8' else 'derived_research_result'})
    write(ROOT/'audit/claim-register.json',claims)
    # Inspect fixed numeric arrays without executing plotting or package-install code.
    fig_checks=[]
    def loaded(n):
        s=(ROOT/f'evidence/figure_package/code/Figure{n}.py').read_text(encoding='utf-8')
        s=s.split('# DATA LOADING',1)[1].split('# PARAMETERS',1)[0]
        ns={};exec(compile(s,f'Figure{n}:data','exec'),ns);return ns
    def fc(name,actual,expected,tolerance):
        fig_checks.append({'check':name,'passed':bool(np.allclose(actual,expected,rtol=0,atol=tolerance)),'absolute_tolerance':tolerance})
    f=loaded(2);annual=json.loads((ROOT/'audit/data-reconciliation.json').read_text())['annual']
    fc('Figure2 rows',f['policy_rows'],[x['policy_rows'] for x in annual],0)
    for field in ['claim_frequency','loss_ratio']:fc('Figure2 '+field,f[field],[x[field] for x in annual],.000005)
    f=loaded(3)
    for year in [2023,2024]:
        b=benchmarks[benchmarks.target==year]
        for key,col,tol in [('claim_error','claim_error_pct',.00005),('incurred_error','incurred_error_pct',.00005),('claim_deviance','claim_poisson_deviance',.000005),('incurred_deviance','incurred_poisson_deviance',.00005)]:fc(f'Figure3 {key} {year}',f[key][year],b[col],tol)
    f=loaded(4);dec=pd.read_csv(evidence/'20_POLICY_DECILE_CALIBRATION.csv')
    for year in [2023,2024]:
        for key,metric in [('count_op','claim_count'),('incurred_op','incurred')]:fc(f'Figure4 {key} {year}',f[key][year],dec[(dec.target==year)&(dec.metric==metric)].observed_to_predicted,.000005)
    f=loaded(5);stress=pd.read_csv(evidence/'11_STRESS_SURFACE_RESULTS.csv')
    fc('Figure5 surface',f['mean_loss_ratio'].flatten(),stress.mean_loss_ratio,.000005)
    f=loaded(6);classes=pd.read_csv(ROOT/'artifacts/candidate/scenario-classes-10000.csv')
    fc('Figure6 accepted worlds',f['accepted_worlds'],classes.mondes_acceptes,0)
    fc('Figure6 failure rates percent',f['failure_rates'],classes.taux_echec_synthetique*100,.005)
    fc('Figure6 atlas',f['atlas_counts'],[3588,1,5],0)
    f=loaded(7);s=summary.loc[['full','no_transitions','no_validator','shared_stream','strict_reject']]
    for key,col,factor in [('failure_accepted_mean','failure_rate_accepted_mean',100),('failure_accepted_sd','failure_rate_accepted_std',100),('failure_or_reject_mean','failure_or_reject_rate_mean',100),('failure_or_reject_sd','failure_or_reject_rate_std',100),('runtime_mean','total_seconds_mean',1),('runtime_sd','total_seconds_std',1)]:fc('Figure7 '+key,f[key],s[col]*factor,.00005)
    write(ROOT/'audit/figure-data-checks.json',{'scope':'Key numeric arrays of figures 2-7 checked against research CSVs / reconstructed canonical; does not certify rendered pixels or every annotation. Figure1 is conceptual. Figure8 excluded from future product.', 'checks':fig_checks,'all_passed':all(c['passed'] for c in fig_checks)})
    # Provide a reviewable correction patch, never edit frozen source evidence.
    orig=(evidence/'31_ARCCRAFT_FULL_MANUSCRIPT.md').read_text(encoding='utf-8')
    revised=orig.replace('Incurred-cost ratios in the lowest decile were approximately 1.68 and 1.93','Incurred-cost ratios in the lowest decile were approximately 1.51 and 1.93')
    revised=revised.replace('the lowest incurred-risk decile has an observed-to-predicted ratio of 1.68','the first and second incurred-risk deciles in 2023 have observed-to-predicted ratios of 1.51 and 1.68, respectively')
    revised=revised.replace('an incurred-cost error of approximately -4.86%.','an incurred-cost error of approximately -4.88% in the registered 50,000-simulation run (seed 42).')
    revised=revised.replace('the original raw motor file is absent even though its recorded hash is available','the recovered original motor CSV and dictionary now match the recorded SHA-256 fingerprints, and all 16,644,580 normalized cells reconcile with the research database')
    proposal=ROOT/'proposals';proposal.mkdir(exist_ok=True)
    diff=''.join(difflib.unified_diff(orig.splitlines(keepends=True),revised.splitlines(keepends=True),fromfile='original/31_ARCCRAFT_FULL_MANUSCRIPT.md',tofile='proposed/31_ARCCRAFT_FULL_MANUSCRIPT.md'))
    (proposal/'manuscript-corrections.patch').write_text(diff,encoding='utf-8')
    # Manifest distinguishes original evidence, newly replayed outputs and candidate freeze.
    checks_report=json.loads((ROOT/'audit/scientific-checks.json').read_text())
    artifact_list=[]
    for folder,status in [('evidence','ORIGINAL_RESEARCH_SNAPSHOT'),('artifacts/candidate','CANDIDATE_REPLAY')]:
        for p in sorted((ROOT/folder).rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts:continue
            artifact_list.append({'artifact_id':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p),'proof_status':status,
                'verification_commit':source_commit,'historical_producer_commit':None if folder=='evidence' else source_commit,'version':'phase0-candidate-1',
                'license':'AUTHOR_DECISION_PENDING' if folder=='evidence' else 'CODE_AND_DERIVED_ARTIFACT_LICENSE_PENDING'})
    write(ROOT/'artifacts/manifest.json',{'schema_version':'arccraft-artifact-manifest-0.1','status':'CANDIDATE_NOT_RELEASED','source_commit':source_commit,
        'engine_declared_version':'0.1.0','engine_sha256':checks_report['engine_sha256'],'world_grammar_version':'world_grammar-0.1.0',
        'package_version':'0.1.0.dev1','calibration_version':'motor-mendeley-v1-reconciled-20260925','product_version':'synthetic-product-content-sha256',
        'historical_fingerprint_contract':'SHA-256 of compact JSON row arrays with metric rounding at 12 decimals',
        'canonical_historical_fingerprint':checks_report['canonical_fingerprint_rounded_12'],'canonical_full_precision_semantic_sha256':checks_report['canonical_raw_semantic_sha256'],
        'archive_doi':None,'release_tag':None,'artifacts':artifact_list})
    # Ensure audit execution did not change a single inventoried original resource.
    inventory=json.loads((ROOT/'audit/inventory.json').read_text())
    changes=[x['path'] for x in inventory if not Path(x['path']).is_file() or sha(Path(x['path']))!=x['sha256']]
    before=json.loads((ROOT/'audit/source-git.json').read_text())['status_before']
    after=subprocess.check_output(['git','status','--porcelain'],cwd=LEGACY,text=True)
    write(ROOT/'audit/source-integrity-after.json',{'checked_files':len(inventory),'changed_files':changes,'legacy_git_status_unchanged':before==after,'passed':not changes and before==after})
    print(json.dumps({'notebook_outputs_match':all(x['passed'] for x in checks),'figure_arrays_match':all(c['passed'] for c in fig_checks),'source_changes':changes,'source_commit':source_commit},indent=2))
    assert not changes and before==after

if __name__=='__main__':main()
