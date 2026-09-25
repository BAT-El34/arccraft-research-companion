# ARCCRAFT Research Companion — candidat scientifique

Phase 0 réalisée le 25 septembre 2026. **Candidat local, pas une application publiée ni une release scientifique approuvée.**

Lire [le rapport de phase 0](docs/PHASE_0_REPORT.md), [l’architecture retenue](docs/ARCHITECTURE.md) et [le plan d’implémentation](docs/IMPLEMENTATION_PLAN.md).

Le nouveau dépôt local est indépendant de l’application de référence. Aucun remote GitHub ni projet Vercel n’a encore été créé : cette livraison précède la décision de gel demandée. Les fichiers originaux ont été lus et contrôlés par empreinte, jamais modifiés.

## Contenu

- `arccraft/` : moteur synthétique extrait octet pour octet, moteur automobile extrait sans changement de formule, calibration compacte vérifiée, benchmark par police.
- `evidence/` : copies préservées du manuscrit, des résultats, figures, scripts et sources LaTeX. Ce sont des preuves historiques, avec leurs incohérences recensées.
- `artifacts/candidate/` : golden master candidat, mondes complets, Atlas complet, résultats canoniques et automobiles.
- `audit/` : inventaire SHA-256, réconciliation publique/locale, contrôles de données, replays, huit claims, environnement et intégrité des originaux.
- `proposals/` : corrections éditoriales proposées, sans modification des originaux.
- `scripts/` : procédures exécutables. Les scripts d’audit historique utilisent les chemins de la recherche locale ; les replays canoniques et par police sont autonomes.

## Rejouer

Environnement vérifié : Windows AMD64, Python 3.12.14, NumPy 2.3.5. Les versions scientifiques exactes sont enregistrées dans `requirements-replay.lock`. Cette capture de 70 paquets n’a pas encore été testée par installation dans un environnement vierge.

```powershell
python -B scripts/verify_checksums.py
python -B scripts/replay_canonical.py
python -B scripts/run_ablation.py
python -B scripts/verify_science.py
python -B scripts/replay_policy.py --csv "D:\Projet\SOUTENANCE\Quantitative_Datasets_Clean_Final\Dataset of motor insurance portfolio (1).csv"
```

`replay_canonical.py` ne requiert que NumPy et n’écrase jamais le golden master. `run_ablation.py` et `verify_science.py` demandent les dépendances de recherche et écrivent uniquement les nouveaux résultats dans ce dépôt. Les durées de nouveaux runs ne remplacent pas celles du paper.

Le moteur automobile utilise un petit JSON de calibration, sans SQLite ni accès à l’ancienne application. Le benchmark par police vérifie le SHA-256 du CSV avant son utilisation et ne l’écrit jamais.

## Identité et statut

Le commit des sources de vérification est `b642f8238d86b5ec3a4115d9d06d582682d69f1e`. Le manifeste distingue ce commit connu de l’état historique non commité qui avait produit le paper. Il n’invente pas de commit historique.

Le package candidat porte la version `0.1.0.dev1`. La constante historique du moteur reste `0.1.0` et sa grammaire `world_grammar-0.1.0` ; leur identité scientifique est complétée par le SHA-256 et le commit, car le backend historique portait déjà les mêmes versions déclarées.

La licence du code, des textes et des figures doit être décidée par leurs ayants droit. La source automobile est CC BY 4.0, vérifiée auprès de Mendeley. Aucun DOI, tag final, statut de publication ou droit de redistribution des autres datasets n’est inventé.
