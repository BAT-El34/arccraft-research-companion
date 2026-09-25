"""Execute every code cell in order, redirecting outputs and enforcing source DB read-only.

This is a cell replay in one Python process, not a Jupyter kernel/E2E notebook test.
The original source cells are copied into the execution receipt with the sole output-path edit.
"""
import contextlib, io, json, os, shutil, sqlite3, sys, time, traceback
from pathlib import Path
from prepare_phase0 import ROOT, RESEARCH, LEGACY, sha, write

def main():
    name=sys.argv[1]
    assert name in {'08_EMPIRICAL_BENCHMARK.ipynb','17_DATA_QUALITY_POLICY_BENCHMARK.ipynb'}
    output=ROOT/'audit/notebook-replay'/name[:2]; output.mkdir(parents=True,exist_ok=True)
    # The notebook hashes its benchmark module relative to OUT; preserve exact bytes there.
    shutil.copyfile(RESEARCH/'policy_benchmark_core.py', output/'policy_benchmark_core.py')
    shutil.copyfile(RESEARCH/'16_RETROSPECTIVE_ANALYSIS_SPECIFICATION.md', output/'16_RETROSPECTIVE_ANALYSIS_SPECIFICATION.md')
    os.environ['MPLBACKEND']='Agg'
    sys.path.insert(0,str(LEGACY)); sys.path.insert(0,str(RESEARCH))
    os.chdir(LEGACY)
    native_connect=sqlite3.connect
    db=(LEGACY/'data/platform.db').resolve()
    def readonly_connect(database,*args,**kwargs):
        if str(database)==str(db) or str(database)==db.as_posix():
            database=f'file:{db.as_posix()}?mode=ro'; kwargs['uri']=True
        con=native_connect(database,*args,**kwargs)
        con.execute('PRAGMA temp_store=MEMORY')
        return con
    sqlite3.connect=readonly_connect
    namespace={'__name__':'__notebook_replay__','display':lambda *items:None}
    notebook=json.loads((RESEARCH/name).read_text(encoding='utf-8'))
    receipt={'source':name,'source_sha256':sha(RESEARCH/name),'method':'Sequential execution of all code cells; output directory redirected; SQLite original forced read-only; temp_store=MEMORY to avoid system-temp disk exhaustion','cells':[]}
    buffer=io.StringIO()
    with contextlib.redirect_stdout(buffer),contextlib.redirect_stderr(buffer):
        for index,cell in enumerate(notebook['cells']):
            if cell['cell_type']!='code':continue
            source=''.join(cell['source'])
            source=source.replace('OUT = REPO.parents[1] / "ARCCRAFT"',f'OUT = Path({str(output)!r})')
            start=time.perf_counter()
            record={'cell_index':index,'executed_source':source}
            try:
                exec(compile(source,f'{name}:cell{index}','exec'),namespace)
                record['status']='PASS'
            except Exception:
                record['status']='FAIL';record['traceback']=traceback.format_exc()
            record['seconds']=time.perf_counter()-start;receipt['cells'].append(record)
            if record['status']=='FAIL':break
    receipt['all_code_cells_executed']=len(receipt['cells'])==sum(c['cell_type']=='code' for c in notebook['cells'])
    receipt['passed']=receipt['all_code_cells_executed'] and all(c['status']=='PASS' for c in receipt['cells'])
    write(output/'execution.json',receipt)
    (output/'stdout.txt').write_text(buffer.getvalue(),encoding='utf-8')
    print(json.dumps({'notebook':name,'passed':receipt['passed'],'code_cells':len(receipt['cells']),'error':next((c.get('traceback') for c in receipt['cells'] if c['status']=='FAIL'),None)},indent=2))
    raise SystemExit(0 if receipt['passed'] else 1)

if __name__=='__main__':main()
