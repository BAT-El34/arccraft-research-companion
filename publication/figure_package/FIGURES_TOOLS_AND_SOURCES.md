# ARCCRAFT Figures: Internal Production Record

This file documents the evidence, production assets, and manuscript captions for the figure package. It is an internal reproducibility record and is not a manuscript annex.

## Figure inventory

| Figure | Title | Type | Scientific role | Data dependency | Complexity |
|---|---|---|---|---|---|
| 1 | ARCCRAFT Procedural Architecture and Evidence Boundaries | Strategic | Defines the registered procedural flow and separates computational replay from empirical validation | Paper internal specification | High |
| 2 | Motor Portfolio Scale, Outcome Dynamics, and Composition Shift, 2022 to 2024 | Technical | Establishes portfolio growth, temporal outcome changes, and the composition shift that motivates temporal evaluation | Public portfolio data, results embedded | Medium |
| 3 | Temporal Forecast Performance Across Matched Actuarial Comparators | Technical | Compares aggregate accuracy and policy level deviance for pooled and policy level benchmarks | Benchmark outputs, results embedded | High |
| 4 | Risk Decile Calibration and Process Interval Coverage | Technical | Tests risk stratification and aggregate process interval coverage | Benchmark outputs, results embedded | High |
| 5 | Frequency and Severity Stress Surface for the Motor Portfolio | Technical | Shows the joint stress response and the technical loss ratio crossing | Registered stress simulation, results embedded | Medium |
| 6 | Scenario Class Failure Rates and Failure Atlas Composition | Technical | Shows class conditional failures and the operational dominance of the traceability gate | Canonical procedural run, results embedded | Medium |
| 7 | Procedural Ablations, Computational Cost, and Stream Isolation | Technical | Tests procedural sensitivity, runtime, exact replay, and random stream isolation | Registered ablation runs, results embedded | High |
| 8 | Public ARCCRAFT Demonstrator Access | Technical | Provides direct access to the public ARCCRAFT interface while separating the demonstrator from the authoritative research artifacts | Validated public deployment | Low |

## Data sources

The external benchmark uses the [motor insurance portfolio dataset](https://data.mendeley.com/datasets/sw4jmdb2sm/1) published through Mendeley Data by Universitat de València and Universidad de Alcalá. Version 1 contains 354,140 observations and 47 variables covering 2022 to 2024 under a CC BY 4.0 licence. Persistent identifier: [doi:10.17632/sw4jmdb2sm.1](https://doi.org/10.17632/sw4jmdb2sm.1).

Internal evidence tables used to freeze plotted values:

| Figure | Evidence file or registered source |
|---|---|
| 1 | `29_ARCCRAFT_MANUSCRIPT_DRAFT.md`, Sections 3.2 to 3.9 |
| 2 | `18_DATA_QUALITY_FINDINGS.csv` and `24_TEMPORAL_CATEGORY_SHIFT.csv` |
| 3 | `19_POLICY_BENCHMARK_RESULTS.csv` |
| 4 | `20_POLICY_DECILE_CALIBRATION.csv` and `19_POLICY_BENCHMARK_RESULTS.csv` |
| 5 | `11_STRESS_SURFACE_RESULTS.csv` |
| 6 | Canonical 10,000 world run at seed 20260825, reconciled with `25_ARCCRAFT_ABLATION_RESULTS.csv` |
| 7 | `26_ARCCRAFT_ABLATION_SUMMARY.csv` and `27_STREAM_ISOLATION_TEST.csv` |
| 8 | [Public ARCCRAFT demonstrator](https://actuarial-digital-dashboard-rd-v3.vercel.app/fr#/arccraft), inspected on 25 September 2026 |

## Production assets

Figure 1 is defined as a complete standalone LaTeX source in `code/Figure1_tikz.tex`. Figures 2 to 8 are defined as self contained Python 3.10 or later scripts in `code/Figure2.py` through `code/Figure8.py`. Each technical script installs only missing dependencies, embeds its frozen evidence values or validated destination, creates the `figures` directory when required, and exports the matching PNG at 300 dpi.

The technical figures use NumPy and Matplotlib. The strategic figure uses LaTeX, TikZ, TikZ CD, Xcolor, and Palatino compatible typography. Production tool names are confined to this internal record and source code and do not appear in the manuscript body or figure captions.

## Reproduction

Run each technical script from the package root so its relative output path resolves to `figures/FigureN.png`. Compile `code/Figure1_tikz.tex` as a standalone document, then rasterize the resulting PDF at 300 dpi or higher to `figures/Figure1.png`.

## Publication captions

### Figure 1

**ARCCRAFT procedural architecture and evidence boundaries.** The specification layer registers the experiment, generates procedural worlds, separates stochastic streams, and validates states before simulation. The simulation layer links transitions and noncompensatory gates to replayable Failure Atlas records and reverse stress search, while the evaluation layer keeps computational replay distinct from empirical validation and classifies the resulting evidence as supported, mixed, or unsupported.

### Figure 2

**Motor portfolio scale, outcome dynamics, and composition shift, 2022 to 2024.** Panel A reports the growth from 67,172 to 168,133 policy year records. Panel B shows annual claim frequency and loss ratio, while Panel C shows the decline in the new business share from 97.91% to 57.34%, a 40.57 percentage point change that supports temporal rather than random evaluation. Source: public Spanish motor insurance portfolio, 2022 to 2024.

### Figure 3

**Temporal forecast performance across matched actuarial comparators.** Panels A and B report aggregate errors relative to observed claim counts and incurred losses, where zero denotes perfect aggregate prediction. Panels C and D report policy level Poisson deviance, where smaller values indicate better predictive discrimination; policy level frequency improves deviance in both years, but the policy level cost model produces a pronounced 2023 aggregate error and never dominates the pooled cost comparator. Source: retrospective ARCCRAFT benchmark using the public Spanish motor insurance portfolio.

### Figure 4

**Risk decile calibration and process interval coverage.** Panels A and B plot observed to predicted ratios by predicted risk decile, with 1.00 denoting perfect calibration; the lowest predicted risk groups are materially underpredicted, particularly for 2024 incurred loss. Panels C and D normalize predictions and their 95% process only intervals to the observed aggregate, showing count coverage in 2023, count misses in 2024, and incurred loss misses for every comparator and year. Source: retrospective ARCCRAFT benchmark using the public Spanish motor insurance portfolio.

### Figure 5

**Frequency and severity stress surface for the motor portfolio.** Panel A reports the mean simulated loss ratio for the 25 combinations of frequency and severity multipliers, with the outlined cell identifying the joint 25% stress. Panel B follows the equal multiplier path and shows the 95% process interval; the joint 1.25 multiplier produces a mean loss ratio of 1.11, above the technical threshold of 1.00. Source: registered ARCCRAFT stress simulations using the retrospective motor calibration.

### Figure 6

**Scenario class failure rates and Failure Atlas composition.** Panel A reports failures among accepted worlds for each registered scenario class in the canonical 10,000 world run, from 0.00% under Baseline to 49.88% under Severe plausible conditions; Exploratory worlds remain analytically separate. Panel B reports atlas events on a logarithmic axis and shows that 3,588 traceability failures dominate one combined ratio failure and five structural rejections, so the experiment primarily tests the operational gate rather than actuarial insolvency detection. Source: canonical ARCCRAFT run, registered seed 20260825.

### Figure 7

**Procedural ablations, computational cost, and stream isolation.** Panel A compares failures among accepted worlds with the broader failure or rejection measure across three registered runs per configuration; strict rejection creates the largest divergence because repaired worlds become structural rejections. Panel B reports mean runtime with one standard deviation, while Panel C shows exact replay in all 15 runs and confirms that named streams preserve claims and behavioural outputs after 100 irrelevant world draws, whereas a shared stream does not. Source: ARCCRAFT ablation and stream isolation experiments at registered seeds 20260825, 20260826, and 20260827.

### Figure 8

**Public ARCCRAFT demonstrator access.** The QR code opens the ARCCRAFT module within the integrated MAPTA, COMPASS, and ARCCRAFT demonstrator. The public deployment exposes API version 2.1.0 and executes the synthetic simulation endpoint. It is provided for interface inspection rather than as the authoritative source of the paper's numerical results because parts of the deployed backend differ from the current local working tree.
