# ARCCRAFT novelty assessment and evidence gaps

Date: 23 September 2026  
Purpose: convert the literature review and repository audit into a defensible contribution claim and a falsifiable experimental design.

## 1. What the literature already establishes

The paper must not claim novelty for any of the following in isolation:

- actuarial frequency-severity and compound-loss simulation;
- dependence between claim frequency and severity;
- multi-period or longitudinal insurance-claims modelling;
- severe-but-plausible scenario construction;
- systematic, entropy-constrained, or empirical-likelihood stress scenarios;
- reverse stress testing or reverse sensitivity testing;
- dynamic stress of compound loss processes;
- synthetic individual-claim simulators or artificial insurers;
- Monte Carlo seeds, random streams, substreams, or deterministic replay as general computational practices;
- model verification, validation, calibration, sensitivity analysis, proper scoring, interval coverage, VaR/ES, or exceedance backtesting;
- model-risk governance, documentation, benchmarking, and limitation disclosure.

These are established domains represented in `02_LITERATURE_EXTRACTION.csv`.

## 2. Closest prior systems

| Prior work | Overlap with ARCCRAFT | Remaining distinction that must be demonstrated |
|---|---|---|
| SynthETIC | Controllable, open, synthetic insurance claim histories with dependencies | ARCCRAFT proposes multi-risk worlds, stress regimes, structural world validation, seed-addressable failure diagnosis, and external model testing rather than a claims-development simulator alone |
| SPLICE | Procedural paid/incurred claim histories and dependencies | ARCCRAFT targets adverse environment generation and system failure conditions, not incurred-loss development only |
| Individual Claims History Simulation Machine | Synthetic granular portfolios and longitudinal claim cash flows | ARCCRAFT claims explicit scenario grammar, validator decisions, stress taxonomy, replay and failure attribution |
| openIRM | Open artificial insurer and reproducible benchmark platform | ARCCRAFT is oriented to non-life procedural stress environments and failure discovery rather than a life-insurance nested-SCR benchmark |
| Reverse sensitivity testing | Identifies input changes associated with stressed outputs in an insurance portfolio | ARCCRAFT proposes generation and validation of full time-dependent worlds plus persistent seed-level diagnostic records |
| Stressing Dynamic Loss Models | Dynamic reverse stress for compound loss processes | ARCCRAFT is a software architecture with discrete world states, transition/event mechanisms, validation gates and replay; it does not yet possess comparable formal theory |
| Systematic/entropic scenario selection | Internal consistency and controlled severity/plausibility | ARCCRAFT's validator and grammar must be shown to preserve or improve plausibility without silently changing the target stress distribution |

## 3. Defensible provisional contribution

Subject to successful implementation and testing, the manuscript may propose ARCCRAFT as:

> a reproducible software architecture for procedural, multi-period actuarial stress testing that integrates versioned world specifications, explicit state transitions and dependencies, separated random streams, structural accept/repair/reject validation, exact seed-level replay, and failure attribution within one auditable workflow.

This is an **architectural and empirical contribution claim**, not an assertion that ARCCRAFT is an established actuarial theory or validated industry standard.

The stronger phrase “validated framework” is permissible only if the final study supplies independent empirical validation, comparator results, ablations, uncertainty analysis, and failure-detection ground truth. With the current evidence, the appropriate phrase is “designed and preliminarily evaluated framework.”

## 4. Current evidence status

| Claim dimension | Evidence currently available | Status |
|---|---|---|
| Software execution | Working Python/TypeScript repository and reproducible seeded runs | Supported locally, pending packaged tests and environment lock |
| Structural validation | Accept/repair/reject outcomes are produced by the engine | Implemented, but repair correctness and distributional side effects are unvalidated |
| Seed replay | Seeded synthetic and motor experiments can be rerun | Demonstrated locally, but bitwise/cross-platform guarantees are untested |
| External predictive accuracy | 2024 motor aggregates compared with simulations calibrated on 2022-2023 | Preliminary retrospective temporal check only |
| Predictive calibration | Observed 2024 claim count, cost and loss ratio exceed the reported 97.5% predictive quantiles | Failed for the current evaluated tail criterion |
| Stress response | Joint +25% frequency and severity stress produces mean loss ratio about 1.11 | Demonstrates response to a configured shock, not realism, calibration, or superior detection |
| Failure Atlas | Seed-level traceability and a combined-ratio threshold are recorded | Internal rule execution only; no external failure ground truth or diagnostic-utility test |
| Comparative advantage | No matched conventional Monte Carlo or frequency-severity comparison has been run | Unsupported |
| Generalisability | One motor portfolio and one already-inspected 2024 period | Unsupported |

## 5. Mandatory comparators

All methods must receive matched calibration data, exposures, simulation budgets, random-seed sets where applicable, output definitions, and evaluation metrics.

1. **B0: deterministic expected-loss projection.** Historical exposure-weighted frequency multiplied by historical average severity.
2. **B1: conventional independent frequency-severity Monte Carlo.** Poisson or negative-binomial frequency and a justified positive severity distribution; parameter uncertainty reported separately.
3. **B2: dependent or longitudinal frequency-severity model.** A transparent implementation grounded in `L013`-`L018`, chosen according to available claim granularity.
4. **B3: static scenario stress.** Predefined marginal shocks without procedural state transitions or a structural validator.
5. **B4: reverse-sensitivity or systematic scenario method.** A method grounded in `L005`, `L007`, `L009`, or `L011`, subject to feasible data and computation.
6. **A: full ARCCRAFT.** The complete architecture under test.

If transaction-level claim severity is unavailable, the paper must say that B1/B2 use policy-year aggregate incurred cost or average-cost proxies. It must not label those proxies as individual claim severity.

## 6. Required ablations

| Ablation | Question answered | Primary outcomes |
|---|---|---|
| A minus structural validator | Does validation improve consistency or merely censor/reshape the scenario distribution? | invalid-world rate, output-distribution shift, failure yield, runtime |
| A minus repair; reject only | Are repairs scientifically defensible compared with transparent rejection? | acceptance rate, bias, tail movement, auditability |
| A with one shared RNG stream | Do separated streams materially improve controlled replay and component isolation? | exact replay, counterfactual component stability, seed sensitivity |
| A with static one-period states | Do procedural transitions add detectable information beyond static shocks? | failure discovery, time-to-failure, predictive scores, runtime |
| A without dependency rules | Are claimed effects driven by explicit inter-variable dependence? | tail risk, failure regions, calibration, rank changes |
| A without Failure Atlas output | Does attribution improve human diagnosis rather than just record more data? | blinded analyst accuracy, time-to-cause, inter-rater agreement |

The last ablation requires a small, pre-specified diagnostic user study or an objective ground-truth attribution task. Anecdotal screenshots are insufficient.

## 7. Falsifiable hypotheses

- **H1 — predictive distribution:** ARCCRAFT improves at least one pre-specified proper score without materially worsening interval coverage relative to B1 and B2 on untouched evaluation data.
- **H2 — tail calibration:** ARCCRAFT's nominal tail probabilities are compatible with observed exceedance frequencies across repeated evaluation periods or folds.
- **H3 — failure discovery:** Under blinded synthetic fault injection, ARCCRAFT identifies a higher proportion of true failure configurations at a fixed false-discovery rate than B3.
- **H4 — diagnostic attribution:** Failure Atlas rankings recover the implanted causal variables or mechanisms more accurately than raw-output ranking or variance-only sensitivity.
- **H5 — reproducibility:** Repeating a registered configuration, software version and seed reproduces declared outputs within a pre-specified exact or numerical tolerance.
- **H6 — value for cost:** Any gain in H1-H4 remains after reporting runtime, memory, rejected worlds, repaired worlds, and effective accepted-sample size.

Failure to support one hypothesis must be reported; it must not be reinterpreted post hoc as evidence of a different benefit.

## 8. Pre-specified outcomes

### Central and distributional prediction

- observed and predicted claim count, incurred cost, premium and loss ratio;
- signed percentage error and absolute percentage error, with zero-safe definitions;
- ranked probability score or log score for counts where the full predictive mass is available;
- CRPS or an appropriate proper score for continuous aggregate cost;
- 50%, 80%, 90% and 95% predictive-interval coverage and width;
- randomized PIT or an equivalent discrete calibration diagnostic for counts.

### Tail and failure behaviour

- exceedances at pre-specified VaR levels;
- Expected Shortfall where sample size supports it;
- probability and first passage time for pre-defined failure thresholds;
- precision, recall, false-discovery rate and detection delay under implanted failures;
- stability of failure rankings across seeds and resamples.

### Computation and reproducibility

- wall-clock time, peak memory and simulations per second;
- accepted, repaired and rejected worlds;
- effective sample size after validation/filtering;
- exact configuration hash, code commit, dependency lock, PRNG/bit-generator name and version;
- equality or declared tolerance of replayed outputs.

## 9. Immediate blockers to a strong validation claim

1. The 2024 outcome has already been used and reported, so it is not a pristine untouched holdout.
2. Only one external portfolio and three annual periods are currently available.
3. The observed 2024 count, incurred cost and loss ratio lie above the current 97.5% predictive quantiles.
4. The synthetic world engine and empirical motor model are not yet formally connected in one end-to-end experiment.
5. Failure Atlas labels are generated by internal thresholds, not independent observed failure truth.
6. No matched comparator or ablation result exists.
7. The effect of validator repair/rejection on the target scenario distribution is unknown.
8. Individual claim-level severity is unavailable in the normalized policy-year data currently inspected.

## 10. Minimum additional evidence before manuscript drafting

The Methods can be drafted from the code and protocol now, but Results and Conclusion should wait until at least the following exist:

- one independent portfolio, later untouched period, or rigorously pre-specified rolling-origin evaluation;
- runnable B0-B3 comparators and the six core ablations;
- full predictive outputs sufficient for proper scoring and calibration plots;
- synthetic fault-injection truth for failure-detection and attribution evaluation;
- a reproducible experiment manifest with code, data and environment hashes;
- an explicit rule for validator repair and a sensitivity analysis of its distributional consequences.

