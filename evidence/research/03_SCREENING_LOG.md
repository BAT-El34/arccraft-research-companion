# ARCCRAFT literature screening log

Status date: 23 September 2026  
Protocol: `01_SEARCH_PROTOCOL.md` version 1.0  
Extraction file: `02_LITERATURE_EXTRACTION.csv`

## 1. Current screening status

- Records retained in the structured extraction: **67**.
- Peer-reviewed journal articles or scholarly books: **55**.
- Official regulatory, supervisory, professional-standard, or documented public-data sources: **11**.
- Technical report retained for implementation provenance: **1** (the PCG family report).
- Records with fully verified title and DOI or official URL: **63**.
- Records requiring a final metadata check before bibliography export: **4** (`L014`, `L019`, `L022`, and `L025`).

These counts describe the retained evidence set, not a PRISMA claim. The discovery interfaces used in this phase do not expose stable, exhaustive database-result counts, so an invented total number of search hits would be misleading. Before submission, the authors should repeat the frozen queries in named bibliographic databases that provide exportable result sets and record exact retrieval counts and deduplication decisions.

## 2. Search families executed

| Search family | Core concepts | Date searched | Retention outcome |
|---|---|---:|---:|
| Insurance stress testing | insurance, stress test, solvency, severe plausible, dynamic scenario | 23 Sep 2026 | 6 core official/scholarly sources |
| Reverse and systematic stress | reverse stress, entropy/KL, plausible severe scenario, empirical likelihood, dynamic loss | 23 Sep 2026 | 7 sources |
| Frequency-severity modelling | compound loss, dependence, copula, longitudinal, random effects, GLM | 23 Sep 2026 | 10 sources |
| Synthetic insurance systems | synthetic claims, artificial insurer, claim simulator, open benchmark | 23 Sep 2026 | 5 sources |
| Calibration and tail validation | proper scores, calibration, coverage, VaR/ES, exceedance backtesting | 23 Sep 2026 | 10 sources |
| Uncertainty and model risk | aleatory, epistemic, discrepancy, model risk, distribution shift | 23 Sep 2026 | 7 sources |
| Simulation V&V and sensitivity | verification, validation, metamodel, Morris, Sobol, global sensitivity | 23 Sep 2026 | 6 sources |
| Reproducibility and random streams | computational reproducibility, seed, streams, substreams, PCG | 23 Sep 2026 | 5 sources |
| Computational benchmarks | nested simulation, regression, sample recycling, least-squares Monte Carlo | 23 Sep 2026 | 6 sources |
| Public motor data and benchmarks | freMTPL2, CASdatasets, motor frequency/severity comparison | 23 Sep 2026 | 2 sources |

The category totals overlap because several sources support more than one methodological question. The extraction file assigns one primary strand to each source to prevent double counting.

## 3. Inclusion decisions

A source was retained when it directly supports at least one of the following:

1. an established definition that ARCCRAFT must respect;
2. a close methodological predecessor against which novelty must be judged;
3. a benchmark or ablation design;
4. a validation metric or falsification rule;
5. an implementation-level reproducibility claim;
6. a regulatory or professional expectation relevant to model use and limitation disclosure;
7. a documented public dataset or simulator needed for external replication.

The `critical_limit_for_ARCCRAFT` field records why a retained source cannot be used as evidence that ARCCRAFT itself is valid.

## 4. Exclusion rules applied during discovery

The following were screened out of the retained evidence set:

- duplicate preprint, repository, aggregator, or mirror records when a version of record was identifiable;
- marketing pages, informal tutorials, Wikipedia pages, and discussion-forum posts;
- sources that used the phrase *stress testing* without a scenario-design, validation, insurance, risk, or simulation contribution;
- generic machine-learning papers with no transferable calibration, robustness, or simulation-validation result;
- synthetic datasets without a documented generation method or scholarly/official provenance;
- papers dated after the search cut-off or listed only as forthcoming without a citable version of record;
- banking sources used only by analogy when a closer insurance source was available.

Banking material was retained only for formal scenario-selection, reverse-stress, backtesting, or model-risk principles that are explicitly transferable. It will be labelled as cross-domain evidence in the manuscript.

## 5. Quality hierarchy for synthesis

1. Peer-reviewed actuarial and risk journals directly addressing insurance claims, solvency, or stress testing.
2. Official insurance supervisory and actuarial-standard publications.
3. General statistical and simulation-methodology literature.
4. Banking/financial-risk literature used transparently by analogy.
5. Technical reports used only for implementation provenance.

No claim about ARCCRAFT's empirical performance may rest solely on levels 4 or 5.

## 6. Required completion before submission

- Verify the four partial metadata records.
- Export full bibliographic records and abstracts from at least two indexed scholarly databases.
- Conduct backward citation searching from `L005`, `L009`, `L011`, `L013`, `L015`, `L026`, `L029`, `L031`, and `L048`.
- Conduct forward citation searching for the same seed set through the frozen date.
- Record exact retrieved, deduplicated, title-screened, full-text-screened, included, and excluded counts.
- Add a reason code for every full-text exclusion.
- Freeze a bibliography snapshot and archive the query/export files with hashes.

