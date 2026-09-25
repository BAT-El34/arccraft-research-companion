# ARCCRAFT research paper work plan

Status date: 24 September 2026  
Status: ARCCRAFT-only scope confirmed; literature review, complete data audit, matched retrospective policy benchmark, procedural ablations, and integrated manuscript draft completed  
Paper type: Experimental and benchmark paper, confirmed by the authors

## 1. Purpose and integrity rule

This plan converts the material currently present in the workspace into a defensible research workflow for a paper on procedural actuarial stress testing. It distinguishes verified resources from documentation claims, synthetic outputs from empirical evidence, and exploratory validation from confirmatory validation.

ARCCRAFT must be presented as a proposed computational architecture. Reproducibility of a simulation is evidence that the computation can be replayed; it is not evidence of realism, calibration, external validity, superiority, adoption, or production readiness. All claims of comparative value must be linked to pre-specified metrics and measured against credible baselines.

## 2. Provisional research focus

### 2.1 Confirmed topic

Procedural Stress Testing of Actuarial Models: Design and Validation of the ARCCRAFT Framework.

### 2.2 Provisional structured question

For insurance portfolios evaluated under temporal and scenario stress, does a reproducible multi-period procedural architecture with world validation, named random substreams, failure attribution, and reverse-stress search improve failure detection, distributional calibration, tail-risk diagnosis, robustness, or reproducibility relative to transparent frequency-severity and conventional stochastic simulation baselines, and at what computational cost?

This question is falsifiable. ARCCRAFT may fail to improve one or more dimensions, and any such result must be reported.

### 2.3 Recommended scope

The paper is exclusively about ARCCRAFT: Actuarial Risk & Contingency Computational, Reproducible Architecture for Failure Testing. It will focus on the methodological contribution and one motor-insurance demonstration. The Togo insurance benchmark and the macro-financial databases may provide context, but they should not be used to imply empirical validation of ARCCRAFT for Togo, Mixx by Yas, the CIMA market, or any institution.

MAPTA and COMPASS are outside the paper's scope. Their methods, results, interfaces, and claims will not appear in the manuscript unless needed only to explain repository boundaries.

## 3. Resources actually available

### 3.1 Research brief

The supplied research brief defines:

- information-integrity constraints;
- an experimental and benchmark orientation for ARCCRAFT;
- a four-layer literature search and PRISMA-style accounting process;
- a mandatory post-literature data gate;
- a fixed paper structure and approximately 30-page limit;
- required validation, robustness, ablation, tail-risk, reproducibility, and citation audits;
- a single Markdown manuscript as the final writing artifact.

The brief contains process requirements, not academic evidence. It cannot be cited as literature or used to substantiate actuarial claims.

### 3.2 Executable software

The repository contains a TypeScript front end and a Python/FastAPI backend. The components relevant to the proposed paper are:

- `backend/engine/arccraft_engine.py`: 658 lines implementing the synthetic procedural engine;
- `backend/model_service.py`: the synthetic API wrapper and an external motor frequency-severity experiment;
- `backend/data_service.py`: database access, annual motor summaries, and aggregate calibration;
- `backend/build_data_store.py`: source ingestion and database construction logic;
- `scripts/verify_backend.py`, `scripts/verify_design.py`, and `scripts/smoke.mjs`: software and data checks;
- an included Git repository based on commit `b3df670` on `main`; the working tree now contains the documented ARCCRAFT reproducibility corrections and research tests.

The ARCCRAFT engine currently includes:

- a master seed and named random substreams;
- 10,000-world default simulation over 12 periods;
- nine stress regimes and scenario classes;
- PASS, REPAIR, and REJECT structural validation;
- a combined-ratio and payment-traceability failure mechanism;
- scenario-class aggregation;
- a Failure Atlas linking failed worlds to seeds, regimes, and failed gates;
- rank-correlation screening;
- a reverse-stress search;
- an explicit readiness status.

The current implementation is valuable as a prototype and reproducible experimental object. A matched external policy benchmark and internal procedural ablation suite are now available, but they do not constitute independent confirmatory validation.

### 3.3 Data resources

The included read-only SQLite database is 205,217,792 bytes and passes `PRAGMA integrity_check`. Its verified tables are:

| Resource | Rows | Current research role | Main limitation |
|---|---:|---|---|
| Motor portfolio | 354,140 | Primary empirical demonstration | External policy-year portfolio; not Togo-specific; no individual claim severity |
| Togo insurance benchmark | 200 | Documentary and contextual evidence | Product-actor-source records, not a loss-history dataset |
| IMF FAS | 19,256 | Contextual covariates or background | No direct linkage to the motor portfolio |
| WDI | 764,129 | Contextual covariates or background | No direct linkage to the motor portfolio |
| Global Findex | 8,702 | Financial-inclusion context | 17 of 19 study economies; not actuarial outcomes |
| GFD | 17,180 | Financial-development context | 13 economies in the supplied extract |
| GSMA Mobile Money | 58,975 | Distribution and payment context | Not linked to claim-level outcomes |
| MMPI | 618 | Poverty context | Not linked to claim-level outcomes |
| Motor variable dictionary | 69 | Schema documentation | Does not replace source provenance or data-generating documentation |

Only two normalized CSV files are bundled: the 200-row insurance benchmark and the 69-row motor variable dictionary. The original approximately 94.7 MB motor CSV, the original benchmark workbook, the quantitative-data archive, and the motor dictionary workbook are not included. Their filenames, sizes, and SHA-256 values are recorded in `data/manifest.json`, but their content cannot be independently reconstructed from the present workspace alone.

### 3.4 Motor portfolio quality checks completed

The motor database contains 354,140 policy-year rows and 185,678 distinct insured identifiers. The compound key `insured_id` plus `year` has no duplicates. The four critical aggregate fields inspected, exposure, claims, incurred loss, and premium, contain no null values and no negative values. Exposure ranges from zero to one.

Verified annual aggregates are:

| Year | Policy rows | Exposure | Claims | Incurred loss | Premium | Claim frequency | Average severity | Loss ratio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | 67,172 | 41,912.50 | 12,665 | 12,270,105.06 | 18,697,928.34 | 0.30218 | 968.82 | 0.65623 |
| 2023 | 118,835 | 82,399.04 | 25,158 | 23,488,354.35 | 35,344,308.08 | 0.30532 | 933.63 | 0.66456 |
| 2024 | 168,133 | 126,014.36 | 39,276 | 38,106,351.28 | 51,037,433.00 | 0.31168 | 970.22 | 0.74664 |

These checks establish basic usability, not full data validity. Remaining checks must cover categorical levels, impossible ages and vehicle values, exposure-zero records, component-to-total reconciliation, claim-count and incurred-loss consistency, missingness across all 47 motor variables, outliers, censoring, inflation, portfolio composition changes, and leakage risks.

### 3.5 Reproduced current outputs

After the reproducibility corrections described in `15_EMPIRICAL_FINDINGS_AND_METHOD_AUDIT.md`, the synthetic engine reproduces the scenario metrics with seed 20260825 and 10,000 worlds:

- 8,037 PASS, 1,958 REPAIR, and 5 REJECT worlds;
- 3,588 traceability failures, one combined-ratio failure, and five structural rejects retained in the Failure Atlas;
- synthetic scenario failure rates from 0.00 percent for BASELINE to 49.88 percent for SEVERE_PLAUSIBLE;
- readiness status `BLOCKED`, with portfolio backtesting and out-of-sample validation missing.

These values describe the behavior of the configured synthetic generator. They are not evidence that the scenario probabilities, dependencies, thresholds, or product parameters reflect a real portfolio.

The external motor experiment calibrates on 2022 to 2023 and projects 2024 with seed 42 and 10,000 simulations. It produces:

| Measure | Predicted mean | Observed 2024 | Relative error | Observed inside model 95 percent interval |
|---|---:|---:|---:|---|
| Claim count | 38,342.38 | 39,276 | -2.38 percent | No |
| Incurred loss | 36,254,608.74 | 38,106,351.28 | -4.86 percent | No |
| Loss ratio | 0.71035 | 0.74664 | Not currently reported by the code | No for the implied interval comparison |

The empirical result is therefore mixed. Central predictions are relatively close in percentage terms, but the observed claim count and incurred loss both fall outside the reported 95 percent predictive intervals. This is evidence of miscalibration or unmodelled temporal change under the present aggregate specification, not successful validation.

The supplied 25 percent joint frequency-and-severity stress claim was also reproduced with seed 42 and 10,000 simulations. The mean simulated claims-to-premium ratio is 1.10991, with a simulated 2.5 to 97.5 percentile interval of 1.09157 to 1.12817. This is a verified scenario response under the current model assumptions. It is not evidence that a 25 percent joint shock is empirically probable or that the loss-ratio response generalizes to another portfolio.

### 3.6 Documentation and verification assets

The repository includes a README, a data-architecture note, a verification report, a design QA report, and a platform audit. They document the intended system and previously reported checks. The current audit independently confirmed the database counts, integrity result, core motor aggregates, and the two ARCCRAFT execution paths. The full platform verification suite was not rerun because it includes compilation that writes generated files and is not necessary for this read-only evidence audit.

## 4. Evidence that is not currently available

The workspace does not contain:

- a manuscript draft, abstract, title page, bibliography, BibTeX file, literature extraction grid, search log, or PRISMA record;
- peer-reviewed papers or verified DOI records supplied by the authors;
- Bohrium exports or any other literature-library export;
- confirmed target journal or conference requirements;
- confirmed author affiliations or correspondence email;
- a genuinely untouched final holdout period;
- an independent second insurance portfolio for external validation;
- individual claim transactions or individual claim severities;
- expense and commission ratios needed for empirical combined-ratio validation;
- an empirically calibrated Togo, Mixx by Yas, or CIMA portfolio;
- actual claims operations, payment traceability, network availability, liquidity, or fraud-pressure outcomes linked to the synthetic state variables;
- observed labels establishing whether ARCCRAFT detected real failures earlier or more accurately than a comparator;
- a prospectively untouched temporal outcome or independent external portfolio;
- enough forecast origins for stable tail calibration, VaR, or Expected Shortfall backtests;
- external labels or implanted ground truth for failure-attribution accuracy;
- a locked environment file containing exact Python package versions;
- original large source files needed to rebuild the database from first principles.

No paper claim should imply that any item in this list exists until it has been supplied or produced and verified.

## 5. Critical methodological risks

### 5.1 The existing 2024 evaluation is not a pristine final holdout

The current code, reports, and user interface already expose the 2024 outcome and its validation errors. Further model design informed by those results would contaminate 2024 as a confirmatory holdout. The paper may report 2024 as retrospective temporal validation, but it must not describe it as untouched after model development.

Confirmatory options, in descending order of strength, are:

1. obtain a later genuinely untouched period;
2. obtain an independent external motor portfolio;
3. freeze the complete analysis before accessing a separately held data partition controlled by another person;
4. if none is possible, use pre-specified rolling-origin or nested resampling and state that the evidence is internal and retrospective.

### 5.2 Severity is a proxy

The source stores incurred amount at policy-year level. The current code derives a claim-weighted distribution of policy-year average severity and recenters a lognormal mean. This is not an individual-claim severity model. Any tail claim based on it must be qualified, and strong severity-tail conclusions require claim-level loss observations.

### 5.3 The procedural and empirical layers are not yet integrated

The synthetic ARCCRAFT engine uses scenario assumptions and synthetic product parameters. The external motor function is a separate aggregate frequency-severity simulation. A publishable benchmark requires a documented mapping from empirical calibration to ARCCRAFT state variables, scenario transitions, dependence assumptions, failure thresholds, and outputs. Without that mapping, the paper can evaluate two components but cannot claim empirical validation of the full architecture.

### 5.4 Failure detection lacks observed ground truth

The Failure Atlas faithfully explains failures defined by the framework's own gates. It does not yet demonstrate detection of externally observed operational or actuarial failures. The paper must distinguish internal rule traceability from empirical detection performance.

### 5.5 Contextual databases may cause scope inflation

FAS, WDI, Findex, GFD, GSMA, and MMPI are substantial but are not automatically relevant to the central benchmark. They should be used only if the literature review identifies a testable mechanism, temporal and geographic alignment is adequate, and a defensible linkage can be constructed. Dataset volume is not evidence of relevance.

## 6. Confirmed decisions and unresolved metadata

Confirmed:

1. The paper is exclusively about ARCCRAFT.
2. The working title is *Procedural Stress Testing of Actuarial Models: Design and Validation of the ARCCRAFT Framework*.
3. The target venue is the Revue Internationale de Management et d'Économie (RIME), subject to final confirmation that this is the intended RIME journal.
4. The paper is experimental and benchmark-oriented.
5. Elia Batako is the author and Manuel Ntumba is the co-author.
6. The literature search will be conducted independently; no Bohrium source package will be supplied.
7. The manuscript language is English.

Unresolved:

1. affiliations for Elia Batako and Manuel Ntumba;
2. the corresponding author and correspondence email;
3. whether an independent portfolio or later untouched period can be supplied;
4. the exact RIME Word-template requirements that are not exposed on the indexed submission page.

No affiliations, deployment status, institutional adoption, or author role will be inferred from the repository.

## 7. Phased work plan

### Phase 0. Confirm scope and governance

Tasks:

- resolve the five remaining metadata and data-access items in Section 6;
- select the paper language and citation convention required by the venue;
- preserve the confirmed exclusion of MAPTA and COMPASS from the paper;
- identify who can hold back confirmatory data, if any;
- create a claim register with one evidence source for each factual or numerical claim.

Deliverable: confirmed research charter and authorship metadata.

Exit criterion: the research question, paper type, venue family, empirical case, and author metadata are unambiguous.

### Phase 1. Literature protocol and evidence map

Tasks:

- formalize the PICO or PECO question;
- publish a reproducible search protocol covering years, languages, databases, source types, inclusion criteria, exclusion criteria, Boolean strings, screening, extraction, and synthesis;
- search academic databases, actuarial and insurance sources, regulatory literature, and citation networks;
- cover frequency-severity models, stochastic simulation, insurance stress testing, synthetic portfolios, uncertainty, random-number governance, validation, tail risk, model risk, and benchmarking;
- create the source extraction grid with DOI and link verification;
- maintain exact record counts for identification, deduplication, abstract screening, full-text assessment, inclusion, and exclusion reasons;
- identify the three to five closest methods and test whether the claimed contribution is absent or only differently named.

Deliverables:

- `01_SEARCH_PROTOCOL.md`;
- `02_LITERATURE_EXTRACTION.csv`;
- `03_SCREENING_LOG.md`;
- `04_NOVELTY_AND_EVIDENCE_GAPS.md`;
- verified reference library.

Exit criterion: the novelty statement is framed as a testable gap, not as the existence of ARCCRAFT itself.

### Phase 2. Paper architecture and literature review

Tasks:

- confirm an approximately 30-page allocation with 18 to 22 pages of core text;
- design the fixed sections: Literature Review, Research Methodology, Results and Findings, Conclusion and Recommendations;
- synthesize approximately 35 to 50 highly relevant sources directly in the literature review;
- derive exact empirical tests from the methodological disagreements and evidence gaps;
- define every necessary table and figure by analytical purpose and data source.

Provisional page allocation:

| Component | Pages |
|---|---:|
| Title, abstract, contents, abbreviations | 2 to 3 |
| Literature Review | 5 to 6 |
| Research Methodology | 6 to 7 |
| Results and Findings | 5 to 6 |
| Conclusion, recommendations, limitations | 2 to 3 |
| References, tables, and figure space | balance within 30 |

Deliverable: literature-review draft and validated paper outline.

Exit criterion: the review ends with explicit hypotheses, comparator requirements, validation metrics, and evidence needs.

### Phase 3. Mandatory post-literature data gate

Tasks:

- classify identified datasets as required core data, required robustness or external-validation data, and optional enrichment data;
- provide verified public access points and exact variables, years, units, and experimental uses;
- compare those requirements with the current workspace inventory;
- request only missing datasets that the literature shows are necessary;
- redesign claims when a critical dataset cannot be acquired.

Expected minimum request, subject to literature confirmation:

- the original motor CSV corresponding to the recorded SHA-256, or a controlled verification that the database is a complete faithful copy;
- an independent motor portfolio or untouched later period;
- claim-level severity data if individual-loss tail calibration is claimed;
- expense and commission fields if empirical combined-ratio conclusions are claimed;
- externally observed failure or operational-quality labels if empirical failure-detection claims are retained.

Deliverable: three data-request tables in the required download-link schema.

Mandatory stop: no confirmatory estimation or Results drafting until required core data are present and validated.

### Phase 4. Data validation and frozen pre-analysis plan

Tasks:

- validate schema, types, units, missingness, duplicates, impossible values, exposure periods, reconciliation, temporal coverage, selection effects, censoring, and leakage;
- document portfolio composition by year and investigate the 2024 frequency and loss-ratio shift;
- freeze the role of each period or fold before final evaluation;
- define model transformations, hyperparameter selection, scenario calibration, threshold selection, seed policy, number of simulations, computational budget, and exclusion or repair rules;
- register all deviations made after viewing evaluation data as post-hoc.

Recommended temporal design with current data:

- use 2022 for initial fitting and 2023 for validation or rolling-origin evaluation;
- treat 2024 as an already observed retrospective test, not a pristine holdout;
- reserve a new portfolio, later period, or controlled partition for confirmatory evaluation if available.

Deliverables:

- `05_data_quality_report.md`;
- `06_preanalysis_plan.md`;
- machine-readable experiment configuration;
- version and hash register.

Exit criterion: one person can reproduce the data partitions and all planned experiments without consulting undocumented decisions.

### Phase 5. Comparator and ARCCRAFT implementation

The final comparator set must follow the literature, but the minimum provisional design is:

1. Aggregate frequency-severity baseline. Reproduce and audit the existing compound-Poisson/lognormal model.
2. Policy-level actuarial baseline. Fit a transparent frequency model and a defensible positive-loss severity model using available predictors, with exposure handled explicitly.
3. Conventional stochastic benchmark. Simulate from the calibrated actuarial components without the procedural validator, scenario grammar, failure attribution, or reverse-stress layer.
4. Full ARCCRAFT. Map empirical calibration, state transitions, dependence, scenario classes, validation rules, failure criteria, and seed governance explicitly.

The baselines must not be intentionally weakened. Hyperparameters and computational budgets must be comparable or their differences disclosed.

Required ablations, where technically identifiable:

- remove structural PASS, REPAIR, and REJECT validation;
- remove named substreams while preserving total simulation budget;
- remove or simplify dependence and multi-period state transitions;
- replace scenario classes with an unconditional simulation;
- remove failure attribution and reverse-stress diagnostics when measuring diagnostic utility;
- separate components that affect predictive performance from components that affect traceability only.

Deliverables:

- reproducible experiment scripts;
- configuration files;
- comparator specifications;
- unit and invariance tests;
- runtime and environment records.

Exit criterion: all methods consume compatible data, use the frozen partitions, and produce a common evaluation schema.

### Phase 6. Evaluation and falsification

Primary metric families, subject to pre-analysis confirmation:

- central accuracy: count deviance, absolute or squared error, and loss-ratio error;
- distributional calibration: log score or another proper scoring rule, CRPS when justified, probability integral transform diagnostics, and predictive-interval coverage;
- tail behavior: high-quantile error, exceedance counts, VaR and Expected Shortfall backtests where the data support them;
- robustness: process noise, observation noise, parameter perturbation, distribution shift, and scenario-intensity response;
- failure analysis: minimum-failure perturbation, failure-threshold sensitivity, and agreement with externally observed failure labels when available;
- reproducibility: repeated-seed variability, deterministic replay, and named-substream invariance;
- efficiency: wall-clock time, memory, and simulation budget;
- ablation: metric change after removal of each major component.

Every comparison will report uncertainty and dimension-specific trade-offs. No single composite superiority score will be introduced after seeing results.

Deliverables:

- locked results tables;
- figure source tables;
- figure specifications and generated figures;
- negative and null results log;
- post-hoc analysis log.

Exit criterion: every Results statement traces to executed code, a saved configuration, an evaluation dataset, and a table or figure value.

### Phase 7. Manuscript completion

Draft in this order:

1. Literature Review;
2. Research Methodology with the actuarial baseline, ARCCRAFT formalization, and validation design;
3. Results and Findings with comparators reported before interpretation of ARCCRAFT;
4. Conclusion and Recommendations;
5. abstract, title page, abbreviations, and final references after the body stabilizes.

The manuscript will distinguish:

- established literature from the authors' proposed framework;
- calibrated parameters from externally sourced values and scenario assumptions;
- synthetic behavior from empirical evidence;
- retrospective evaluation from untouched confirmation;
- predictive performance from explanatory traceability;
- internal validity from external transferability.

Deliverable: one complete Markdown manuscript, produced as `31_ARCCRAFT_FULL_MANUSCRIPT.md`.

Exit criterion: no claim is stronger than its evidence and the complete paper stays within the page budget.

### Phase 8. Final audit and reference consolidation

Tasks:

- audit structure, density, abstract alignment, methods, figures, tables, citations, language, paper-type consistency, information integrity, empirical defensibility, and reproducibility;
- verify no leakage, disadvantaged comparator, hidden failed validation, unstable seed result, or unsupported tail claim;
- verify each numerical or symbolic result against executed code;
- consolidate approximately 60 to 90 relevant verified references, adjusted to venue rules;
- ensure every citation has a reference and every reference is cited.

Deliverables:

- `07_final_audit_log.md`;
- final reference list;
- final single-file Markdown manuscript.

Exit criterion: all critical audit findings are resolved or disclosed as limitations.

## 8. Provisional figure and table plan

The final set must be justified by the literature and results. A compact working plan is:

| Item | Purpose | Current status |
|---|---|---|
| Table 1. Evidence and dataset provenance | Separate empirical, documentary, contextual, and synthetic inputs | Available for drafting |
| Figure 1. ARCCRAFT experimental pipeline | Show calibration, world generation, validation, simulation, failure attribution, and evaluation | Requires formal method freeze |
| Table 2. Comparator definitions and assumptions | Demonstrate fair benchmark design | Implemented for B0-B2; full synthetic grammar remains a separate evidence layer |
| Figure 2. Temporal portfolio composition and outcomes | Diagnose 2022 to 2024 shifts | Completed |
| Table 3. Predictive and calibration metrics | Compare matched empirical baselines | Completed for two retrospective temporal origins |
| Figure 3. Predictive distributions versus observed outcomes | Show calibration and interval failures | Partially available for current aggregate baseline |
| Figure 4. Stress response and minimum-failure conditions | Evaluate stress sensitivity and reverse stress | Synthetic result available; empirical calibration pending |
| Table 4. Robustness, seed sensitivity, and ablations | Isolate the value of architectural components | Completed for five configurations and three seeds |
| Figure 5. Failure rate and computational cost | Expose procedural and runtime trade-offs | Completed |

## 9. Claim policy for the current evidence

### Claims that can be made now

- The repository contains an executable synthetic procedural stress-testing prototype with deterministic seed control, structural world validation, failure attribution, and reverse-stress search.
- The included database contains a three-year external motor portfolio with verified annual aggregates and no duplicates on the inspected policy-year key.
- The current aggregate motor experiment underpredicts 2024 claims and incurred loss, and both observed outcomes fall outside its reported 95 percent predictive intervals.
- The current code explicitly marks real-world robustness readiness as blocked.

### Claims that cannot be made now

- ARCCRAFT is an established actuarial theory or accepted industry standard.
- ARCCRAFT is deployed, adopted, or used in production.
- ARCCRAFT is validated for Togo, Mixx by Yas, CIMA, or any named insurer.
- ARCCRAFT generally outperforms conventional actuarial or Monte Carlo baselines.
- The Failure Atlas detects real operational failures.
- The synthetic scenario probabilities or thresholds are empirically calibrated.
- The motor severity model represents individual claim severity.
- The 2024 result is an untouched final holdout.

## 10. Immediate next action

The retrospective benchmark and scientific draft are complete. Submission preparation now depends on author-supplied metadata and genuinely new evidence rather than additional tuning to the inspected 2022-2024 portfolio. Required next inputs are: author affiliations and corresponding-author details; confirmation of the exact RIME template; and, for confirmatory claims, an untouched later year or independent portfolio. The manuscript language is fixed as English. Claim-level losses and operational failure labels remain necessary for individual-severity tail validation and failure-attribution testing. The 2024 period must not be reused as a confirmatory holdout.
