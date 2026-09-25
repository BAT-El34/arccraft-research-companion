# ARCCRAFT literature review protocol

Protocol version: 1.0  
Date frozen: 23 September 2026  
Target venue: Revue Internationale de Management et d'Économie (RIME), pending confirmation of the exact journal identity  
Paper type: Experimental and benchmark paper  
Working language: English, pending final author confirmation

## 1. Provisional title

Procedural Stress Testing of Actuarial Models: Design and Validation of the ARCCRAFT Framework.

## 2. Structured research question

For insurance portfolios and actuarial models exposed to multi-period adverse conditions, does ARCCRAFT, a procedural architecture combining explicit state transitions, structural world validation, reproducible random substreams, failure attribution, and reverse-stress search, improve predictive calibration, tail-risk diagnosis, robustness, failure detection, reproducibility, or diagnostic usefulness relative to transparent frequency-severity and conventional stochastic simulation baselines, and what computational cost or model-risk trade-offs accompany any improvement?

### PECO elements

| Element | Definition |
|---|---|
| Population or phenomenon | Non-life insurance portfolios and actuarial models evaluated under temporal, parameter, operational, and compound stress |
| Exposure or proposed approach | Procedural multi-period stress generation with explicit transitions, dependence, structural validation, deterministic replay, failure attribution, and reverse-stress search |
| Comparators | At least one transparent frequency-severity or aggregate-loss model and one conventional stochastic or Monte Carlo simulation without the additional procedural architecture |
| Outcomes | Central predictive error, proper scoring rules, interval coverage, tail calibration, threshold exceedance, failure-detection performance when ground truth exists, robustness to perturbation and distribution shift, seed variability, replayability, diagnostic value, and computational cost |

The question permits null and negative findings. ARCCRAFT need not outperform a simpler comparator on every outcome.

## 3. Review objectives

1. Determine how actuarial and regulatory literature currently defines credible insurance stress testing.
2. Identify established methods for frequency-severity simulation, dependence, multi-period state evolution, scenario generation, and reverse stress testing.
3. Determine what constitutes valid predictive, distributional, and tail calibration.
4. Separate computational reproducibility from empirical validity and scenario plausibility.
5. Identify existing insurance simulation environments and synthetic-portfolio generators closest to ARCCRAFT.
6. derive fair comparators, falsifiable hypotheses, robustness tests, ablations, and data requirements for the empirical study.

## 4. Coverage period and languages

- Main systematic window: January 2000 to September 2026.
- Foundational sources before 2000 are eligible when they define aggregate-loss models, coherent risk measures, calibration, Monte Carlo practice, stress-testing concepts, or simulation validation still used in the review period.
- Languages: English and French.
- Other languages are excluded unless a complete English or French version is available.

## 5. Eligible source types

- peer-reviewed journal articles;
- peer-reviewed conference papers when computational methods are central;
- scholarly monographs and handbook chapters for established actuarial or simulation methods;
- working papers or preprints when no final version exists and status is clearly identified;
- official regulatory, supervisory, standards, and professional-actuarial publications;
- documented public datasets and open simulation packages used in retained studies.

Blogs, marketing pages, unsourced opinion, duplicated versions, inaccessible records without sufficient bibliographic evidence, and sources that merely mention stress without an actuarial, insurance, simulation, validation, or model-risk contribution are excluded.

## 6. Literature strands

The search covers ten linked strands:

1. frequency-severity, compound loss, and non-life pricing models;
2. Monte Carlo methods, stochastic scenario generation, dependence, and multi-period insurance processes;
3. insurance stress testing, severe-but-plausible scenarios, dynamic stress testing, and reverse stress testing;
4. synthetic insurance portfolios, artificial insurers, claims simulators, and open actuarial datasets;
5. aleatory and epistemic uncertainty, process and observation noise, parameter uncertainty, misspecification, and distribution shift;
6. random-number generation, seeds, independent substreams, deterministic replay, and computational experiment governance;
7. calibration, temporal validation, predictive intervals, proper scoring rules, backtesting, and external validation;
8. VaR, Expected Shortfall, exceedances, tail calibration, sensitivity analysis, and minimum-failure conditions;
9. model risk, scenario plausibility, interpretability, internal consistency, and limits of synthetic evidence;
10. benchmarking, ablation, simulation verification and validation, and computational-budget fairness.

These strands will be synthesized into methodological debates rather than reproduced as ten manuscript subsections.

## 7. Search sources

### Layer 1. Broad scholarly discovery

- Google Scholar;
- Crossref and DOI metadata;
- OpenAlex or equivalent open scholarly metadata where accessible;
- arXiv;
- SSRN;
- publisher platforms including Cambridge Core, Elsevier ScienceDirect, SpringerLink, Wiley, Taylor & Francis, JSTOR, and Project Euclid.

### Layer 2. Specialist sources

- ASTIN Bulletin;
- Insurance: Mathematics and Economics;
- Scandinavian Actuarial Journal;
- Annals of Actuarial Science;
- European Actuarial Journal;
- Journal of Risk and Insurance;
- North American Actuarial Journal;
- IEEE and ACM libraries for random-number and reproducibility methods;
- actuarial professional bodies including the International Actuarial Association, Institute and Faculty of Actuaries, Society of Actuaries, and Casualty Actuarial Society.

### Layer 3. Institutional and regulatory evidence

- EIOPA;
- International Association of Insurance Supervisors;
- Bank of England and Prudential Regulation Authority;
- European Central Bank where insurance or financial stress methodology is relevant;
- International Monetary Fund Financial Sector Assessment Program;
- Financial Stability Board;
- national insurance supervisors and official actuarial standards bodies when directly relevant.

### Layer 4. Citation chasing

For each of the five to ten most central retained sources:

- backward search of references for foundational work;
- forward search for replications, extensions, critiques, and newer validation methods;
- version reconciliation so preprint and journal versions are counted once.

## 8. Boolean keyword families

### Concept A. Insurance and actuarial models

`actuar* OR insurance OR insurer OR "non-life" OR "property casualty" OR "frequency severity" OR "aggregate loss"`

### Concept B. Stress and scenarios

`"stress test*" OR "dynamic stress" OR "reverse stress" OR "severe but plausible" OR "scenario generation" OR "scenario analysis" OR "adverse scenario"`

### Concept C. Procedural simulation

`procedural OR "multi-period simulation" OR "state transition" OR "world generation" OR "synthetic portfolio" OR "simulation environment" OR "agent-based"`

### Concept D. Validation and calibration

`validation OR calibration OR backtest* OR "out-of-sample" OR "predictive interval" OR "proper scoring rule" OR CRPS OR "probability integral transform"`

### Concept E. Tail risk and failure

`"tail risk" OR VaR OR "expected shortfall" OR TVaR OR exceedance OR "failure threshold" OR "failure analysis" OR "minimum failure"`

### Concept F. Uncertainty and robustness

`uncertainty OR noise OR perturbation OR robustness OR misspecification OR "distribution shift" OR aleatory OR epistemic OR sensitivity`

### Concept G. Reproducibility and random streams

`reproducib* OR seed OR "random stream" OR substream OR PCG64 OR "random number generation" OR replay`

### Composite searches

Core search:

`(Concept A) AND (Concept B) AND (Concept D)`

Procedural-novelty search:

`(Concept A) AND (Concept C) AND ((Concept D) OR (Concept G))`

Robustness search:

`(Concept A) AND ((Concept B) OR (Concept C)) AND (Concept F)`

Tail and reverse-stress search:

`(Concept A) AND ((Concept B) OR (Concept E)) AND ((Concept D) OR (Concept F))`

Simulation-governance search:

`((Concept A) OR simulation) AND (Concept G) AND ((Concept D) OR verification)`

Database-specific syntax, title and abstract restrictions, quotation behavior, and truncation will be recorded in the screening log.

## 9. Selection process

1. Record every discovered item with database, query family, date, title, authors, year, DOI or stable URL, and source type.
2. Deduplicate by DOI, normalized title, and version relationship.
3. Screen title and abstract against population, method, and outcome criteria.
4. Assess full text or sufficient official metadata for retained candidates.
5. Record one primary exclusion reason for each full-text exclusion.
6. Target 70 to 100 screened records and retain at least 60 high-relevance sources if the evidence supports that number.

No target count will justify retaining a weak or unverifiable source.

## 10. Extraction fields

For every retained source, record:

- complete reference and DOI;
- discipline and source type;
- research question and contribution;
- data, population, period, sample size, and unit of observation;
- model class and scenario mechanism;
- uncertainty treatment;
- validation and holdout design;
- tail-risk method;
- main result;
- limitations and external-validity boundary;
- role in this paper: baseline, formal definition, metric, hypothesis, robustness test, ablation, data source, or critique.

## 11. Synthesis method

The review will organize evidence around four provisional debates:

1. static shock specification versus dynamic path-dependent simulation;
2. predictive calibration versus exploratory scenario coverage;
3. reproducibility and traceability versus empirical realism;
4. aggregate outcome estimation versus interpretable failure diagnosis.

Each synthesis paragraph must compare multiple sources, identify agreement or contradiction, and derive a requirement for the empirical design. Sequential source summaries are prohibited.

## 12. Quality and verification controls

- Prefer the version of record and verify DOI resolution.
- Label preprints and working papers explicitly.
- Use regulatory sources for regulatory requirements, not for proof of predictive performance.
- Use software documentation only for implementation facts.
- Treat dataset documentation as provenance, not as validation.
- Keep links in the evidence files and use venue-compliant citations in the manuscript.
- Report inaccessible, broken, or ambiguous links separately.
- Do not infer institutional adoption or production deployment.

## 13. Venue adaptation

The official indexed RIME pages describe the journal as an open-access management and economics journal using double-blind review. Its submission guidance calls for an anonymized manuscript, IMRaD structure, APA 7 citations, and verified, numbered tables and figures. These venue requirements override the earlier provisional numbered-reference structure. Exact length, font, spacing, and template-specific instructions remain to be verified from the Word template.

For RIME fit, the paper must explain the economic and managerial relevance of better stress-test governance, model-risk control, reproducibility, and diagnosis for insurers. This framing must not displace the actuarial methodology or create unsupported policy claims.

## 14. Protocol deviations

Any change to the search window, databases, inclusion rules, synthesis debates, or target counts will be dated and justified in a deviation log. Changes made after the empirical results are examined will be labelled post-hoc.

