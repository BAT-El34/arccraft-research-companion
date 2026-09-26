# Dictionnaire de données

Source : dictionnaire du dataset Mendeley Data v1, DOI 10.17632/sw4jmdb2sm.1 (CC BY 4.0). Schéma du dérivé de recherche réconcilié avec la source brute.

Commit de vérification : b642f8238d86b5ec3a4115d9d06d582682d69f1e. SHA-256 dictionnaire : `cde44e797a7fd34de29199c78c9301d6f00ed94fd725b4fe8e67e6c2c4cc2e41`.

| Champ | Type du dérivé |
|---|---|
| `insured_id` | INTEGER |
| `year` | INTEGER |
| `policy_type` | TEXT |
| `policy_status` | TEXT |
| `business_type` | TEXT |
| `payment_frequency` | TEXT |
| `bonus_score` | TEXT |
| `driver_age` | REAL |
| `vehicle_age` | REAL |
| `age_driving_licence` | REAL |
| `fuel_type` | TEXT |
| `vehicle_value` | REAL |
| `seats` | INTEGER |
| `power_to_weight_ratio` | REAL |
| `vehicle_brand` | TEXT |
| `municipality_type` | TEXT |
| `circulation_area` | TEXT |
| `total_premium` | REAL |
| `liability_premium` | REAL |
| `property_damage_premium` | REAL |
| `theft_premium` | REAL |
| `fire_premium` | REAL |
| `glass_premium` | REAL |
| `legal_protection_premium` | REAL |
| `occupants_premium` | REAL |
| `total_claims` | INTEGER |
| `liability_claims` | INTEGER |
| `liability_property_claims` | INTEGER |
| `liability_injury_claims` | INTEGER |
| `property_claims` | INTEGER |
| `theft_claims` | INTEGER |
| `fire_claims` | INTEGER |
| `glass_claims` | INTEGER |
| `legal_protection_claims` | INTEGER |
| `occupants_claims` | INTEGER |
| `total_incurred` | REAL |
| `liability_incurred` | REAL |
| `liability_property_incurred` | REAL |
| `liability_injury_incurred` | REAL |
| `property_incurred` | REAL |
| `theft_incurred` | REAL |
| `fire_incurred` | REAL |
| `glass_incurred` | REAL |
| `legal_protection_incurred` | REAL |
| `occupants_incurred` | REAL |
| `total_exposure` | REAL |
| `liability_exposure` | REAL |

Les métadonnées de variable et transformations complètes sont conservées dans `audit/data-reconciliation.json` et exposées sans les données individuelles via `/data/provenance.json`. Les valeurs nulles ne sont pas converties en zéro.

La calibration runtime contient seulement des agrégats vérifiés, par période. Les données brutes, SQLite et les autres bases ne sont pas dans le bundle de calcul.
