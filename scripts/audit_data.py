"""Verify source bytes, schema and ALL normalized motor cells before reuse."""
from pathlib import Path
import csv, hashlib, importlib.util, json, sqlite3, sys, zipfile
from prepare_phase0 import ROOT, SOURCE, RESEARCH, LEGACY, DATA, sha, write

sys.path.insert(0,str(LEGACY))
from backend import data_service as ds
from backend.build_data_store import infer_motor_type

def main():
    source=DATA/'Dataset of motor insurance portfolio (1).csv'
    dictionary=DATA/'Descriptive of variables (1).xlsx'
    recorded=json.loads((LEGACY/'data/manifest.json').read_text())['source_fingerprints']
    checks={
        'csv_sha256_matches_recorded':sha(source)==recorded['motor_portfolio_upload']['sha256'],
        'dictionary_sha256_matches_recorded':sha(dictionary)==recorded['motor_dictionary_upload']['sha256']}
    assert all(checks.values()), 'Source identity unresolved: stop data reuse'
    result={'source':str(source),'sha256':sha(source),'dictionary_sha256':sha(dictionary),
        'license':{'spdx':'CC-BY-4.0','url':'https://data.mendeley.com/datasets/sw4jmdb2sm/1','version':1,
        'doi':'10.17632/sw4jmdb2sm.1','verified_on':'2026-09-25','contributors':['Priscila Espinosa','Josep Lledó','David Atance'],
        'note':'License verified on publisher dataset page; local bytes match research ingestion manifest. No fresh publisher file download performed.'},'checks':checks}
    with zipfile.ZipFile(DATA/'A detailed dataset of motor insurance policies wit.zip') as z:
        result['zip_members']=[{'name':p.filename,'bytes':p.file_size,'sha256':hashlib.sha256(z.read(p)).hexdigest()} for p in z.infolist() if not p.is_dir()]
    with ds.connect() as con, source.open(encoding='utf-8-sig',newline='') as f:
        result['sqlite_integrity']=con.execute('PRAGMA integrity_check').fetchone()[0]
        schema=[dict(x) for x in con.execute('PRAGMA table_info(motor_portfolio)')]
        result['schema']=schema
        reader=csv.reader(f,delimiter=';'); headers=[h.strip().strip('"') for h in next(reader)]
        assert headers==[x['name'] for x in schema]
        checks['schema_matches']=True
        sqlrows=con.execute('SELECT * FROM motor_portfolio ORDER BY rowid')
        mismatched_rows=mismatched_cells=rows=0; cast_failures={}; null_counts=dict.fromkeys(headers,0)
        types=[infer_motor_type(h) for h in headers]
        for raw in reader:
            assert len(raw)==len(headers)
            normalized=[]
            for key,s,t in zip(headers,raw,types):
                s=s.strip().strip('"')
                try: v=None if s=='' else s if t=='TEXT' else int(float(s)) if t=='INTEGER' else float(s)
                except ValueError:
                    cast_failures[key]=cast_failures.get(key,0)+1; v=None
                null_counts[key]+=v is None
                normalized.append(v)
            dbrow=sqlrows.fetchone()
            assert dbrow is not None
            mismatches=sum(a!=b for a,b in zip(normalized,dbrow))
            mismatched_rows+=mismatches>0; mismatched_cells+=mismatches; rows+=1
        assert sqlrows.fetchone() is None
        result.update(rows=rows,columns=len(headers),compared_cells=rows*len(headers),mismatched_rows=mismatched_rows,mismatched_cells=mismatched_cells,cast_failures=cast_failures,null_counts=null_counts)
        checks['all_normalized_cells_equal']=mismatched_cells==0
        result['unique_insureds']=con.execute('SELECT COUNT(DISTINCT insured_id) FROM motor_portfolio').fetchone()[0]
        result['duplicate_keys']=con.execute('SELECT COUNT(*) FROM (SELECT insured_id,year FROM motor_portfolio GROUP BY insured_id,year HAVING COUNT(*)>1)').fetchone()[0]
        result['annual']=[dict(x) for x in con.execute('SELECT * FROM motor_year_summary ORDER BY year')]
        result['dictionary_rows']=[dict(x) for x in con.execute('SELECT * FROM motor_variables')]
    # Only produce reusable calibration after all source checks have passed.
    assert all(checks.values()) and result['sqlite_integrity']=='ok'
    calibration={f'{a}-{b}':ds.empirical_motor_calibration(a,b) for a,b in [(2022,2022),(2022,2023),(2023,2023),(2024,2024)]}
    write(ROOT/'arccraft/calibration/motor-v1.json',calibration)
    write(ROOT/'audit/data-reconciliation.json',result)
    print(json.dumps({k:result[k] for k in ['rows','columns','compared_cells','mismatched_cells','cast_failures','checks']},indent=2))

if __name__=='__main__': main()
