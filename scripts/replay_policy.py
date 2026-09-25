"""Standalone policy benchmark from verified raw CSV, without the legacy app or SQLite."""
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from arccraft.policy_benchmark import MODEL_COLUMNS, CATEGORICAL_FEATURES, fit_policy_models
from arccraft.motor import empirical_motor_calibration

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--csv',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'audit/standalone-policy')
    args=parser.parse_args()
    digest=hashlib.file_digest(args.csv.open('rb'),'sha256').hexdigest()
    expected='6a47d19d5278a049ea0aeaf39c955cc26068639bdc58cb4523b201e740f0faf4'
    if digest!=expected:raise ValueError('Unverified motor source: SHA-256 differs from registered source')
    frame=pd.read_csv(args.csv,sep=';',dtype=str,keep_default_na=False,usecols=MODEL_COLUMNS)
    categorical=set(CATEGORICAL_FEATURES)|{'policy_status'}
    failures={}
    for col in MODEL_COLUMNS:
        values=frame[col].str.strip().str.strip('"')
        if col in categorical:
            frame[col]=values.map(lambda x:None if x=='' else x)
        else:
            def parse(value):
                try:return float(value) if value!='' else None
                except ValueError:
                    failures[col]=failures.get(col,0)+1
                    return None
            frame[col]=values.map(parse)
            if col in {'insured_id','year','seats','total_claims'} and frame[col].notna().all():frame[col]=frame[col].astype('int64')
    frame=frame[MODEL_COLUMNS].sort_values(['year','insured_id']).reset_index(drop=True)
    results=[]; deciles=[]; diagnostics=[]
    for years,target in [([2022],2023),([2022,2023],2024)]:
        sigma=empirical_motor_calibration(min(years),max(years))['severity_proxy']['sigma_log']
        r,d,diag=fit_policy_models(frame,years,target,sigma)
        results.append(r);deciles.append(d)
        diagnostics.append({'target':target,**{k:v for k,v in diag.items() if not isinstance(v,np.ndarray)}})
    actual=pd.concat(results,ignore_index=True)
    actual_deciles=pd.concat(deciles,ignore_index=True)
    expected_df=pd.read_csv(ROOT/'evidence/research/19_POLICY_BENCHMARK_RESULTS.csv')
    expected_deciles=pd.read_csv(ROOT/'evidence/research/20_POLICY_DECILE_CALIBRATION.csv')
    checks={}
    for title,a,b in [('benchmark',actual,expected_df),('deciles',actual_deciles,expected_deciles)]:
        checks[title]={}
        for c in a:
            if pd.api.types.is_numeric_dtype(a[c]) and a[c].dtype!=bool:
                checks[title][c]={'passed':bool(np.allclose(a[c],b[c],rtol=1e-10,atol=1e-10,equal_nan=True)),
                    'max_absolute_difference':float(np.nanmax(np.abs(a[c].to_numpy()-b[c].to_numpy())))}
            else:checks[title][c]={'passed':a[c].tolist()==b[c].tolist()}
    passed=all(v['passed'] for group in checks.values() for v in group.values())
    args.output.mkdir(parents=True,exist_ok=True)
    actual.to_csv(args.output/'19_POLICY_BENCHMARK_RESULTS.csv',index=False)
    actual_deciles.to_csv(args.output/'20_POLICY_DECILE_CALIBRATION.csv',index=False)
    report={'passed':passed,'source_sha256':digest,'rows':len(frame),'normalization_failures_reported':failures,
        'rtol':1e-10,'atol':1e-10,'diagnostics':diagnostics,'checks':checks}
    (args.output/'checks.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'passed':passed,'rows':len(frame),'failed_columns':[k+':'+c for k,g in checks.items() for c,v in g.items() if not v['passed']]},indent=2))
    raise SystemExit(0 if passed else 1)

if __name__=='__main__':main()
