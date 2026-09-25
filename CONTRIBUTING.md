# Contributing

Changes to the scientific engine, calibration, metrics and claims require scientific review and a new verification record. Never replace a golden file merely to make a test pass. The phase-0 evidence directory and manifest are historical snapshots.

Use a feature branch and a pull request against `main`. Run the API contracts, artifact checksums, TypeScript build, browser tests and canonical replay. A changed scientific output must be labelled divergent until reviewed. Timing measurements describe their own host and do not use exact equality.

Raw policy data and private credentials do not belong in this repository. Replication that needs the raw dataset must use a separately obtained source with the documented SHA-256 and licence.

The application is bilingual. Changes to visible prose must preserve semantic parity between EN and FR. Original English paper quotations and machine-readable field identifiers are explicitly labelled.
