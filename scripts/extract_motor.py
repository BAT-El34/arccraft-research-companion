"""Extract the exact motor calculation with a compact, verified calibration provider."""
import ast
from prepare_phase0 import ROOT, LEGACY, sha, write

source=(LEGACY/'backend/model_service.py').read_text(encoding='utf-8')
node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='arccraft_empirical_motor')
function=ast.get_source_segment(source,node)
header='''"""Scientific motor calculation extracted without formula changes.

Calibration values are a verified snapshot; target outcomes are evaluation-only.
No access to the legacy application or SQLite is required.
"""
from __future__ import annotations
import copy
import json
import math
from pathlib import Path
from typing import Any
import numpy as np

def empirical_motor_calibration(start_year: int, end_year: int) -> dict[str, Any]:
    data = json.loads((Path(__file__).parent / "calibration/motor-v1.json").read_text(encoding="utf-8"))
    key = f"{start_year}-{end_year}"
    if key not in data:
        raise ValueError("Unregistered calibration period")
    return copy.deepcopy(data[key])

'''
(ROOT/'arccraft/motor.py').write_text(header+function+'\n',encoding='utf-8')
write(ROOT/'audit/motor-extraction.json',{'source':str(LEGACY/'backend/model_service.py'),'source_sha256':sha(LEGACY/'backend/model_service.py'),
    'function':'arccraft_empirical_motor','formula_changes':False,'provider_change':'SQLite read-only calibration replaced by verified arccraft/calibration/motor-v1.json',
    'target_sha256':sha(ROOT/'arccraft/motor.py')})
