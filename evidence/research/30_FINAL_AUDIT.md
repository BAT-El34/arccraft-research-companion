# ARCCRAFT final research-package audit

**Audit date:** 24 September 2026  
**Authors:** Elia Batako and Manuel Ntumba  
**Scope:** retrospective benchmark and scientific manuscript draft

## Outcome

The planned retrospective benchmark is complete and reproducible in the inspected local environment. The package is suitable for author review and for preparation in the RIME template. It is not a confirmatory validation package because the 2024 outcome was previously inspected and no independent portfolio or later untouched year is available.

## Executed checks

| Check | Result |
|---|---|
| Backend, database, API, and ARCCRAFT regression suite | 27/27 passed |
| Policy benchmark notebook | 10/10 code cells executed; 0 error outputs |
| Policy model optimization | Frequency and cost models converged at both temporal origins |
| Machine-readable evidence | All CSV outputs 02, 07, 09–14, and 18–27 parse successfully |
| Claim register | 35 unique claims; no duplicate identifiers |
| Python syntax | Engine, policy core, notebook builder, and ablation runner compile successfully |
| Figure QA | Temporal-shift, benchmark-error, decile-calibration, and ablation figures visually inspected |
| Procedural replay | All 15 ablation configuration–seed pairs reproduce exact fingerprints |
| Stream isolation | Full named-stream model invariant; shared-stream ablation changes after irrelevant world draws |
| Manuscript | Integrated 6,654-word scientific draft created with the complete reviewed literature section, bounded claims, and negative findings |

## Evidence conclusions

Supported locally:

- exact same-seed replay;
- random-substream isolation;
- explicit accounting of pass, repair, reject, and failed gates;
- improved held-out count deviance from policy-level frequency differentiation;
- sensitivity of synthetic results to validator policy and transitions.

Not supported:

- complete predictive validation;
- general superiority over conventional actuarial models;
- stability or superiority of the policy-level incurred-cost model;
- empirical plausibility of synthetic scenario classes;
- causal failure attribution;
- stable tail coverage or external generalization.

## Required author inputs before journal submission

1. Affiliations for Elia Batako and Manuel Ntumba.
2. Corresponding-author name and email.
3. Confirmation of the exact RIME author template and current reference requirements.
4. Author review of the title; “preliminary evaluation” is scientifically required unless new independent validation is added.

## Evidence required for stronger future claims

- a prospectively untouched later year or independent motor portfolio;
- claim-level losses and payment development for individual-severity and tail evaluation;
- expense and commission data for empirical combined-ratio validation;
- observed operational traceability outcomes or registered fault-injection labels;
- empirically calibrated state transitions and quantitative scenario-plausibility criteria.

Further tuning against the already inspected 2024 outcome must not be presented as confirmatory testing.
