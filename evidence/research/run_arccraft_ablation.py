from __future__ import annotations

import hashlib
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "mapta-compass-arccraft-platform-v2.1-FINAL" / "mapta-compass-arccraft-poc"
OUT = ROOT / "ARCCRAFT"
FIG = OUT / "figures"
sys.path.insert(0, str(REPO))

from backend.engine.arccraft_engine import (  # noqa: E402
    VARIABLES_ETAT,
    Mondes,
    ResultatValidation,
    construire_failure_atlas,
    construire_flux_nommes,
    cribler_variables,
    decrire_flux_nommes,
    generer_mondes,
    product,
    simuler_trajectoires,
    synthese_failure_atlas,
    valider_mondes,
)


SEEDS = (20260825, 20260826, 20260827)
N_WORLDS = 10_000


def fingerprint(resultats) -> str:
    payload = [
        [
            r.world_id,
            r.regime,
            r.classe,
            r.statut_validation,
            None if not np.isfinite(r.combined_ratio) else round(r.combined_ratio, 12),
            None if not np.isfinite(r.tracabilite_score) else round(r.tracabilite_score, 12),
            r.porte_ratee,
            r.succes,
        ]
        for r in resultats
    ]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def strict_validation(validation: ResultatValidation) -> ResultatValidation:
    statut = validation.statut.copy()
    statut[statut == "REPAIR"] = "REJECT"
    return ResultatValidation(
        statut=statut,
        etat_valide={v: x.copy() for v, x in validation.etat_valide.items()},
    )


def absent_validation(mondes: Mondes) -> ResultatValidation:
    return ResultatValidation(
        statut=np.full(mondes.n, "PASS", dtype=object),
        etat_valide={v: mondes.etat[v].copy() for v in VARIABLES_ETAT},
    )


def run_once(config: str, seed: int, *, perturb_world_stream: bool = False):
    start_total = time.perf_counter()
    start_generation = time.perf_counter()

    if config == "shared_stream":
        shared = np.random.Generator(np.random.PCG64(seed))
        mondes = generer_mondes(shared, n=N_WORLDS)
        if perturb_world_stream:
            shared.random(100)
        claims = shared
        behaviour = shared
        stream_description = {"shared": {"algorithme": "PCG64", "spawn_key": []}}
    else:
        flux = construire_flux_nommes(seed)
        mondes = generer_mondes(flux["world"], n=N_WORLDS)
        if perturb_world_stream:
            flux["world"].random(100)
        claims = flux["claims"]
        behaviour = flux["behaviour"]
        stream_description = decrire_flux_nommes(flux)
    generation_seconds = time.perf_counter() - start_generation

    start_validation = time.perf_counter()
    base_validation = valider_mondes(mondes)
    if config == "no_validator":
        validation = absent_validation(mondes)
    elif config == "strict_reject":
        validation = strict_validation(base_validation)
    else:
        validation = base_validation
    validation_seconds = time.perf_counter() - start_validation

    start_simulation = time.perf_counter()
    resultats = simuler_trajectoires(
        product,
        mondes,
        validation,
        claims,
        behaviour,
        activer_transitions=config != "no_transitions",
    )
    simulation_seconds = time.perf_counter() - start_simulation

    start_diagnostics = time.perf_counter()
    atlas = construire_failure_atlas(resultats, seed, stream_description)
    atlas_summary = synthese_failure_atlas(atlas)
    correlations = cribler_variables(resultats, mondes, validation)
    diagnostics_seconds = time.perf_counter() - start_diagnostics

    accepted = [r for r in resultats if r.statut_validation != "REJECT"]
    finite_cr = [r.combined_ratio for r in accepted if np.isfinite(r.combined_ratio)]
    finite_trace = [r.tracabilite_score for r in accepted if np.isfinite(r.tracabilite_score)]
    rejected = sum(r.statut_validation == "REJECT" for r in resultats)
    repaired = sum(r.statut_validation == "REPAIR" for r in resultats)
    failures = sum(not r.succes for r in accepted)

    metrics = {
        "config": config,
        "seed": seed,
        "n_worlds": N_WORLDS,
        "accepted_worlds": len(accepted),
        "pass_worlds": sum(r.statut_validation == "PASS" for r in resultats),
        "repair_worlds": repaired,
        "reject_worlds": rejected,
        "traceability_failures": atlas_summary["echecs_tracabilite"],
        "combined_ratio_failures": atlas_summary["echecs_ratio_combine"],
        "failure_rate_accepted": failures / len(accepted) if accepted else np.nan,
        "failure_or_reject_rate": (failures + rejected) / N_WORLDS,
        "mean_combined_ratio": float(np.mean(finite_cr)) if finite_cr else np.nan,
        "mean_traceability": float(np.mean(finite_trace)) if finite_trace else np.nan,
        "top_cr_driver": next(iter(correlations)),
        "top_cr_driver_spearman": next(iter(correlations.values())),
        "generation_seconds": generation_seconds,
        "validation_seconds": validation_seconds,
        "simulation_seconds": simulation_seconds,
        "diagnostics_seconds": diagnostics_seconds,
        "total_seconds": time.perf_counter() - start_total,
        "fingerprint": fingerprint(resultats),
    }
    return metrics, resultats


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)

    configs = ("full", "no_validator", "strict_reject", "no_transitions", "shared_stream")
    rows = []
    for seed in SEEDS:
        for config in configs:
            metrics, _ = run_once(config, seed)
            replay_metrics, _ = run_once(config, seed)
            metrics["exact_replay"] = metrics["fingerprint"] == replay_metrics["fingerprint"]
            rows.append(metrics)

    details = pd.DataFrame(rows)
    numeric = [
        "accepted_worlds", "pass_worlds", "repair_worlds", "reject_worlds",
        "traceability_failures", "combined_ratio_failures", "failure_rate_accepted",
        "failure_or_reject_rate", "mean_combined_ratio", "mean_traceability",
        "top_cr_driver_spearman", "generation_seconds", "validation_seconds",
        "simulation_seconds", "diagnostics_seconds", "total_seconds",
    ]
    summary = details.groupby("config", as_index=False)[numeric].agg(["mean", "std"])
    summary.columns = ["config"] + [f"{a}_{b}" for a, b in summary.columns.tolist()[1:]]

    isolation_rows = []
    for config in ("full", "shared_stream"):
        base, _ = run_once(config, SEEDS[0], perturb_world_stream=False)
        perturbed, _ = run_once(config, SEEDS[0], perturb_world_stream=True)
        isolation_rows.append({
            "config": config,
            "intervention": "consume_100_unused_world_draws_before_simulation",
            "baseline_fingerprint": base["fingerprint"],
            "perturbed_fingerprint": perturbed["fingerprint"],
            "claims_and_behaviour_invariant": base["fingerprint"] == perturbed["fingerprint"],
        })
    isolation = pd.DataFrame(isolation_rows)

    details.to_csv(OUT / "25_ARCCRAFT_ABLATION_RESULTS.csv", index=False)
    summary.to_csv(OUT / "26_ARCCRAFT_ABLATION_SUMMARY.csv", index=False)
    isolation.to_csv(OUT / "27_STREAM_ISOLATION_TEST.csv", index=False)

    ordered = list(configs)
    plot = summary.set_index("config").loc[ordered]
    labels = ["Full", "No validator", "Strict reject", "No transitions", "Shared stream"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].bar(
        labels,
        100 * plot["failure_rate_accepted_mean"],
        yerr=100 * plot["failure_rate_accepted_std"],
        capsize=4,
        color="#315f72",
    )
    axes[0].set(ylabel="Failures among accepted worlds (%)", title="Procedural ablation: failure rate")
    axes[0].tick_params(axis="x", rotation=25)
    axes[1].bar(
        labels,
        plot["total_seconds_mean"],
        yerr=plot["total_seconds_std"],
        capsize=4,
        color="#bf6b3b",
    )
    axes[1].set(ylabel="Wall-clock seconds", title=f"Mean runtime ({N_WORLDS:,} worlds)")
    axes[1].tick_params(axis="x", rotation=25)
    for axis in axes:
        axis.set_ylim(bottom=0)
    fig.tight_layout()
    fig.savefig(FIG / "arccraft_ablation_failure_runtime.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    report = f"""# ARCCRAFT procedural ablation report

**Authors:** Elia Batako and Manuel Ntumba  
**Status:** synthetic computational experiment; not empirical product validation  
**Seeds:** {', '.join(map(str, SEEDS))}  
**Worlds per configuration and seed:** {N_WORLDS:,}

## Design

The experiment changes one procedural component at a time relative to the full ARCCRAFT implementation. `no_validator` passes raw worlds directly to the simulator; `strict_reject` rejects every world that the full validator would repair; `no_transitions` holds the validated initial state fixed over the twelve periods; and `shared_stream` replaces the three named PCG64 substreams with one sequential generator. All comparisons remain synthetic and conditional on the current world grammar and product assumptions.

## Reproducibility tests

Every configuration reproduced an identical result fingerprint when rerun with the same seed: **{bool(details['exact_replay'].all())}**. Consuming 100 unused draws from the world stream left the full model invariant: **{bool(isolation.loc[isolation.config == 'full', 'claims_and_behaviour_invariant'].iloc[0])}**. The same intervention changed results under the shared-stream ablation: **{not bool(isolation.loc[isolation.config == 'shared_stream', 'claims_and_behaviour_invariant'].iloc[0])}**. This is direct evidence for stream isolation as an engineering reproducibility property, not evidence of actuarial accuracy.

## Main result

The numerical evidence is stored in `25_ARCCRAFT_ABLATION_RESULTS.csv` and its across-seed summary in `26_ARCCRAFT_ABLATION_SUMMARY.csv`. Differences across validator and transition configurations show that reported failure regions are conditional on procedural design choices. They must therefore be reported with the grammar, validation policy, horizon, seed regime, and gate definitions rather than treated as invariant portfolio facts.

## Interpretation boundary

The ablation evaluates internal computational behaviour. It cannot validate the scenario probabilities, state-transition laws, loss model, or economic realism because those elements remain scenario assumptions. Runtime is wall-clock time on the execution host and is descriptive, not a portable performance guarantee.
"""
    (OUT / "28_ARCCRAFT_ABLATION_REPORT.md").write_text(report, encoding="utf-8")

    print(details[["config", "seed", "failure_rate_accepted", "mean_combined_ratio", "total_seconds", "exact_replay"]].to_string(index=False))
    print("\nStream isolation\n", isolation.to_string(index=False))
    print(f"\nWrote outputs 25-28 and {FIG / 'arccraft_ablation_failure_runtime.png'}")


if __name__ == "__main__":
    main()
