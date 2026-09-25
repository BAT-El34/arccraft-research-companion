"""Record the resolved, installed dependency closure; no claim of fresh-install validation."""
import importlib.metadata as md,json,platform,sys
from pathlib import Path
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
ROOT=Path(__file__).resolve().parents[1]
pending=['numpy','pandas','scipy','matplotlib','fastapi','nbformat','nbclient','nbconvert','ipykernel','openpyxl','pypdf']
versions={};missing=[]
while pending:
    name=canonicalize_name(pending.pop())
    if name in versions:continue
    try:d=md.distribution(name)
    except md.PackageNotFoundError:missing.append(name);continue
    versions[name]=d.version
    for text in d.requires or []:
        r=Requirement(text)
        if r.marker is None or r.marker.evaluate({'extra':''}):pending.append(r.name)
lock='# Observed Windows/Python 3.12 environment; exact installed dependency closure.\n# No fresh-environment installation or wheel-hash verification yet.\n'+'\n'.join(f'{k}=={v}' for k,v in sorted(versions.items()))+'\n'
(ROOT/'requirements-replay.lock').write_text(lock,encoding='utf-8')
(ROOT/'audit/environment-lock-status.json').write_text(json.dumps({'python':sys.version,'platform':platform.platform(),'packages':len(versions),'missing_dependencies':sorted(set(missing)),'fresh_install_verified':False,'wheel_hashes_verified':False},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'packages':len(versions),'missing':missing},indent=2))
