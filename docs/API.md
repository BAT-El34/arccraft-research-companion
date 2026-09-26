# API v1

The interactive OpenAPI specification is `/api/v1/docs`. All responses are strict JSON; undefined scientific quantities are `null`.

| Endpoint | Purpose |
|---|---|
| `GET /api/v1/health` | Runtime identity, science/build commits, integrity and computation availability |
| `GET /api/v1/runs/canonical` | Precomputed reference identity, parameters and artifact registry |
| `GET /api/v1/artifacts/{id}` | Closed registry lookup; no arbitrary path resolution |
| `POST /api/v1/simulate/synthetic` | Canonical, registered or exploratory synthetic execution |
| `POST /api/v1/simulate/motor` | Canonical or exploratory motor projection |

Canonical synthetic requests lock `variant=full`, `seed=20260825`, `worlds=10000`. Registered variants allow the five paper configurations and seeds 20260825–20260827. Exploration allows 100–10000 worlds and unsigned 32-bit seeds. `world_id` replays the entire run before selecting a world.

Canonical motor requests lock seed 42, 50000 simulations, calibration 2022–2023, target 2024 and unmodified frequency/severity. Explorations accept 500–50000 simulations and multipliers 0.5–2.0. Expense and commission assumptions must either both be absent or both supplied between 0 and 1. Target-year claims are evaluation-only.

Every run has an ID, mode, parameter hash, deterministic result hash, versions, environment, duration and warnings. `VERIFIED` means the applicable numerical fingerprint matches; it does not imply predictive validation. `EXPLORATORY_NOT_VALIDATED` is not a publication status. `DIVERGENT` is never silently coerced into a match.

Failures: 422 invalid/unknown parameter, 413 oversized body, 404 unknown artifact, 503 public compute not qualified or engine integrity failure. Client budget: 55 seconds; Vercel function budget: 60 seconds. A browser abort does not cancel remote execution.
