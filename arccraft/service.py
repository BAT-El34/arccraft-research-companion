"""Bounded web adapter; the frozen scientific modules remain unchanged."""
from __future__ import annotations
import csv
import dataclasses
import hashlib
import json
import math
import os
import platform
import time
import uuid
from pathlib import Path
from typing import Literal
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, model_validator
from . import engine as e
from .motor import arccraft_empirical_motor

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'artifacts/manifest.json').read_text(encoding='utf-8'))
REGISTRY = json.loads((ROOT / 'artifacts/web-registry.json').read_text(encoding='utf-8'))
SEEDS = (20260825, 20260826, 20260827)
app = FastAPI(title='ARCCRAFT Research Companion', version='0.1.0', docs_url='/api/v1/docs', openapi_url='/api/v1/openapi.json')

def clean(value):
    if isinstance(value, dict): return {k: clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [clean(v) for v in value]
    if isinstance(value, np.generic): return clean(value.item())
    if isinstance(value, float) and not math.isfinite(value): return None
    return value

def digest(value):
    return hashlib.sha256(json.dumps(clean(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()

def live_available():
    # Vercel production/preview require qualified platform protection. Fail closed.
    return not os.getenv('VERCEL') or os.getenv('ARCCRAFT_COMPUTE_PROTECTION') == 'qualified-platform-rule-v1'

@app.middleware('http')
async def request_bounds(request: Request, call_next):
    if request.method == 'POST':
        size = request.headers.get('content-length')
        if size is None or not size.isdigit() or int(size) > 4096:
            return JSONResponse({'detail': 'Request body must have a Content-Length of at most 4096 bytes.'}, status_code=413)
        body = await request.body()
        if len(body) > 4096:
            return JSONResponse({'detail': 'Payload too large.'}, status_code=413)
        try:
            def reject_nonfinite(token): raise ValueError('Non-finite JSON value')
            json.loads(body, parse_constant=reject_nonfinite)
        except (ValueError, UnicodeDecodeError):
            return JSONResponse({'detail': 'A valid finite JSON body is required.'}, status_code=400)
        if not live_available():
            return JSONResponse({'detail': 'Public computation awaits qualification of shared rate limiting. Canonical artifacts and local replay remain available.'}, status_code=503)
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, allow_inf_nan=False)

class SyntheticRequest(Strict):
    mode: Literal['CANONICAL_REPLAY', 'REGISTERED_VARIANT', 'EXPLORATORY'] = 'CANONICAL_REPLAY'
    variant: Literal['full', 'no_validator', 'strict_reject', 'no_transitions', 'shared_stream'] = 'full'
    seed: int = Field(default=20260825, ge=0, le=4294967295)
    worlds: int = Field(default=10000, ge=100, le=10000)
    world_id: int | None = Field(default=None, ge=0, le=9999)

    @model_validator(mode='after')
    def registered(self):
        if self.mode == 'CANONICAL_REPLAY' and (self.variant, self.seed, self.worlds) != ('full', 20260825, 10000):
            raise ValueError('Canonical replay is locked to full / 20260825 / 10000.')
        if self.mode == 'REGISTERED_VARIANT' and (self.seed not in SEEDS or self.worlds != 10000):
            raise ValueError('Registered variants require a registered seed and 10000 worlds.')
        if self.world_id is not None and self.world_id >= self.worlds:
            raise ValueError('world_id must belong to the run.')
        return self

class MotorRequest(Strict):
    mode: Literal['CANONICAL_REPLAY', 'EXPLORATORY'] = 'CANONICAL_REPLAY'
    seed: int = Field(default=42, ge=0, le=4294967295)
    n_simulations: int = Field(default=50000, ge=500, le=50000)
    frequency_multiplier: float = Field(default=1.0, ge=0.5, le=2.0)
    severity_multiplier: float = Field(default=1.0, ge=0.5, le=2.0)
    expense_ratio: float | None = Field(default=None, ge=0, le=1)
    commission_ratio: float | None = Field(default=None, ge=0, le=1)

    @model_validator(mode='after')
    def registered(self):
        if (self.expense_ratio is None) != (self.commission_ratio is None):
            raise ValueError('Supply both expense and commission assumptions or neither.')
        if self.mode == 'CANONICAL_REPLAY' and (self.seed, self.n_simulations, self.frequency_multiplier, self.severity_multiplier, self.expense_ratio, self.commission_ratio) != (42, 50000, 1., 1., None, None):
            raise ValueError('Canonical motor run is locked to the registered calibration and assumptions.')
        return self

def identity():
    return {'science_commit': MANIFEST['source_commit'], 'build_commit': os.getenv('VERCEL_GIT_COMMIT_SHA', os.getenv('ARCCRAFT_BUILD_COMMIT', 'LOCAL_UNCOMMITTED_BUILD')),
            'engine_version': e.MODEL_VERSION, 'grammar_version': e.GRAMMAIRE_VERSION,
            'calibration_version': MANIFEST['calibration_version'], 'engine_sha256': MANIFEST['engine_sha256'],
            'product_version': 'sha256:' + digest(e.product), 'release_tag': None,
            'schema_version': 'arccraft-web-run-1.0', 'release_status': 'CANDIDATE', 'archive_doi': None,
            'runtime': {'python': platform.python_version(), 'numpy': np.__version__, 'system': platform.system(), 'machine': platform.machine(), 'python_compiler': platform.python_compiler()}}

@app.get('/api/v1/health')
def health():
    actual = hashlib.sha256((ROOT / 'arccraft/engine.py').read_bytes()).hexdigest()
    return {**identity(), 'status': 'ok' if actual == MANIFEST['engine_sha256'] else 'integrity_error',
            'live_computation': live_available(), 'manifest_sha256': hashlib.sha256((ROOT / 'artifacts/manifest.json').read_bytes()).hexdigest(),
            'public_rate_limit': 'platform-rule' if os.getenv('ARCCRAFT_COMPUTE_PROTECTION') else 'NOT_QUALIFIED'}

@app.get('/api/v1/runs/canonical')
def canonical():
    return {**identity(), 'execution': 'PRECOMPUTED_REFERENCE', 'proof_status': 'LOCAL_REPRODUCTION_VERIFIED',
            'parameters': {'synthetic': {'seed': 20260825, 'worlds': 10000, 'variant': 'full'}, 'motor': {'seed': 42, 'n_simulations': 50000, 'calibration': [2022, 2023], 'target': 2024}},
            'expected_semantic_sha256': MANIFEST['canonical_full_precision_semantic_sha256'], 'artifacts': REGISTRY['artifacts']}

@app.get('/api/v1/artifacts/{artifact_id}')
def artifact(artifact_id: str):
    for item in REGISTRY['artifacts']:
        if item['id'] == artifact_id: return item
    raise HTTPException(404, 'Unknown artifact identifier')

def envelope(parameters, result, expected=None, historical=None):
    output_hash = digest(result)
    return {**identity(), 'run_id': str(uuid.uuid4()), 'execution': 'LIVE_COMPUTATION', 'mode': parameters['mode'],
            'parameters': parameters, 'input_sha256': digest(parameters), 'output_semantic_sha256': output_hash,
            'proof_status': ('VERIFIED' if output_hash == expected else 'DIVERGENT') if expected else 'EXPLORATORY_NOT_VALIDATED',
            'expected_semantic_sha256': expected, 'historical_fingerprint': historical, 'result': clean(result)}

def synthetic_run(p):
    if hashlib.sha256((ROOT / 'arccraft/engine.py').read_bytes()).hexdigest() != MANIFEST['engine_sha256']:
        raise HTTPException(503, 'Frozen engine integrity check failed')
    if p.variant == 'shared_stream':
        shared = np.random.Generator(np.random.PCG64(p.seed))
        worlds = e.generer_mondes(shared, n=p.worlds)
        claims = behaviour = shared
        streams = {'shared': {'algorithme': 'PCG64', 'spawn_key': []}}
    else:
        flux = e.construire_flux_nommes(p.seed)
        worlds = e.generer_mondes(flux['world'], n=p.worlds)
        claims, behaviour = flux['claims'], flux['behaviour']
        streams = e.decrire_flux_nommes(flux)
    validation = e.valider_mondes(worlds)
    if p.variant == 'strict_reject':
        states = validation.statut.copy()
        states[states == 'REPAIR'] = 'REJECT'
        validation = e.ResultatValidation(statut=states, etat_valide={k: v.copy() for k, v in validation.etat_valide.items()})
    elif p.variant == 'no_validator':
        validation = e.ResultatValidation(statut=np.full(worlds.n, 'PASS', dtype=object), etat_valide={v: worlds.etat[v].copy() for v in e.VARIABLES_ETAT})
    rows = e.simuler_trajectoires(e.product, worlds, validation, claims, behaviour, activer_transitions=p.variant != 'no_transitions')
    payload = clean([dataclasses.asdict(r) for r in rows])
    rounded = [[r.world_id, r.regime, r.classe, r.statut_validation, None if not np.isfinite(r.combined_ratio) else round(r.combined_ratio, 12), None if not np.isfinite(r.tracabilite_score) else round(r.tracabilite_score, 12), r.porte_ratee, r.succes] for r in rows]
    fingerprint = hashlib.sha256(json.dumps(rounded, separators=(',', ':')).encode()).hexdigest()
    expected = MANIFEST['canonical_full_precision_semantic_sha256'] if p.mode == 'CANONICAL_REPLAY' else None
    response = envelope(p.model_dump(), payload, expected, fingerprint)
    if p.mode == 'REGISTERED_VARIANT':
        registered = REGISTRY['registered_fingerprints'][f'{p.variant}:{p.seed}']
        response['expected_historical_fingerprint'] = registered
        response['proof_status'] = 'VERIFIED' if fingerprint == registered else 'DIVERGENT'
    statuses = {r.world_id: r.statut_validation for r in rows}
    atlas = e.construire_failure_atlas(rows, p.seed, streams)
    for event in atlas: event['statut_validation'] = statuses[event['world_id']]
    response.update(named_streams=streams, atlas=clean(atlas), classes=clean(e.agreger_par_classe(rows)), gates=e.synthese_failure_atlas(atlas),
                    correlations=clean(e.cribler_variables(rows, worlds, validation)),
                    reverse_stress=e.recherche_stress_inverse(e.product, p.seed) if p.variant == 'full' else None,
                    warnings=['Synthetic grammar is not an empirical motor calibration.', 'Correlations and failure gates do not establish causality.', 'Reverse stress uses a separate full-configuration search, not a global optimum.'] )
    response['diagnostics_semantic_sha256'] = digest({k: response[k] for k in ['atlas', 'classes', 'gates', 'correlations', 'reverse_stress']})
    if p.world_id is not None:
        response['selected_world'] = payload[p.world_id]
        response['selection_method'] = 'Replay complete run before selecting world; output hash always covers complete run.'
    return response

@app.post('/api/v1/simulate/synthetic')
def synthetic(p: SyntheticRequest):
    started = time.perf_counter()
    response = synthetic_run(p)
    response['duration_seconds'] = time.perf_counter() - started
    return response

@app.post('/api/v1/simulate/motor')
def motor(p: MotorRequest):
    started = time.perf_counter()
    args = p.model_dump(exclude={'mode'})
    result = arccraft_empirical_motor(**args)
    reference = json.loads((ROOT / 'artifacts/candidate/motor-forecast.json').read_text(encoding='utf-8'))
    response = envelope(p.model_dump(), result, digest(reference) if p.mode == 'CANONICAL_REPLAY' else None)
    response.update(duration_seconds=time.perf_counter()-started, named_streams={'motor': {'algorithm': 'PCG64', 'seed': p.seed}}, warnings=result['limitations'])
    return response
