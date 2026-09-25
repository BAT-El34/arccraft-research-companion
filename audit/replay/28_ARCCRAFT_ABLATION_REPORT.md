# ARCCRAFT procedural ablation report

**Authors:** Elia Batako and Manuel Ntumba  
**Status:** synthetic computational experiment; not empirical product validation  
**Seeds:** 20260825, 20260826, 20260827  
**Worlds per configuration and seed:** 10,000

## Design

The experiment changes one procedural component at a time relative to the full ARCCRAFT implementation. `no_validator` passes raw worlds directly to the simulator; `strict_reject` rejects every world that the full validator would repair; `no_transitions` holds the validated initial state fixed over the twelve periods; and `shared_stream` replaces the three named PCG64 substreams with one sequential generator. All comparisons remain synthetic and conditional on the current world grammar and product assumptions.

## Reproducibility tests

Every configuration reproduced an identical result fingerprint when rerun with the same seed: **True**. Consuming 100 unused draws from the world stream left the full model invariant: **True**. The same intervention changed results under the shared-stream ablation: **True**. This is direct evidence for stream isolation as an engineering reproducibility property, not evidence of actuarial accuracy.

## Main result

The numerical evidence is stored in `25_ARCCRAFT_ABLATION_RESULTS.csv` and its across-seed summary in `26_ARCCRAFT_ABLATION_SUMMARY.csv`. Differences across validator and transition configurations show that reported failure regions are conditional on procedural design choices. They must therefore be reported with the grammar, validation policy, horizon, seed regime, and gate definitions rather than treated as invariant portfolio facts.

## Interpretation boundary

The ablation evaluates internal computational behaviour. It cannot validate the scenario probabilities, state-transition laws, loss model, or economic realism because those elements remain scenario assumptions. Runtime is wall-clock time on the execution host and is descriptive, not a portable performance guarantee.
