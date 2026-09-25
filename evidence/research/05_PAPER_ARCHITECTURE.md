# ARCCRAFT paper architecture for RIME

Version: 1.0  
Date: 23 September 2026  
Target journal: Revue Internationale de Management et d'Économie  
Citation system: APA 7  
Article structure: IMRaD, with a distinct literature-review section inside the Introduction-to-Methods progression

## 1. Title and positioning

**Working title**

Procedural Stress Testing of Actuarial Models: Design and Validation of the ARCCRAFT Framework

**Safer title if independent validation remains unavailable**

Procedural Stress Testing of Actuarial Models: Design and Preliminary Evaluation of the ARCCRAFT Framework

The second title is mandatory if the final evidence remains limited to the current synthetic experiment and retrospective 2024 motor-portfolio check.

## 2. Central research question

Does an integrated procedural architecture combining explicit multi-period state transitions, separated random streams, structural validation, deterministic replay, and failure attribution improve the reproducibility, diagnostic value, failure detection, or predictive evaluation of actuarial stress tests relative to transparent conventional simulation baselines, and at what computational and model-risk cost?

## 3. Article-level argument

The paper will develop one continuous argument:

1. Conventional actuarial stress tests and frequency-severity simulations provide established loss projections and scenario analysis, but their implementation can leave scenario sequencing, internal consistency, reproducible replay, and failure attribution weakly integrated.
2. Prior research already supplies important pieces of this problem, including severe-but-plausible scenario selection, reverse sensitivity testing, dynamic loss stress, synthetic claims simulators, artificial insurers, random substreams, and simulation validation.
3. ARCCRAFT is therefore proposed as an integration architecture rather than a replacement for these theories.
4. Its contribution must be evaluated against matched baselines and ablations, not inferred from the existence of the software.
5. The evidence must separately assess software verification, empirical predictive validity, scenario plausibility, diagnostic usefulness, and computational cost.
6. The conclusion will report which dimensions are supported, unsupported, or falsified.

## 4. Target length

| Section | Target words | Purpose |
|---|---:|---|
| Title, abstract and keywords | 250-300 | State the question, design, main quantified results and limitations |
| 1. Introduction | 750-900 | Establish the decision problem, gap, research question and contributions |
| 2. Literature Review | 2,200-2,700 | Synthesize debates and derive the evaluation design |
| 3. Methods | 2,500-3,000 | Define ARCCRAFT, data, comparators, experiments and metrics |
| 4. Results | 1,800-2,300 | Report data audit, benchmark, calibration, stress, ablation and cost findings |
| 5. Discussion | 900-1,200 | Interpret evidence, relate it to literature and explain management implications |
| 6. Conclusion | 450-650 | Answer the research question without overstating validation |
| References and appendices | As required | APA 7 references and reproducibility material |

Target core manuscript length: approximately 9,000-10,500 words before references and appendices.

## 5. Detailed IMRaD outline

### Abstract

Use a structured logical sequence in one paragraph:

- problem and gap;
- objective and exact research question;
- data and experimental design;
- principal numerical findings;
- calibration failure or limitation;
- bounded contribution and implication.

Do not state that ARCCRAFT is validated unless all pre-specified validation gates pass. The current abstract must say “preliminary evidence” or “preliminary evaluation.”

Keywords: actuarial stress testing; procedural simulation; non-life insurance; model risk; reproducibility; reverse stress testing; predictive calibration.

### 1. Introduction

#### 1.1 Decision problem

Explain why insurers and decision-makers need more than an expected-loss estimate: they need to understand how interacting conditions unfold, when thresholds are crossed, which assumptions cause vulnerability, and whether a critical outcome can be reproduced.

#### 1.2 Scientific problem

Separate five properties that are often conflated:

- stochastic loss projection;
- scenario severity and plausibility;
- software and experiment reproducibility;
- predictive calibration;
- diagnostic attribution.

#### 1.3 Research gap

State that the literature contains mature methods for each component, but the review did not identify a directly equivalent non-life architecture that combines all five in a versioned, seed-addressable workflow and evaluates their joint value through matched comparators and ablations.

#### 1.4 Research question and hypotheses

Present H1-H6 from `04_NOVELTY_AND_EVIDENCE_GAPS.md` in condensed form.

#### 1.5 Contributions

Claim only contributions demonstrated in the final experiments:

1. a formal specification of procedural actuarial worlds;
2. an implementation with separated stochastic streams and replay semantics;
3. a structural validation protocol with explicit accept, repair and reject decisions;
4. a failure-attribution representation linking seeds, states, variables, metrics and thresholds;
5. a matched benchmark and ablation study;
6. an external temporal evaluation with explicit calibration limits.

#### 1.6 Paper organization

One concise paragraph.

### 2. Literature Review

#### 2.1 Actuarial frequency-severity and longitudinal loss models

Establish the collective-loss baseline, the conventional conditional-independence assumption, evidence for frequency-severity dependence, and the relevance of longitudinal models.

#### 2.2 Stress-scenario design and severe-plausible trade-offs

Compare predefined shocks, systematic scenario selection, entropic plausibility, empirical-likelihood approaches and supervisory stress principles.

#### 2.3 Reverse stress testing, dynamic loss models and sensitivity

Explain how reverse methods locate conditions associated with failure and how this differs from forward stress testing and ordinary sensitivity analysis.

#### 2.4 Synthetic insurance environments and open benchmarks

Compare SynthETIC, SPLICE, the Individual Claims History Simulation Machine and openIRM with ARCCRAFT's proposed scope.

#### 2.5 Reproducibility, model validation and uncertainty

Separate deterministic replay from validation; distinguish aleatory uncertainty, parameter uncertainty, model discrepancy and distribution shift.

#### 2.6 Evaluation criteria and unresolved gap

Derive the need for proper scoring, coverage, tail diagnostics, fault-injection ground truth, ablations and cost reporting. End with the bounded novelty statement.

### 3. Methods

#### 3.1 Study design and pre-specification

- experimental and benchmark study;
- confirmatory versus exploratory analyses;
- temporal evaluation policy;
- seed-registration policy;
- no recalibration on evaluation outcomes;
- treatment of the already-inspected 2024 period as retrospective evidence.

#### 3.2 ARCCRAFT formal definition

Define a world as a versioned tuple containing:

- initial state;
- time index and horizon;
- transition functions;
- dependency graph or conditional rules;
- admissible bounds and invariants;
- event mechanisms;
- stochastic-stream allocation;
- validation and repair policy;
- output metrics and failure predicates.

Every symbol must map to a field or function in the implementation. Features absent from the repository must not appear in the formal definition as implemented features.

#### 3.3 Reproducibility model

Document:

- root seed and derivation of component seeds;
- PCG64 bit generator and library version;
- world, claim and behavioural streams;
- grammar/configuration version;
- code commit and environment lock;
- exact versus tolerance-based replay contract.

#### 3.4 Structural validator

Define accept, repair and reject as mutually exclusive outcomes. For each repair rule, specify:

- violated invariant;
- transformation applied;
- whether the repair preserves marginal or joint target distributions;
- audit record;
- downstream inclusion rule.

#### 3.5 Failure Atlas

Define a Failure Atlas record as a mapping from a registered run and seed to:

- world trajectory;
- first failure time;
- failed predicate;
- relevant variables and transitions;
- output metrics;
- validator history;
- reproduction metadata.

Do not call a variable “causal” unless recovery against implanted ground truth or a causal identification design supports that term. Use “attributed,” “associated,” or “ranked as influential” otherwise.

#### 3.6 Data

Report the local motor portfolio:

- 354,140 policy-year observations;
- 185,678 distinct insureds;
- years 2022-2024;
- exposure, claims, incurred loss and premium definitions;
- checks for duplicates, missingness and negative values;
- provenance limitations and absent original raw file;
- policy-year average-cost limitation.

#### 3.7 Comparators

Implement B0-B4 from `04_NOVELTY_AND_EVIDENCE_GAPS.md`. If a comparator cannot be estimated, state the data reason and narrow the corresponding research claim.

#### 3.8 Experimental regimes

- baseline;
- alternative;
- adverse;
- severe-plausible;
- exploratory;
- reverse stress.

Regime labels must be associated with quantitative rules. “Severe plausible” requires a stated plausibility criterion rather than a subjective label.

#### 3.9 Ablations

Run the six ablations defined in `04_NOVELTY_AND_EVIDENCE_GAPS.md` under matched budgets.

#### 3.10 Outcomes and statistical analysis

Pre-specify:

- point errors;
- proper scores;
- interval coverage and width;
- randomized PIT or discrete calibration;
- VaR/ES diagnostics where sample size permits;
- failure detection and attribution metrics;
- bootstrap or resampling uncertainty;
- multiple-comparison handling if many regimes are compared;
- runtime, memory and effective accepted sample size.

### 4. Results

Use a fixed reporting order so interpretation does not select favourable outputs:

#### 4.1 Data integrity and descriptive profile

#### 4.2 Reproducibility and validator behaviour

#### 4.3 Baseline and comparator performance

#### 4.4 Temporal predictive evaluation

#### 4.5 Stress-response surfaces and failure regions

#### 4.6 Failure-detection and attribution experiment

#### 4.7 Ablations and computational cost

#### 4.8 Robustness and negative findings

The current 2024 exceedance of the 97.5% predictive quantile belongs in Section 4.4 and must be visible in the abstract and discussion.

### 5. Discussion

#### 5.1 Principal findings

Answer each hypothesis separately.

#### 5.2 Relation to prior methods

Explain whether ARCCRAFT adds integration, performance, diagnostic value, reproducibility, or only implementation convenience relative to the closest literature.

#### 5.3 Management and governance implications

Discuss how replayable failure records could support model challenge, assumption governance, contingency planning and communication between actuaries and decision-makers. These are implications conditioned on the evidence, not evidence of adoption.

#### 5.4 Limitations

Include data provenance, already-inspected holdout, sample-period length, external-validity limits, repair-induced distribution changes, proxy severity, benchmark completeness and absence of operational deployment evidence.

#### 5.5 Research agenda

Prioritize independent portfolio validation, later periods, richer claim-level severity, formal plausibility constraints, calibrated reverse search and preregistered analyst studies.

### 6. Conclusion

Use four elements:

1. direct answer to the research question;
2. supported contribution;
3. strongest falsification or unresolved limitation;
4. bounded practical implication.

Avoid introducing new results or claiming general industry readiness.

## 6. Planned tables

| No. | Title | Evidence purpose |
|---:|---|---|
| 1 | Comparison of ARCCRAFT with closest actuarial and stress-testing methods | Establish bounded novelty |
| 2 | Motor-portfolio variables, provenance and quality checks | Establish data fitness and limitations |
| 3 | Formal ARCCRAFT components and implementation mapping | Demonstrate that definitions correspond to code |
| 4 | Comparator, ablation and simulation-budget specification | Establish fairness and reproducibility |
| 5 | Annual portfolio aggregates for 2022-2024 | Describe calibration and evaluation periods |
| 6 | Point and probabilistic predictive performance | Compare ARCCRAFT and baselines |
| 7 | Validator outcomes and distributional consequences | Test accept/repair/reject effects |
| 8 | Stress regimes, failure rates and first-passage metrics | Quantify vulnerability regions |
| 9 | Fault-injection detection and attribution performance | Validate Failure Atlas utility |
| 10 | Runtime, memory and replay verification | Report computational trade-offs |

## 7. Planned figures

1. ARCCRAFT architecture and evidence boundaries.
2. Temporal data split, calibration and evaluation workflow.
3. Predictive distributions with observed 2024 outcomes.
4. Calibration and proper-score diagnostics across evaluation folds.
5. Frequency-severity stress surface with failure boundary.
6. Example replayed trajectory from baseline to first failure.
7. Failure Atlas attribution stability across seeds or resamples.
8. Ablation performance-cost frontier.

Figures 4, 6, 7 and 8 require new experiments and must not be fabricated from the current dashboard.

## 8. RIME production requirements

- A4 portrait, approximately 2.5 cm margins, based on the official template structure audit.
- French and English titles are expected by the template.
- French `Résumé` and English `Abstract` fields are present.
- French and English keyword fields are present.
- The template requests author name, role, institution, university, laboratory, country and email for each author.
- Main headings, captions and source lines are represented at 12 pt in the template; title placeholders are 14 pt in the file although their text says Times New Roman 16. This internal inconsistency must be resolved with the journal before final formatting.
- The template uses anchored full-page branding images on each apparent page. It must remain the design authority when the manuscript DOCX is produced.
- The journal submission page requires IMRaD, APA 7, anonymization, checked references, and numbered/labeled tables and figures.
- A separate anonymized review copy and identified title-page copy should be prepared because the review process is double-blind.

The downloaded original template is preserved as `RIME_TEMPLATE_ORIGINAL.docx` with SHA-256 `76767838C55547A4F695C0697899477A3C230C0A42E779AFD771AE2F0E5F74EF`.

