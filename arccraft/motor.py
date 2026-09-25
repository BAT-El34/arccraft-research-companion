"""Scientific motor calculation extracted without formula changes.

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

def arccraft_empirical_motor(
    start_year: int=2022,
    end_year: int=2023,
    projection_year: int=2024,
    n_simulations: int=10_000,
    seed: int=42,
    frequency_multiplier: float=1.0,
    severity_multiplier: float=1.0,
    expense_ratio: float | None=None,
    commission_ratio: float | None=None,
) -> dict[str,Any]:
    """Experimental frequency-severity simulation calibrated on the external motor portfolio.

    Calibration uses aggregate claim frequency and a lognormal proxy derived from policy-year incurred/claim averages.
    It intentionally distinguishes observed source metrics from scenario assumptions.
    """
    cal=empirical_motor_calibration(start_year,end_year)
    target=empirical_motor_calibration(projection_year,projection_year)
    if not cal["claim_frequency"] or not cal["severity_proxy"]["mu_log"]:
        raise ValueError("Insufficient calibration data")
    n_simulations=min(max(int(n_simulations),500),50_000)
    rng=np.random.default_rng(seed)
    exposure=float(target["exposure"])
    premium=float(target["premium"])
    lam=exposure*float(cal["claim_frequency"])*float(frequency_multiplier)
    claim_counts=rng.poisson(lam,size=n_simulations)
    mu=float(cal["severity_proxy"]["mu_log"])+math.log(max(float(severity_multiplier),1e-9))
    sigma=float(cal["severity_proxy"]["sigma_log"] or 0.0)
    # Aggregate compound-Poisson approximation: conditional sum of lognormal claims.
    # For speed, use mean/variance of lognormal and a normal approximation conditional on N for large counts.
    sev_mean=math.exp(mu+0.5*sigma*sigma)
    sev_var=(math.exp(sigma*sigma)-1.0)*math.exp(2*mu+sigma*sigma)
    mean_total=claim_counts*sev_mean
    sd_total=np.sqrt(np.maximum(claim_counts*sev_var,0.0))
    incurred=np.maximum(rng.normal(mean_total,sd_total),0.0)
    loss_ratio=incurred/premium if premium>0 else np.full(n_simulations,np.nan)
    combined=None
    if expense_ratio is not None and commission_ratio is not None:
        combined=loss_ratio+float(expense_ratio)+float(commission_ratio)
    def qs(a):
        return {"mean":float(np.nanmean(a)),"q025":float(np.nanpercentile(a,2.5)),"q50":float(np.nanpercentile(a,50)),"q975":float(np.nanpercentile(a,97.5))}
    out={
        "schema_version":"arccraft-motor-external-1.0","mode":"PUBLIC_EXTERNAL / EXPERIMENTAL_CALIBRATION",
        "seed":seed,"simulations":n_simulations,"calibration_period":[start_year,end_year],"projection_year":projection_year,
        "assumptions":{"frequency_multiplier":frequency_multiplier,"severity_multiplier":severity_multiplier,
                       "expense_ratio":expense_ratio,"commission_ratio":commission_ratio},
        "calibration":cal,"observed_projection_year":target,
        "predicted_claim_count":qs(claim_counts.astype(float)),"predicted_incurred":qs(incurred),"predicted_loss_ratio":qs(loss_ratio),
        "combined_ratio":qs(combined) if combined is not None else None,
        "validation":{
            "observed_claims":target["claims"],"observed_incurred":target["incurred"],"observed_loss_ratio":target["loss_ratio"],
            "claim_count_error_pct":(float(np.mean(claim_counts))-target["claims"])/target["claims"]*100 if target["claims"] else None,
            "incurred_error_pct":(float(np.mean(incurred))-target["incurred"])/target["incurred"]*100 if target["incurred"] else None,
            "observed_claims_in_95_interval":bool(np.percentile(claim_counts,2.5)<=target["claims"]<=np.percentile(claim_counts,97.5)),
            "observed_incurred_in_95_interval":bool(np.percentile(incurred,2.5)<=target["incurred"]<=np.percentile(incurred,97.5)),
        },
        "limitations":[
            "External public motor portfolio; not automatically transferable to Togo, Mixx by Yas or the CIMA market.",
            "Policy-year incurred amount is not individual-claim severity; the lognormal calibration is an experimental proxy.",
            "Expense and commission ratios are returned as NOT_AVAILABLE unless explicitly supplied as scenario assumptions.",
        ],
    }
    return out
