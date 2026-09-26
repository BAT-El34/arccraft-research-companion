"""Build reviewed editorial copies and a closed, hash-addressed download registry."""
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def write(path, value):
    p=ROOT/path; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n', encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def apply_reviewed_patch(patch, resolver):
    lines=(ROOT/patch).read_text(encoding='utf-8').splitlines()
    current=None; old=[]; new=[]
    def flush():
        if current and old:
            p=resolver(current); text=p.read_text(encoding='utf-8')
            before='\n'.join(old); after='\n'.join(new)
            if text.count(before)!=1: raise ValueError(f'Patch context is not unique: {p}')
            p.write_text(text.replace(before,after),encoding='utf-8')
    for line in lines:
        if line.startswith('--- '):
            flush(); old=[];new=[];current=line[4:]
        elif line.startswith('+++ '): continue
        elif line.startswith('@@'):
            flush();old=[];new=[]
        elif line.startswith(' '): old.append(line[1:]);new.append(line[1:])
        elif line.startswith('-'): old.append(line[1:])
        elif line.startswith('+'): new.append(line[1:])
    flush()

def main():
    publication=ROOT/'publication'
    # Always regenerate from the immutable in-repository evidence, never the original folders.
    shutil.copytree(ROOT/'evidence/latex',publication/'latex',dirs_exist_ok=True)
    shutil.copytree(ROOT/'evidence/figure_package',publication/'figure_package',dirs_exist_ok=True)
    shutil.copy2(ROOT/'evidence/research/31_ARCCRAFT_FULL_MANUSCRIPT.md',publication/'manuscript.md')
    apply_reviewed_patch('proposals/manuscript-corrections.patch',lambda _:publication/'manuscript.md')
    def resolve(path):
        suffix=path.removeprefix('original/')
        return publication/suffix
    apply_reviewed_patch('proposals/latex-and-figure-corrections.patch',resolve)
    # A candidate is explicit; archive DOI, reuse licences and affiliations are not fabricated.
    main_tex=publication/'latex/main.tex'
    text=main_tex.read_text(encoding='utf-8').replace('\\vspace{0.5em}', '\\vspace{0.5em}\n{\\large Elia Batako and Manuel Ntumba}\\par\n{\\small Reviewed companion candidate; author affiliations and archive DOI pending.}\\par',1)
    text=text.replace('\\vspace*{1.5cm}','\\vspace*{0.7cm}').replace('\\vspace{1.8cm}','\\vspace{0.8cm}')
    main_tex.write_text(text,encoding='utf-8')
    update_companion_links()
    subprocess.run([sys.executable,'code/Figure3.py'],cwd=publication/'figure_package',check=True)
    subprocess.run([sys.executable,'code/Figure8.py'],cwd=publication/'figure_package',check=True)
    shutil.copytree(publication/'figure_package/figures',publication/'latex/figures',dirs_exist_ok=True)
    build_registry()

def update_companion_links():
    publication=ROOT/'publication'
    url='https://arccraft-research-companion.vercel.app/en/'
    code=publication/'figure_package/code/Figure8.py'
    code.write_text(code.read_text(encoding='utf-8').replace('https://actuarial-digital-dashboard-rd-v3.vercel.app/fr#/arccraft',url),encoding='utf-8')
    statement=('The reviewed scientific engine is frozen at commit b642f8238d86b5ec3a4115d9d06d582682d69f1e in the independent ARCCRAFT Research Companion repository. '
               'Registered evidence, source hashes, calibration snapshots, replication scripts and the claim register accompany this candidate. '
               'The original motor CSV and variable dictionary were recovered and reconciled against the research derivative. Raw policy data and the general research database are not served by the companion. '
               'The external dataset is available from Mendeley Data under CC BY 4.0, DOI 10.17632/sw4jmdb2sm.1. Author metadata, reuse licences for code and authored content, and a final immutable archive DOI remain pending.')
    access=('Figure 8 opens the dedicated ARCCRAFT Research Companion. The site separates precomputed reference artifacts, live replays and user explorations. '
            'Each run records its scientific commit, parameters, environment and output fingerprint. The live site is a consultation and execution interface; '
            'the versioned evidence registry defines the reference results. The candidate must not be described as a final archived publication before its release metadata and DOI are completed.')
    caption='ARCCRAFT Research Companion access. The QR code opens the dedicated bilingual scientific companion. Reference evidence, live replay and user exploration remain separate; final archive DOI pending.'
    for path in [publication/'latex/sections/04_conclusion.tex',publication/'manuscript.md']:
        text=path.read_text(encoding='utf-8')
        text=re.sub(r'All reported calculations are stored.*?(?=\n\n)',lambda _:statement,text,flags=re.S)
        text=re.sub(r'An integrated public demonstrator is accessible.*?(?=\n\n)',lambda _:access,text,flags=re.S)
        if path.suffix=='.tex': text=re.sub(r'\\caption\{\\textbf\{Public ARCCRAFT demonstrator access\.\}.*?\}',lambda _:'\\caption{'+caption+'}',text)
        else:
            text=text.replace('https://actuarial-digital-dashboard-rd-v3.vercel.app/fr#/arccraft',url)
            text=re.sub(r'\*\*(?:Figure 8\. )?Public ARCCRAFT demonstrator access\.\*\*[^\n]*',caption,text)
        path.write_text(text,encoding='utf-8')

def build_registry():
    manifest=read('artifacts/manifest.json'); commit=manifest['source_commit']
    entries=[]
    def add(p, status='ORIGINAL_RESEARCH_SNAPSHOT', version='phase0-candidate-1', licence='AUTHOR_DECISION_PENDING'):
        rel=p.relative_to(ROOT).as_posix(); artifact_id=rel.replace('/','__')
        dest=ROOT/'public/downloads'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        item={'id':artifact_id,'path':rel,'url':'/downloads/'+rel,'sha256':sha(p),'bytes':p.stat().st_size,'proof_status':status,'version':version,'science_commit':commit,'license':licence,'release_status':'CANDIDATE'}
        entries.append(item);return item
    sources=list((ROOT/'evidence/research').glob('*.csv'))+list((ROOT/'artifacts/candidate').glob('*'))
    sources += [ROOT/'artifacts/manifest.json',ROOT/'audit/claim-register.json',ROOT/'audit/scientific-checks.json',ROOT/'audit/notebook-output-comparison.json',ROOT/'requirements-replay.lock',ROOT/'publication/manuscript.md',ROOT/'publication/latex/references.bib']
    for extra in ['requirements-runtime.lock','audit/application/vercel-cross-runtime.json']:
        if (ROOT/extra).exists():sources.append(ROOT/extra)
    for p in sources: add(p, 'LOCAL_REPRODUCTION_VERIFIED' if 'candidate' in p.parts else 'ORIGINAL_RESEARCH_SNAPSHOT')
    titles=['Architecture and evidence boundaries','Portfolio and temporal shift','Matched temporal forecasts','Calibration and interval coverage','Frequency–severity stress surface','Scenario classes and failure gates','Ablations and stream isolation']
    titles_fr=['Architecture et frontières de preuve','Portefeuille et dérive temporelle','Prévisions temporelles comparées','Calibration et couverture des intervalles','Surface de stress fréquence–sévérité','Classes de scénarios et seuils d’échec','Ablations et isolation des flux']
    mapping=[[],['18_DATA_QUALITY_FINDINGS.csv','24_TEMPORAL_CATEGORY_SHIFT.csv'],['19_POLICY_BENCHMARK_RESULTS.csv'],['20_POLICY_DECILE_CALIBRATION.csv','19_POLICY_BENCHMARK_RESULTS.csv'],['11_STRESS_SURFACE_RESULTS.csv'],['25_ARCCRAFT_ABLATION_RESULTS.csv'],['26_ARCCRAFT_ABLATION_SUMMARY.csv','27_STREAM_ISOLATION_TEST.csv']]
    captions=(ROOT/'evidence/figure_package/FIGURES_TOOLS_AND_SOURCES.md').read_text(encoding='utf-8').split('## Publication captions')[1]
    figures=[]
    for i in range(1,8):
        png=ROOT/f'publication/figure_package/figures/Figure{i}.png'
        img=add(png,'REVIEWED_EDITORIAL_COPY')
        script=add(ROOT/f'publication/figure_package/code/Figure{i}{"_tikz.tex" if i==1 else ".py"}','REVIEWED_EDITORIAL_COPY')
        caption=re.search(rf'### Figure {i}\s+(.+?)(?=### Figure|$)',captions,re.S).group(1).strip().replace('**','')
        figure_sources=[next(a for a in entries if a['path'].endswith('/'+name)) for name in mapping[i-1]]
        if i==1:figure_sources.append(next(a for a in entries if a['path']=='publication/manuscript.md'))
        if i==6:
            figure_sources.extend(next(a for a in entries if a['path'].endswith('/'+name)) for name in ['scenario-classes-10000.csv','failure-atlas-counts-10000.csv'])
        figures.append({'number':i,'title':titles[i-1],'title_fr':titles_fr[i-1],'caption':caption,'image':img,'script':script,'sources':figure_sources})
    pdf=ROOT/'publication/latex/main.pdf'
    if pdf.exists(): add(pdf,'REVIEWED_EDITORIAL_COPY')
    claims=read('audit/claim-register.json')
    fr=[('La fréquence par police améliore la discrimination','Baisse relative de déviance hors échantillon face à B0','Discrimination uniquement'),('Les intervalles sont insuffisamment calibrés','Réalisations couvertes par les intervalles de processus à 95 %','Deux origines temporelles'),('Les runs enregistrés se rejouent exactement','Empreintes de sortie identiques','Vérification informatique locale'),('Les flux nommés isolent les tirages inutilisés','Réponse de l’empreinte à des tirages supplémentaires','Une intervention enregistrée'),('Le validateur modifie la population retenue','Rejet strict comparé à la configuration complète','Effet de sélection et de mesure'),('Les transitions ont un faible effet observé','Taux d’échec parmi les mondes acceptés sans transitions','Résultat descriptif sur trois seeds'),('Le seuil de traçabilité domine l’Atlas','Part des échecs simulés associés à la traçabilité','Aucune preuve d’attribution causale'),('La comparaison des durées est bruitée','Moyenne, écart-type et coefficient de variation','Durée historique propre à un hôte')]
    formulas=['100 × (deviance B0 − deviance B1) / deviance B0','Σ 1[q025 ≤ observed ≤ q975] / outcomes','Σ 1[fingerprint replay = fingerprint registered] / runs','fingerprint(before) = fingerprint(after unused draws)','100 × (accepted full − accepted strict) / accepted full; 100 × (rate strict − rate full)','100 × (failure rate no transitions − failure rate full)','100 × traceability failures / simulated failures (rejects excluded)','mean(t); sample SD(t); 100 × SD(t) / mean(t)']
    units=['%','outcomes','runs','boolean','%; percentage points','percentage points; %','%','seconds; %']
    for i,c in enumerate(claims):
        c.update(claim_fr=fr[i][0],metric_fr=fr[i][1],scope_fr=fr[i][2],formula=formulas[i],unit=units[i],source_url='/downloads/'+c['source_path'],population='Motor portfolio; forecast origins 2023, 2024' if i<2 else 'Synthetic registered worlds; seeds 20260825–20260827',paper_reference='Results / empirical benchmark' if i<2 else 'Results / procedural ablations')
    result_translations=[
        '7,19 % en 2023 ; 8,99 % en 2024',
        '3/12 au total ; 3/6 nombres de sinistres ; 0/6 coûts totaux',
        '15/15 paires configuration–seed',
        'Flux nommés inchangés ; flux partagé modifié',
        '19,87 % de mondes acceptés en moins ; +13,43 points de pourcentage d’échec ou rejet',
        '−0,247 point de pourcentage ; −0,69 % en relatif',
        '3588/3589, soit 99,97 %',
        '3,59 s ; 1,05 s ; 29,09 %'
    ]
    for c,translated in zip(claims,result_translations):c['observed_result_fr']=translated
    worlds=read('artifacts/candidate/canonical-worlds.json'); by_id={r['world_id']:r for r in worlds}
    atlas=read('artifacts/candidate/failure-atlas.json')
    for row in atlas:
        row['statut_validation']=by_id[row['world_id']]['statut_validation'];row['run_id']='canonical-20260825-10000'
    write('public/data/atlas.json',{'provenance':{'science_commit':commit,'version':'atlas-adapter-1.0','source_sha256':sha(ROOT/'artifacts/candidate/failure-atlas.json'),'source':'/downloads/artifacts/candidate/failure-atlas.json','proof_status':'LOCAL_REPRODUCTION_VERIFIED','release_status':'CANDIDATE','metric_id':'canonical_failure_events'},'rows':atlas})
    data=read('audit/data-reconciliation.json');data.pop('source',None)
    write('public/data/provenance.json',data)
    registered={f"{r['config']}:{r['seed']}":r['fingerprint'] for r in csv.DictReader((ROOT/'evidence/research/25_ARCCRAFT_ABLATION_RESULTS.csv').open(encoding='utf-8'))}
    registry={'science_commit':commit,'version':'companion-candidate-1','release_status':'CANDIDATE','archive_doi':None,'artifacts':entries,'registered_fingerprints':registered}
    write('artifacts/web-registry.json',registry);write('public/data/registry.json',registry)
    manuscript=(ROOT/'publication/manuscript.md').read_text(encoding='utf-8')
    abstract=manuscript.split('## Abstract')[1].split('**Keywords:**')[0].strip()
    cross_runtime=read('audit/application/vercel-cross-runtime.json') if (ROOT/'audit/application/vercel-cross-runtime.json').exists() else None
    write('web/content.json',{'crossRuntime':cross_runtime,'manifest':{k:v for k,v in manifest.items() if k!='artifacts'},'claims':claims,'figures':figures,'registry':registry,'abstract':abstract,'title':manuscript.splitlines()[0].removeprefix('# '),'motor':read('artifacts/candidate/motor-forecast.json'),'data':{k:v for k,v in data.items() if k not in ['schema','dictionary']}})
    title=manuscript.splitlines()[0].removeprefix('# ')
    (ROOT/'CITATION.cff').write_text(f'cff-version: 1.2.0\nmessage: "Please cite the scientific candidate; archive DOI pending."\ntype: software\ntitle: "{title}"\nversion: 0.1.0\nauthors:\n  - family-names: Batako\n    given-names: Elia\n  - family-names: Ntumba\n    given-names: Manuel\nrepository-code: "https://github.com/BAT-El34/arccraft-research-companion"\n',encoding='utf-8')
    citation_dir=ROOT/'public/citations';citation_dir.mkdir(parents=True,exist_ok=True)
    (citation_dir/'arccraft.bib').write_text('@misc{batako_ntumba_arccraft_candidate,\n  author = {Batako, Elia and Ntumba, Manuel},\n  title = {'+title+'},\n  year = {2026},\n  note = {Scientific draft; companion candidate; archive DOI pending},\n  url = {https://github.com/BAT-El34/arccraft-research-companion}\n}\n',encoding='utf-8')
    (citation_dir/'arccraft.ris').write_text('TY  - UNPB\nAU  - Batako, Elia\nAU  - Ntumba, Manuel\nTI  - '+title+'\nPY  - 2026\nN1  - Scientific draft; archive DOI pending\nUR  - https://github.com/BAT-El34/arccraft-research-companion\nER  - \n',encoding='utf-8')
    print(json.dumps({'artifacts':len(entries),'claims':len(claims),'figures':len(figures),'atlas_events':len(atlas)}))

if __name__=='__main__': main()
