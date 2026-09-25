"""Read-only inventory and byte-preserving extraction. Originals are never written."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent
RESEARCH = SOURCE / 'ARCCRAFT'
LEGACY = SOURCE / 'mapta-compass-arccraft-platform-v2.1-FINAL/mapta-compass-arccraft-poc'
DATA = SOURCE.parent / 'Quantitative_Datasets_Clean_Final'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')

def main():
    inventory = []
    excluded = {'.git','node_modules','__pycache__','.vercel'}
    for category, base in [('research', RESEARCH), ('reference_app', LEGACY), ('datasets', DATA), ('paper_pdf', SOURCE/'output/pdf')]:
        for p in sorted(base.rglob('*')):
            if not p.is_file() or excluded.intersection(p.relative_to(base).parts): continue
            inventory.append(dict(category=category, path=str(p), relative_path=p.relative_to(base).as_posix(), bytes=p.stat().st_size, sha256=sha(p)))
    write(ROOT/'audit/inventory.json', inventory)
    copies = [(LEGACY/'backend/engine/arccraft_engine.py', ROOT/'arccraft/engine.py'),
              (RESEARCH/'policy_benchmark_core.py', ROOT/'arccraft/policy_benchmark.py')]
    for p in RESEARCH.iterdir():
        if p.is_file() and (p.suffix in {'.csv','.md','.ipynb'} or p.name in {'run_arccraft_ablation.py','research_requirements.txt','build_empirical_notebook.py','build_policy_benchmark_notebook.py'}):
            copies.append((p, ROOT/'evidence/research'/p.name))
    for p in (RESEARCH/'figure_package').rglob('*'):
        if p.is_file() and not {'__pycache__','_archive_staging'}.intersection(p.parts) and p.suffix in {'.py','.tex','.png','.md'}:
            copies.append((p, ROOT/'evidence/figure_package'/p.relative_to(RESEARCH/'figure_package')))
    copies += [(SOURCE/'output/pdf/ARCCRAFT_Procedural_Stress_Testing.pdf', ROOT/'evidence/paper/ARCCRAFT_Procedural_Stress_Testing.pdf')]
    for p in (RESEARCH/'latex_project/latex_code').rglob('*'):
        if p.is_file() and p.suffix in {'.tex','.bib'}: copies.append((p,ROOT/'evidence/latex'/p.relative_to(RESEARCH/'latex_project/latex_code')))
    mapping=[]
    for src,dst in copies:
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dst)
        assert sha(src)==sha(dst)
        mapping.append({'source':str(src),'target':dst.relative_to(ROOT).as_posix(),'sha256':sha(dst)})
    (ROOT/'arccraft/__init__.py').write_text('"""ARCCRAFT scientific candidate; publication freeze pending review."""\n',encoding='utf-8')
    runner=(RESEARCH/'run_arccraft_ablation.py').read_text(encoding='utf-8')
    runner=runner.replace('from backend.engine.arccraft_engine import (','from arccraft.engine import (')
    runner=runner.replace('REPO = ROOT / "mapta-compass-arccraft-platform-v2.1-FINAL" / "mapta-compass-arccraft-poc"','REPO = ROOT')
    runner=runner.replace('OUT = ROOT / "ARCCRAFT"','OUT = ROOT / "audit" / "replay"')
    (ROOT/'scripts/run_ablation.py').write_text(runner,encoding='utf-8')
    write(ROOT/'audit/extraction.json',mapping)
    write(ROOT/'audit/source-git.json',{
        'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=LEGACY,text=True).strip(),
        'status_before':subprocess.check_output(['git','status','--porcelain'],cwd=LEGACY,text=True),
        'scientific_engine_sha256':sha(LEGACY/'backend/engine/arccraft_engine.py')})
    patch=subprocess.check_output(['git','diff','--binary'],cwd=LEGACY)
    (ROOT/'audit/legacy-working-tree.patch').write_bytes(patch)
    base=subprocess.check_output(['git','show','HEAD:backend/engine/arccraft_engine.py'],cwd=LEGACY)
    private=ROOT/'.audit-private'; private.mkdir(exist_ok=True)
    (private/'base_engine.py').write_bytes(base)
    print(json.dumps({'files':len(inventory),'bytes':sum(p['bytes'] for p in inventory),'extracted':len(mapping),'categories':{k:sum(x['category']==k for x in inventory) for k in sorted(set(x['category'] for x in inventory))}},indent=2))

if __name__=='__main__': main()
