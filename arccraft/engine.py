"""
ARCCRAFT — Stress-testing procédural et Failure Atlas
=======================================================

Statut : SYNTHETIC_DEMO. La grammaire de mondes, la calibration et le
produit testé sont fictifs (statut SCENARIO_ASSUMPTION). Le backtesting
et la validation hors échantillon sont NOT_AVAILABLE faute d'historique
de portefeuille autorisé. Ce moteur ne mesure ni la performance d'un
produit réel, ni un tarif, ni une projection de portefeuille.

Objectif :
    Évaluer la robustesse d'un produit d'assurance non pas sur des
    variables indépendantes, mais sur des trajectoires de monde
    multi-périodes générées par une grammaire combinant régimes
    macroéconomiques, de risque, de comportement, de transaction,
    d'institution et d'opérations — puis identifier, cartographier et
    localiser les échecs plutôt que de les moyenner.

Principe :
    1. Générer des trajectoires Ws,0:T de douze périodes à partir d'une
       seed maître et de sous-flux nommés indépendants (world, claims,
       behaviour), sous l'algorithme PCG64.
    2. Répartir chaque monde entre neuf régimes de stress documentés
       (central, liquidité, sinistres, inflation des prestations,
       défaillance numérique, fraude, adoption forte, backlog
       opérationnel, stress composé) et six classes de scénario
       (BASELINE, ALTERNATIVE, ADVERSE, SEVERE_PLAUSIBLE, EXPLORATORY,
       REVERSE_STRESS). Seules les quatre premières classes alimentent
       la synthèse centrale ; EXPLORATORY est rapportée séparément et
       REVERSE_STRESS fait l'objet d'un rapport dédié.
    3. Valider structurellement chaque monde avant simulation :
       PASS, REPAIR (bornage documenté) ou REJECT (incohérence non
       réparable). Les réparations et rejets ne sont pas effacés.
    4. Simuler le produit sur chaque monde accepté et appliquer une
       porte non compensatoire de traçabilité de paiement avant toute
       lecture du ratio combiné : un bon résultat moyen ne corrige pas
       un défaut d'exécution.
    5. Agréger comme dans une approche de Monte-Carlo, globalement et
       par classe de scénario, et construire un Failure Atlas qui relie
       chaque échec à sa seed, son régime et sa porte.
    6. Effectuer un criblage par corrélation de rang pour identifier les
       variables les plus associées au ratio combiné, dans les limites
       du générateur — pas comme relations empiriques calibrées.
    7. Rechercher un stress inverse : le monde synthétique le plus
       proche du scénario central qui échoue malgré tout, pour
       distinguer une fragilité procédurale d'une fragilité actuarielle.

Règle fondamentale :
    La seed génère le monde. Les caractéristiques du produit restent
    fixes pendant l'évaluation, sauf lorsqu'un scénario expérimental
    prévoit explicitement leur modification. Une porte non compensatoire
    ratée classe le monde comme défaillant même si le ratio combiné est
    excellent : le taux d'échec global doit toujours être décomposé par
    porte avant interprétation.
"""

from __future__ import annotations

import argparse
import csv
import json
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Configuration globale et gouvernance des seeds
# ---------------------------------------------------------------------------

SEED_MASTER = 20260825
ALGORITHME = "PCG64"
N_WORLDS = 10_000
T_PERIODES = 12
SCHEMA_VERSION = "arccraft-output-1.0"
MODEL_VERSION = "0.1.0"
GRAMMAIRE_VERSION = "world_grammar-0.1.0"
CALIBRATION_STATUT = "SCENARIO_ASSUMPTION"
DEMO_STATUS = "SYNTHETIC_DEMO"

SEUIL_TRACABILITE = 0.95   # porte non compensatoire : traçabilité de paiement
SEUIL_RATIO_COMBINE = 1.0  # au-delà, le monde est en perte technique

# Neuf régimes de stress documentés (biomes B0-B8, Annexe 9)
REGIMES: dict[str, str] = {
    "B0": "central",
    "B1": "liquidite",
    "B2": "sinistres",
    "B3": "inflation_prestations",
    "B4": "defaillance_numerique",
    "B5": "pression_fraude",
    "B6": "adoption_forte",
    "B7": "backlog_operationnel",
    "B8": "stress_compose",
}

# Classes de scénario : proportion cible de tirage et inclusion dans la
# synthèse centrale (Annexe 9)
CLASSES_SCENARIO: dict[str, dict[str, Any]] = {
    "BASELINE": {"proportion": 0.12, "intensite": 0.15, "inclus_synthese": True, "statut_usage": "synthese_centrale"},
    "ALTERNATIVE": {"proportion": 0.22, "intensite": 0.55, "inclus_synthese": True, "statut_usage": "synthese_centrale"},
    "ADVERSE": {"proportion": 0.44, "intensite": 1.10, "inclus_synthese": True, "statut_usage": "synthese_centrale"},
    "SEVERE_PLAUSIBLE": {"proportion": 0.12, "intensite": 2.00, "inclus_synthese": True, "statut_usage": "synthese_centrale_separable"},
    "EXPLORATORY": {"proportion": 0.10, "intensite": None, "inclus_synthese": False, "statut_usage": "rapporte_separement"},
}

# Chocs additifs par régime, appliqués à l'état central et mis à l'échelle
# par l'intensité de la classe de scénario. Clés = variables d'état.
CHOCS_REGIME: dict[str, dict[str, float]] = {
    "B0": {},
    "B1": {"liquidite": -0.30, "lapse_rate": +0.15},
    "B2": {"claim_freq_mult": +0.50, "claim_sev_mult": +0.30},
    "B3": {"medical_inflation": +0.08, "claim_sev_mult": +0.40},
    "B4": {"digital_reliability": -0.35, "network_availability": -0.35},
    "B5": {"fraud_pressure": +0.15, "claim_freq_mult": +0.15},
    "B6": {"adoption_load": +0.60},
    "B7": {"backlog_capacity": -0.40, "network_availability": -0.15},
    "B8": {"liquidite": -0.15, "claim_freq_mult": +0.25, "digital_reliability": -0.18,
           "backlog_capacity": -0.20, "fraud_pressure": +0.07},
}

# État central (moyenne à t=0, avant choc de régime)
ETAT_CENTRAL: dict[str, float] = {
    "inflation_rate": 0.05, "medical_inflation": 0.06, "liquidite": 0.85,
    "claim_freq_mult": 1.00, "claim_sev_mult": 1.00, "digital_reliability": 0.92,
    "network_availability": 0.95, "fraud_pressure": 0.05, "adoption_load": 1.00,
    "backlog_capacity": 0.90, "lapse_rate": 0.15,
}

# Bornes structurelles pour le validateur (dur = REJECT, souple = REPAIR)
BORNES_DURES: dict[str, tuple[float, float]] = {
    "liquidite": (-0.4, 1.5), "digital_reliability": (-0.4, 1.5),
    "network_availability": (-0.4, 1.5), "backlog_capacity": (-0.4, 1.5),
    "claim_freq_mult": (-0.2, 3.5), "claim_sev_mult": (-0.2, 3.5),
    "fraud_pressure": (-0.2, 1.5), "lapse_rate": (-0.2, 1.5),
}
BORNES_SOUPLES: dict[str, tuple[float, float]] = {
    "liquidite": (0.0, 1.0), "digital_reliability": (0.0, 1.0),
    "network_availability": (0.0, 1.0), "backlog_capacity": (0.0, 1.0),
    "claim_freq_mult": (0.0, 4.0), "claim_sev_mult": (0.0, 4.0),
    "fraud_pressure": (0.0, 1.0), "lapse_rate": (0.0, 1.0),
}

VARIABLES_ETAT = list(ETAT_CENTRAL.keys())


# ---------------------------------------------------------------------------
# Produit d'assurance à tester
# ---------------------------------------------------------------------------

product: dict[str, Any] = {
    "name": "P_DEMO_ACCIDENT_FLEX",
    "premium": 2800, "payment_frequency": "monthly", "contract_duration": 12,
    "coverage_limit": 500_000, "deductible": 5_000, "coinsurance_rate": 0.10,
    "waiting_period": 30, "base_claim_frequency": 0.09,
    "severity_distribution": "lognormal", "severity_parameters": {"mean": 10.3, "sigma": 0.7},
    "expense_ratio": 0.20, "commission_ratio": 0.10, "initial_exposure": 10_000,
    "premium_frequency": "monthly", "contract_duration_months": 12,
    "statut": DEMO_STATUS,
}
"""
"name" identifie l'archétype produit (synthétique, non tarifé).
Les autres clés reprennent la structure standard du dispositif :
premium, payment_frequency, contract_duration, coverage_limit, deductible,
coinsurance_rate, waiting_period, base_claim_frequency, severity_distribution,
severity_parameters, expense_ratio, commission_ratio, initial_exposure,
premium_frequency, contract_duration_months.
"""


# ---------------------------------------------------------------------------
# Registre de reproductibilité : seed maître, sous-flux nommés
# ---------------------------------------------------------------------------

@dataclass
class RegistreSeed:
    experiment_id: str
    seed_master: int
    algorithme: str
    sous_flux: tuple[str, ...]
    grammaire_version: str
    calibration_version: str
    produit_version: str
    moteur_version: str


def construire_flux_nommes(seed_master: int = SEED_MASTER) -> dict[str, np.random.Generator]:
    """Dérive trois flux indépendants et nommés (world, claims, behaviour) à
    partir d'une unique seed maître, via SeedSequence.spawn — rejouable à
    l'identique en repassant la même seed maître."""
    seq_master = np.random.SeedSequence(seed_master)
    seq_world, seq_claims, seq_behaviour = seq_master.spawn(3)
    return {
        "world": np.random.Generator(np.random.PCG64(seq_world)),
        "claims": np.random.Generator(np.random.PCG64(seq_claims)),
        "behaviour": np.random.Generator(np.random.PCG64(seq_behaviour)),
    }


def decrire_flux_nommes(flux_nommes: dict[str, np.random.Generator]) -> dict[str, dict[str, Any]]:
    """Expose des identifiants de sous-flux stables sans sérialiser leur état interne."""
    return {
        nom: {
            "algorithme": type(rng.bit_generator).__name__,
            "spawn_key": list(rng.bit_generator.seed_seq.spawn_key),
        }
        for nom, rng in flux_nommes.items()
    }


# ---------------------------------------------------------------------------
# Génération de la grammaire de mondes (vectorisée sur N mondes)
# ---------------------------------------------------------------------------

@dataclass
class Mondes:
    """Tableau de N mondes, un par colonne, sur toutes les variables d'état."""
    n: int
    regime: np.ndarray            # (N,) codes régime B0..B8
    classe: np.ndarray            # (N,) classes de scénario
    etat: dict[str, np.ndarray]   # variable -> (N,) valeurs à t=0, avant validation


def generer_mondes(rng_world: np.random.Generator, n: int = N_WORLDS) -> Mondes:
    """Tire N mondes : classe de scénario, régime, puis état initial choqué
    et bruité selon la grammaire (Annexe 9)."""
    classes = list(CLASSES_SCENARIO.keys())
    p_classes = np.array([CLASSES_SCENARIO[c]["proportion"] for c in classes])
    p_classes = p_classes / p_classes.sum()
    classe = rng_world.choice(classes, size=n, p=p_classes)

    regime = np.empty(n, dtype=object)
    regimes_stress = [r for r in REGIMES if r != "B0"]
    for i, c in enumerate(classe):
        if c == "BASELINE":
            regime[i] = "B0"  # la classe centrale correspond au régime central
        else:
            regime[i] = rng_world.choice(regimes_stress)

    etat: dict[str, np.ndarray] = {v: np.full(n, ETAT_CENTRAL[v], dtype=float) for v in VARIABLES_ETAT}

    for i in range(n):
        c = classe[i]
        r = regime[i]
        if c == "EXPLORATORY":
            # Recherche hors calibration centrale : intensité tirée dans une
            # plage étendue, potentiellement plus large que les bornes souples.
            intensite = rng_world.uniform(0.4, 3.0)
        else:
            intensite = CLASSES_SCENARIO[c]["intensite"]
        chocs = CHOCS_REGIME[r]
        for var, choc in chocs.items():
            etat[var][i] += choc * intensite
        # Bruit gaussien propre à chaque monde, également mis à l'échelle
        # par l'intensité de la classe.
        for var in VARIABLES_ETAT:
            etat[var][i] += rng_world.normal(0.0, 0.04 * max(intensite, 0.3))

    return Mondes(n=n, regime=regime, classe=classe, etat=etat)


# ---------------------------------------------------------------------------
# Validateur structurel : PASS / REPAIR / REJECT
# ---------------------------------------------------------------------------

@dataclass
class ResultatValidation:
    statut: np.ndarray            # (N,) "PASS" / "REPAIR" / "REJECT"
    etat_valide: dict[str, np.ndarray]  # état après réparation éventuelle


def valider_mondes(mondes: Mondes) -> ResultatValidation:
    """Vérifie chaque monde contre les bornes dures (REJECT si dépassées) et
    les bornes souples (REPAIR = bornage documenté). Les mondes rejetés
    conservent leur état brut pour la traçabilité, mais ne sont pas simulés."""
    n = mondes.n
    statut = np.full(n, "PASS", dtype=object)
    etat_valide = {v: mondes.etat[v].copy() for v in VARIABLES_ETAT}

    for var, (lo_dur, hi_dur) in BORNES_DURES.items():
        hors_bornes_dures = (mondes.etat[var] < lo_dur) | (mondes.etat[var] > hi_dur)
        statut[hors_bornes_dures] = "REJECT"

    for var, (lo_souple, hi_souple) in BORNES_SOUPLES.items():
        hors_bornes_souples = (mondes.etat[var] < lo_souple) | (mondes.etat[var] > hi_souple)
        a_reparer = hors_bornes_souples & (statut != "REJECT")
        statut[a_reparer] = np.where(statut[a_reparer] == "PASS", "REPAIR", statut[a_reparer])
        etat_valide[var] = np.clip(mondes.etat[var], lo_souple, hi_souple)

    return ResultatValidation(statut=statut, etat_valide=etat_valide)


# ---------------------------------------------------------------------------
# Simulation du produit sur une trajectoire de 12 périodes
# ---------------------------------------------------------------------------

@dataclass
class ResultatMonde:
    world_id: int
    regime: str
    classe: str
    statut_validation: str
    combined_ratio: float
    tracabilite_score: float
    porte_ratee: str            # "" si succès, sinon "tracabilite" ou "ratio_combine"
    succes: bool


def simuler_trajectoires(
    produit: dict[str, Any], mondes: Mondes, validation: ResultatValidation,
    flux_claims: np.random.Generator, flux_behaviour: np.random.Generator,
    t_periodes: int = T_PERIODES,
    activer_transitions: bool = True,
) -> list[ResultatMonde]:
    """Simule chaque monde accepté (PASS/REPAIR) sur douze périodes et
    applique la porte non compensatoire de traçabilité avant lecture du
    ratio combiné. Les mondes REJECT ne sont pas simulés."""
    n = mondes.n
    accepte = validation.statut != "REJECT"
    idx_acceptes = np.where(accepte)[0]

    # Les trajectoires sont un état de travail. Ne jamais modifier l'objet de
    # validation : il doit rester réutilisable pour les contrôles et replays.
    etat = {var: valeurs.copy() for var, valeurs in validation.etat_valide.items()}
    freq_an = 12
    resultats: list[ResultatMonde] = []

    primes_cum = np.zeros(n)
    sinistres_cum = np.zeros(n)
    trace_cum = np.zeros(n)

    exposure = produit["initial_exposure"]

    for t in range(t_periodes):
        lapse = np.clip(etat["lapse_rate"], 0, 1)
        digitalisation = np.clip((etat["digital_reliability"] + etat["network_availability"]) / 2, 0, 1)
        exposure_periode = exposure * (1 - lapse * (t / t_periodes) * 0.5) * (0.5 + 0.5 * digitalisation)

        facteur_collecte = np.clip(1 - etat["inflation_rate"] * 0.5, 0.4, 1.0) * np.clip(etat["liquidite"], 0.2, 1.0)
        primes_periode = produit["premium"] * exposure_periode * facteur_collecte
        primes_cum += np.where(accepte, primes_periode, 0.0)

        lam = np.clip(
            produit["base_claim_frequency"] / freq_an
            * np.clip(etat["claim_freq_mult"], 0, None)
            * (1 + np.clip(etat["fraud_pressure"], 0, None))
            * exposure_periode, 0, None,
        )
        sinistres_survenus = flux_claims.poisson(np.where(accepte, lam, 0.0))

        params = produit["severity_parameters"]
        sigma_base = params.get("sigma", 0.8)
        montants_periode = np.zeros(n)
        for i in idx_acceptes:
            k = sinistres_survenus[i]
            if k <= 0:
                continue
            sigma_i = max(sigma_base * max(etat["claim_sev_mult"][i], 0.1) * (1 + 0.3 * max(etat["medical_inflation"][i], 0)), 0.05)
            severites = flux_claims.lognormal(params.get("mean", 10.0), sigma_i, size=k)
            nets = np.clip(severites - produit["deductible"], 0, None) * (1 - produit["coinsurance_rate"])
            nets = np.minimum(nets, produit["coverage_limit"])
            montants_periode[i] = nets.sum()
        sinistres_cum += montants_periode

        tracabilite_periode = np.clip(
            0.55 * etat["digital_reliability"] + 0.30 * etat["network_availability"]
            + 0.25 * etat["backlog_capacity"] - 0.10 * np.clip(etat["fraud_pressure"], 0, None)
            + flux_behaviour.normal(0.0, 0.01, size=n),
            0.0, 1.0,
        )
        trace_cum += np.where(accepte, tracabilite_periode, 0.0)

        if activer_transitions:
            # Dérive légère des variables d'état d'une période à l'autre.
            # Le commutateur sert aux ablations documentées ; la valeur par
            # défaut conserve le comportement versionné du moteur.
            for var in VARIABLES_ETAT:
                etat[var] = etat[var] + flux_behaviour.normal(0.0, 0.01, size=n)

    frais = produit["expense_ratio"] * primes_cum
    commissions = produit["commission_ratio"] * primes_cum
    combined_ratio = np.divide(
        sinistres_cum + frais + commissions, primes_cum,
        out=np.full(n, np.inf), where=primes_cum > 0,
    )
    tracabilite_score = trace_cum / t_periodes

    for i in range(n):
        if not accepte[i]:
            resultats.append(ResultatMonde(
                world_id=i, regime=mondes.regime[i], classe=mondes.classe[i],
                statut_validation=validation.statut[i], combined_ratio=float("nan"),
                tracabilite_score=float("nan"), porte_ratee="rejete_avant_simulation", succes=False,
            ))
            continue

        porte_ratee = ""
        succes = True
        if tracabilite_score[i] < SEUIL_TRACABILITE:
            porte_ratee = "tracabilite"
            succes = False
        elif combined_ratio[i] >= SEUIL_RATIO_COMBINE:
            porte_ratee = "ratio_combine"
            succes = False

        resultats.append(ResultatMonde(
            world_id=i, regime=mondes.regime[i], classe=mondes.classe[i],
            statut_validation=validation.statut[i], combined_ratio=float(combined_ratio[i]),
            tracabilite_score=float(tracabilite_score[i]), porte_ratee=porte_ratee, succes=succes,
        ))

    return resultats


# ---------------------------------------------------------------------------
# Agrégation par classe de scénario et Failure Atlas
# ---------------------------------------------------------------------------

def agreger_par_classe(resultats: list[ResultatMonde]) -> dict[str, dict[str, float]]:
    """N'agrège que les mondes simulés (PASS/REPAIR). EXPLORATORY est
    rapportée séparément, jamais mélangée à la synthèse centrale."""
    rapport: dict[str, dict[str, float]] = {}
    for classe, meta in CLASSES_SCENARIO.items():
        sous = [r for r in resultats if r.classe == classe and r.statut_validation != "REJECT"]
        if not sous:
            continue
        rapport[classe] = {
            "mondes_acceptes": len(sous),
            "taux_echec_synthetique": float(np.mean([not r.succes for r in sous])),
            "ratio_combine_moyen": float(np.mean([r.combined_ratio for r in sous])),
            "statut_usage": meta["statut_usage"],
        }
    return rapport


def construire_failure_atlas(
    resultats: list[ResultatMonde], seed_master: int,
    flux_nommes: dict[str, Any],
) -> list[dict[str, Any]]:
    """Relie chaque échec ou rejet à sa seed, son régime et sa porte."""
    atlas = []
    for r in resultats:
        if r.succes:
            continue
        atlas.append({
            "world_id": r.world_id, "regime": r.regime, "regime_label": REGIMES.get(r.regime, r.regime),
            "classe": r.classe, "porte_ratee": r.porte_ratee,
            "combined_ratio": r.combined_ratio if np.isfinite(r.combined_ratio) else None,
            "tracabilite_score": r.tracabilite_score if np.isfinite(r.tracabilite_score) else None,
            "seed_master": int(seed_master), "sous_flux": flux_nommes,
        })
    return atlas


def synthese_failure_atlas(atlas: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "echecs_tracabilite": sum(1 for a in atlas if a["porte_ratee"] == "tracabilite"),
        "echecs_ratio_combine": sum(1 for a in atlas if a["porte_ratee"] == "ratio_combine"),
        "mondes_rejetes_avant_simulation": sum(1 for a in atlas if a["porte_ratee"] == "rejete_avant_simulation"),
    }


# ---------------------------------------------------------------------------
# Criblage par corrélation de rang (Spearman, implémentation numpy)
# ---------------------------------------------------------------------------

def _rang(x: np.ndarray) -> np.ndarray:
    ordre = x.argsort()
    rangs = np.empty_like(ordre, dtype=float)
    rangs[ordre] = np.arange(len(x))
    return rangs


def correlation_rang(x: np.ndarray, y: np.ndarray) -> float:
    rx, ry = _rang(x), _rang(y)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def cribler_variables(resultats: list[ResultatMonde], mondes: Mondes, validation: ResultatValidation) -> dict[str, float]:
    """Corrèle chaque variable d'état à t=0 (avant validation) avec le
    ratio combiné final, uniquement sur les mondes simulés."""
    idx = np.array([r.world_id for r in resultats if r.statut_validation != "REJECT"])
    combined = np.array([r.combined_ratio for r in resultats if r.statut_validation != "REJECT"])
    valides = np.isfinite(combined)
    idx, combined = idx[valides], combined[valides]

    correlations: dict[str, float] = {}
    for var in VARIABLES_ETAT:
        correlations[var] = correlation_rang(mondes.etat[var][idx], combined)
    return dict(sorted(correlations.items(), key=lambda kv: abs(kv[1]) if np.isfinite(kv[1]) else -1, reverse=True))


# ---------------------------------------------------------------------------
# Stress inverse : échec synthétique le plus proche du centre
# ---------------------------------------------------------------------------

def recherche_stress_inverse(
    produit: dict[str, Any], seed_master: int = SEED_MASTER,
    n_perturbations: int = 500, pas_max: float = 2.5,
) -> dict[str, Any] | None:
    """Explore des perturbations croissantes autour du scénario central
    (régime B0) et retient l'échec le plus proche selon une distance
    standardisée — pas un optimum global."""
    # Domaine de seed dédié : le résultat ne dépend pas de la consommation
    # antérieure des flux de la simulation principale.
    seq_reverse = np.random.SeedSequence([int(seed_master), 0xAACC])
    seq_world, seq_claims, seq_behaviour = seq_reverse.spawn(3)
    rng_world = np.random.Generator(np.random.PCG64(seq_world))
    rng_claims = np.random.Generator(np.random.PCG64(seq_claims))
    rng_behaviour = np.random.Generator(np.random.PCG64(seq_behaviour))
    n = n_perturbations
    pas = np.linspace(0.05, pas_max, n)

    regime = np.full(n, "B0", dtype=object)
    classe = np.full(n, "REVERSE_STRESS", dtype=object)
    etat = {v: np.full(n, ETAT_CENTRAL[v], dtype=float) for v in VARIABLES_ETAT}
    ecarts_std = np.zeros(n)
    for i in range(n):
        direction = rng_world.normal(0.0, 1.0, size=len(VARIABLES_ETAT))
        direction = direction / (np.linalg.norm(direction) + 1e-9)
        for j, var in enumerate(VARIABLES_ETAT):
            deplacement = direction[j] * pas[i] * 0.15
            etat[var][i] += deplacement
        ecarts_std[i] = pas[i]

    mondes = Mondes(n=n, regime=regime, classe=classe, etat=etat)
    validation = valider_mondes(mondes)
    resultats = simuler_trajectoires(
        produit, mondes, validation, rng_claims, rng_behaviour,
    )

    echecs = [(i, r, ecarts_std[i]) for i, r in enumerate(resultats) if not r.succes and r.statut_validation != "REJECT"]
    if not echecs:
        return None
    i_min, r_min, distance = min(echecs, key=lambda t: t[2])
    return {
        "world_id_perturbation": i_min, "distance_standardisee": float(distance),
        "porte_ratee": r_min.porte_ratee, "tracabilite_score": r_min.tracabilite_score,
        "combined_ratio": r_min.combined_ratio,
    }


# ---------------------------------------------------------------------------
# Readiness et contrat de sortie versionné (schéma arccraft-output-1.0)
# ---------------------------------------------------------------------------

def evaluer_readiness() -> tuple[str, list[str]]:
    """Applique la règle fail-closed : backtesting et validation hors
    échantillon sont NOT_AVAILABLE faute d'historique de portefeuille
    autorisé, donc aucune conclusion de robustesse réelle n'est produite."""
    manquantes = ["backtesting_portefeuille", "validation_hors_echantillon"]
    return "BLOCKED", manquantes


def construire_contrat_sortie(
    rapport_classes: dict[str, dict[str, float]], synthese_atlas: dict[str, int],
    registre: RegistreSeed, readiness: tuple[str, list[str]],
) -> dict[str, Any]:
    statut_readiness, manquantes = readiness
    return {
        "schema_version": SCHEMA_VERSION,
        "execution_id": registre.experiment_id,
        "produit": product["name"],
        "classes_synthese": rapport_classes,
        "failure_atlas_synthese": synthese_atlas,
        "calibration_statut": CALIBRATION_STATUT,
        "readiness_backtesting": {"statut": statut_readiness, "variables_manquantes": manquantes},
        "version_modele": registre.moteur_version,
        "version_grammaire": registre.grammaire_version,
        "registre_seed": {
            "seed_master": registre.seed_master, "algorithme": registre.algorithme,
            "sous_flux": list(registre.sous_flux),
        },
        "statut_donnee": DEMO_STATUS,
    }


# ---------------------------------------------------------------------------
# Rapport et export
# ---------------------------------------------------------------------------

def imprimer_rapport(
    rapport_classes: dict[str, dict[str, float]], synthese_atlas: dict[str, int],
    criblage: dict[str, float], stress_inverse: dict[str, Any] | None, readiness: tuple[str, list[str]],
) -> None:
    print("=" * 78)
    print(f"ARCCRAFT — {product['name']} ({DEMO_STATUS}, calibration {CALIBRATION_STATUT})")
    print("=" * 78)
    print("-- Profil de robustesse synthétique par classe de scénario --")
    for classe, s in rapport_classes.items():
        print(f"  {classe:<18} n={s['mondes_acceptes']:<6} "
              f"échec={s['taux_echec_synthetique']:.2%}  CR moy={s['ratio_combine_moyen']:.3f}  "
              f"[{s['statut_usage']}]")
    print()
    print("-- Failure Atlas --")
    for k, v in synthese_atlas.items():
        print(f"  {k:<32} {v}")
    print()
    print("-- Criblage par corrélation de rang (top 5) --")
    for var, corr in list(criblage.items())[:5]:
        print(f"  {var:<24} {corr:+.3f}")
    print()
    print("-- Stress inverse --")
    if stress_inverse:
        print(f"  Échec le plus proche du centre : distance={stress_inverse['distance_standardisee']:.3f}  "
              f"porte={stress_inverse['porte_ratee']}  "
              f"tracabilite={stress_inverse['tracabilite_score']:.3f}  "
              f"CR={stress_inverse['combined_ratio']:.3f}")
    else:
        print("  Aucun échec trouvé dans le budget de perturbations exploré.")
    print()
    statut_readiness, manquantes = readiness
    print(f"Readiness robustesse réelle : {statut_readiness} (manquant : {', '.join(manquantes)})")
    print("=" * 78)


def exporter_csv(resultats: list[ResultatMonde], chemin: str) -> None:
    champs = list(asdict(resultats[0]).keys())
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        for r in resultats:
            writer.writerow(asdict(r))


def exporter_json(objet: Any, chemin: str) -> None:
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(objet, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="ARCCRAFT — stress-testing procédural et Failure Atlas (SYNTHETIC_DEMO)")
    parser.add_argument("--seed", type=int, default=SEED_MASTER)
    parser.add_argument("--n-worlds", type=int, default=N_WORLDS)
    parser.add_argument("--out-dir", type=str, default=".")
    args = parser.parse_args()

    flux = construire_flux_nommes(args.seed)
    registre = RegistreSeed(
        experiment_id=str(uuid.uuid4()), seed_master=args.seed, algorithme=ALGORITHME,
        sous_flux=("world", "claims", "behaviour"), grammaire_version=GRAMMAIRE_VERSION,
        calibration_version=CALIBRATION_STATUT, produit_version="P_DEMO_ACCIDENT_FLEX-0.1.0",
        moteur_version=MODEL_VERSION,
    )

    mondes = generer_mondes(flux["world"], n=args.n_worlds)
    validation = valider_mondes(mondes)
    resultats = simuler_trajectoires(product, mondes, validation, flux["claims"], flux["behaviour"])

    rapport_classes = agreger_par_classe(resultats)
    atlas = construire_failure_atlas(resultats, args.seed, decrire_flux_nommes(flux))
    synthese_atlas = synthese_failure_atlas(atlas)
    criblage = cribler_variables(resultats, mondes, validation)
    stress_inverse = recherche_stress_inverse(product, args.seed)
    readiness = evaluer_readiness()

    imprimer_rapport(rapport_classes, synthese_atlas, criblage, stress_inverse, readiness)

    n_pass = int(np.sum(validation.statut == "PASS"))
    n_repair = int(np.sum(validation.statut == "REPAIR"))
    n_reject = int(np.sum(validation.statut == "REJECT"))
    print(f"\nValidateur structurel : {n_pass} PASS, {n_repair} REPAIR, {n_reject} REJECT (sur {mondes.n} mondes)")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    exporter_csv(resultats, str(out_dir / "arccraft_resultats.csv"))
    exporter_json(atlas, str(out_dir / "arccraft_failure_atlas.json"))
    contrat = construire_contrat_sortie(rapport_classes, synthese_atlas, registre, readiness)
    exporter_json(contrat, str(out_dir / "arccraft_contrat_sortie.json"))

    print(f"\nExports : {out_dir / 'arccraft_resultats.csv'} , "
          f"{out_dir / 'arccraft_failure_atlas.json'} , {out_dir / 'arccraft_contrat_sortie.json'}")


if __name__ == "__main__":
    main()
