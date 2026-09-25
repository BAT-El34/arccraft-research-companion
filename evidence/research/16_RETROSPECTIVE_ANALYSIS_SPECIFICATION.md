# Retrospective data-quality and policy-level benchmark specification

Frozen: 23 September 2026, before execution of the final policy-level notebook  
Status: retrospective analysis specification, not a preregistration  
Authors: Elia Batako and Manuel Ntumba

## 1. Scope

This analysis uses the normalized `motor_portfolio` table to assess whether the 47 supplied fields are fit for a retrospective temporal benchmark and whether policy-level risk differentiation improves aggregate 2023 and 2024 forecasts relative to the existing pooled frequency-severity mean.

The 2024 aggregate result had already been inspected before this specification. A prototype policy model was also executed once during implementation. The final analysis is therefore exploratory and cannot be represented as blinded or confirmatory.

## 2. Temporal evaluation

- Origin 1: fit on 2022 and evaluate on 2023.
- Origin 2: fit on 2022-2023 and evaluate on 2024.
- Target-year portfolio characteristics and exposure are treated as known at the start of evaluation.
- No random train-test split will be used, because it would mix calendar periods and repeated insured identifiers.

## 3. Eligible predictors

The models may use:

- policy type;
- business type;
- payment frequency;
- bonus score;
- driver age;
- vehicle age;
- the ambiguous `age_driving_licence` field only as an unidentified numeric proxy;
- fuel type;
- declared vehicle value;
- seat count;
- power-to-weight ratio;
- vehicle brand;
- municipality type;
- circulation area.

The following fields are excluded from predictors:

- `insured_id`, because it is an identifier;
- `policy_status`, because cancellation status may be determined after inception and creates look-ahead risk;
- all premium, claim, incurred, and coverage-component outcomes;
- target-year outcomes of any kind.

`total_exposure` is used only as the frequency offset. `total_claims` is used as the training offset for the claim-cost model.

## 4. Fixed preprocessing

- Numeric missing values: calibration-period median.
- Numeric clipping: calibration-period 0.5th and 99.5th percentiles.
- Numeric scaling: calibration-period mean and standard deviation.
- Log transforms: vehicle value and power-to-weight ratio.
- Quadratic terms: driver age, vehicle age, licence-value proxy, and log vehicle value.
- Categorical encoding: reference-cell one-hot encoding.
- Vehicle brands with fewer than 500 calibration rows: `__OTHER__`.
- Previously unseen target categories: `__OTHER__`.
- No target-period statistic is used during preprocessing.

## 5. Models

### B0. Aggregate pooled mean

Pooled calibration-period claim frequency multiplied by target exposure, and pooled incurred loss per reported claim multiplied by predicted claims.

### B1. Policy frequency plus pooled severity

Penalized Poisson pseudo-maximum-likelihood frequency model with log exposure offset, followed by the pooled incurred loss per reported claim.

### B2. Policy frequency plus policy severity

The B1 frequency model combined with a penalized Poisson pseudo-maximum-likelihood cost-per-reported-claim model. The cost model uses policy-year incurred loss as the non-negative response and reported claims as the offset. This quasi-likelihood admits the observed zero-incurred claim rows; it is not presented as a literal Poisson currency distribution.

All penalized coefficients except the intercept use a fixed ridge coefficient of `1e-4`. Optimization uses L-BFGS-B with at most 500 iterations. No penalty or feature tuning is performed against 2024.

## 6. Metrics

For each origin and model:

- aggregate claim-count percentage error;
- aggregate incurred-loss percentage error;
- policy-level Poisson deviance for claim count;
- policy-level Poisson pseudo-deviance for incurred loss;
- process-only 95% aggregate intervals using a Poisson claim count and the supplied lognormal-severity dispersion proxy;
- observed-to-predicted ratios by predicted-risk decile for B2.

Process intervals exclude parameter uncertainty and are not full predictive intervals.

## 7. Data-quality gates

The audit will report, without silent repair:

- schema and dictionary agreement;
- null, empty-string, and sentinel-value counts;
- duplicate keys and exact duplicates;
- domain ranges and robust quantiles;
- zero-exposure and zero-premium contradictions;
- claim-count/incurred-cost contradictions;
- reconciliation of total premium, total claim count, and total incurred loss to coverage components;
- category cardinality and year-level composition drift;
- repeated-insured overlap between adjacent years;
- potential look-ahead variables and semantic conflicts.

Rows with zero exposure are excluded only from frequency fitting because a log exposure offset is undefined. Their count and outcomes remain reported.

## 8. Decision rules

- A policy model is not superior merely because one aggregate error is smaller.
- Improvement must be dimension-specific and consistent with policy-level deviance and calibration diagnostics.
- Failure of optimization, reconciliation, temporal transfer, or process-interval coverage is reported directly.
- Two forecast origins are insufficient for stable interval-coverage, tail-calibration, or generalization claims.
