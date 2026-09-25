# ARCCRAFT empirical findings and method audit

Status date: 23 September 2026  
Authors: Elia Batako and Manuel Ntumba  
Evidence status: retrospective and exploratory; not confirmatory validation

## 1. Executed study package

The empirical package is recorded in `08_EMPIRICAL_BENCHMARK.ipynb` and its rendered HTML counterpart. The notebook executed all nine code cells without an exception and exported the source tables used by the figures. The evaluated repository base commit is `b3df670`; the research run also includes the reproducibility corrections documented in Section 5 below.

The principal settings are:

- motor forecast seed: 42;
- motor forecast replications: 50,000;
- synthetic procedural audit seed: 20260825;
- synthetic procedural audit size: 3,000 worlds for the notebook sensitivity comparisons;
- supplementary canonical synthetic rerun: 10,000 worlds;
- stochastic generator: PCG64 with named spawned substreams;
- motor calibration/evaluation origins: 2022 to 2023 and 2022-2023 to 2024.

## 2. External motor results

### 2.1 Rolling-origin evaluation

| Calibration | Evaluation | Claim-count error | Count inside 95% interval | Incurred-loss error | Incurred inside 95% interval |
|---|---:|---:|---|---:|---|
| 2022 | 2023 | -1.03% | Yes | +2.70% | No |
| 2022-2023 | 2024 | -2.38% | No | -4.88% | No |

Only two origins exist. The descriptive count-interval coverage is therefore one of two and incurred-loss coverage is zero of two. These proportions must not be presented as stable coverage estimates. The result is nevertheless sufficient to reject a claim of complete predictive calibration for the current aggregate specification.

### 2.2 2024 point benchmarks

| Method | Claim-count error | Incurred-loss error |
|---|---:|---:|
| ARCCRAFT pooled Poisson-lognormal | -2.38% | -4.88% |
| Last-year exposure-scaled | -2.04% | -5.73% |
| Pooled deterministic mean | -2.38% | -4.88% |
| Two-point log trend, exploratory | -1.02% | -8.21% |

The stochastic model's central forecast is essentially the pooled deterministic mean. It is not the best count forecast in this small comparison, while it has a smaller incurred-loss error than the last-year and two-point trend references. This mixed ranking does not support a general superiority claim. The stochastic contribution is its predictive distribution and stress propagation, not an observed improvement in the central estimate.

### 2.3 Stress response

The 5 by 5 frequency-severity grid is monotone under the implemented multiplicative specification. At a joint 1.25 frequency and 1.25 severity multiplier, the simulated mean loss ratio is 1.10985, with 2.5% and 97.5% quantiles of 1.09131 and 1.12822. This confirms the configured response but does not establish that this joint shock is historically calibrated or severe-but-plausible.

## 3. Synthetic procedural results

In the 3,000-world notebook run at seed 20260825, the validator produced 2,397 PASS and 603 REPAIR worlds, with no REJECT. Among accepted worlds, the coded failure rate was 34.57%. All 1,037 atlas failures were traceability failures; none crossed the combined-ratio gate. The scenario-class failure rates ranged from 0% for BASELINE to 48.60% for SEVERE_PLAUSIBLE.

The canonical 10,000-world rerun produced:

- 8,037 PASS, 1,958 REPAIR, and 5 REJECT worlds;
- 3,588 traceability failures;
- one combined-ratio failure;
- five structural rejections retained in the Failure Atlas summary;
- a reverse-stress result at standardized search distance 1.0123, failing the traceability gate with traceability 0.9321 and combined ratio 0.4017.

The predominance of traceability failures and near absence of combined-ratio failures show that the current synthetic result is driven mainly by the operational gate. This is an informative property of the configured experiment, but it also means that the present synthetic product and grammar do not provide a balanced empirical test of actuarial and operational failure modes.

## 4. Reproducibility and validator checks

The following tests pass in the inspected local environment:

1. repeated same-seed simulations produce identical labels, failure gates, combined ratios, and traceability values, including exact floating-point equality with rejected-world `NaN` values treated consistently;
2. trajectory simulation no longer mutates the validated input arrays;
3. the reverse-stress result is unchanged after unrelated random streams have been consumed;
4. every Failure Atlas row records the seed actually executed and stable named-substream identifiers;
5. structural rejects are retained in the Failure Atlas summary;
6. the full backend verification suite reports 27 of 27 checks passed.

Changing the master seed from 20260825 to 20260826 changed the accepted-world failure rate from 34.57% to 37.01% in 3,000-world runs. This difference describes Monte Carlo and world-composition sensitivity under one alternate seed; it is not a confidence interval over the generator design.

Treating every REPAIR as a strict rejection reduced the accepted population from 3,000 to 2,397 and changed the accepted-world failure rate from 34.57% to 35.21%. Because this changes the selected population, it is a validator-sensitivity diagnostic rather than causal evidence that repair improves or worsens scenario quality.

## 5. Corrective changes required before the audit

Four implementation defects were corrected because they directly affected paper claims:

- `simuler_trajectoires` now works on copies of validated state arrays instead of mutating the validation object;
- reverse stress now derives a dedicated deterministic seed domain from the master seed and no longer depends on prior random-number consumption;
- Failure Atlas construction receives and records the executed master seed and descriptive child-stream spawn keys;
- rejected worlds are retained in the atlas, allowing the rejection count to be correct.

Regression tests were added to `scripts/verify_backend.py`. These changes strengthen local computational reproducibility. Cross-platform reproducibility remains untested and the Python environment is not yet locked by a project-level hash.

## 6. Claims supported, falsified, and still unavailable

Supported within the inspected environment:

- exact same-seed local replay;
- mechanically complete accounting of failures and rejects after the corrections;
- retrospective motor errors reported above;
- monotone frequency-severity response under the coded multiplicative stress;
- sensitivity of accepted outcomes to the validation rule and seed.

Falsified or not supported:

- complete predictive validation: incurred loss misses its interval in both evaluation years;
- superior point prediction: transparent references perform better on some dimensions;
- empirical validation of the full procedural world grammar: the external motor module remains separate from the synthetic engine;
- demonstrated causal failure attribution: the Atlas records coded gates, not externally observed causes;
- calibrated severe-plausible scenario probabilities or thresholds;
- stable interval coverage, tail calibration, or external generalization.

## 7. Matched policy-level benchmark completed

The full 47-field audit and retrospective policy benchmark are executed in `17_DATA_QUALITY_POLICY_BENCHMARK.ipynb`. Policy-level frequency lowers count deviance from 0.8481 to 0.7871 in 2023 and from 0.9153 to 0.8330 in 2024. Aggregate count error improves slightly in 2023 but deteriorates slightly in 2024. The policy-level incurred-cost model is not consistently superior: its 2023 aggregate error rises to +9.58%, and its incurred deviance exceeds the policy-frequency/pooled-severity comparator in both years. Decile calibration shows systematic underprediction in low predicted-risk groups. No incurred total is covered by a process-only interval, and no model covers the 2024 count.

The quality audit also establishes that 8,543 of 50,807 claim-bearing policy-years have zero incurred cost. The implemented policy cost model therefore uses a non-negative Poisson pseudo-maximum-likelihood mean with reported claims as exposure rather than a positive-only Gamma severity model. This is an average-cost proxy and does not identify individual claim severity.

## 8. Procedural ablation completed

Five configurations were run over seeds 20260825-20260827 with 10,000 worlds each. All 15 configuration-seed pairs replayed exactly. Consuming 100 unused draws from the world stream leaves the full model unchanged but changes the shared-stream model, directly supporting stream isolation in the inspected environment.

The full configuration has a mean accepted-world failure rate of 35.95% across seeds. No validation gives 35.79%, strict rejection 36.83%, no transitions 35.70%, and a shared stream 35.20%. Strict rejection raises the combined failure-or-rejection rate to 49.41% because approximately 1,991 worlds per run are excluded. These are sensitivity results, not evidence that one validation policy produces more plausible scenarios. The ablation failures remain almost entirely traceability failures; only one combined-ratio failure occurs across the three full runs.

## 9. Remaining confirmatory requirement

The retrospective benchmark is complete and supports a bounded manuscript. Stronger validation now requires new evidence rather than further fitting to the inspected portfolio: a prospectively untouched period or independent portfolio, claim-level losses for tail-severity analysis, and observed or implanted failure labels for diagnostic accuracy. Without those inputs, claims of stable coverage, calibrated scenario plausibility, causal attribution, and external generalization remain unavailable.
