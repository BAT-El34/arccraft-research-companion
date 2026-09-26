# ARCCRAFT Research Companion — candidat scientifique

Phase 0 validée par l’utilisateur le 25 septembre 2026. **Application candidate fonctionnelle ; release scientifique finale en attente de licences, métadonnées auteurs et DOI.**

Lire [le rapport de phase 0](docs/PHASE_0_REPORT.md), [l’architecture retenue](docs/ARCHITECTURE.md) et [le plan d’implémentation](docs/IMPLEMENTATION_PLAN.md).

Le dépôt [BAT-El34/arccraft-research-companion](https://github.com/BAT-El34/arccraft-research-companion) et le [projet Vercel](https://arccraft-research-companion.vercel.app/en/) sont indépendants de l’application de référence. Les fichiers originaux restent intacts.

## Contenu

- `arccraft/` : moteur synthétique extrait octet pour octet, moteur automobile extrait sans changement de formule, calibration compacte vérifiée, benchmark par police.
- `evidence/` : copies préservées du manuscrit, des résultats, figures, scripts et sources LaTeX. Ce sont des preuves historiques, avec leurs incohérences recensées.
- `artifacts/candidate/` : golden master candidat, mondes complets, Atlas complet, résultats canoniques et automobiles.
- `audit/` : inventaire SHA-256, réconciliation publique/locale, contrôles de données, replays, huit claims, environnement et intégrité des originaux.
- `proposals/` : corrections éditoriales proposées, sans modification des originaux.
- `scripts/` : procédures exécutables. Les scripts d’audit historique utilisent les chemins de la recherche locale ; les replays canoniques et par police sont autonomes.

## Rejouer

Environnement vérifié : Windows AMD64, Python 3.12.14, NumPy 2.3.5. Les versions scientifiques exactes sont enregistrées dans `requirements-replay.lock`. Cette capture de recherche contient 70 paquets. Le runtime web est verrouillé séparément dans `requirements-runtime.lock` et a été installé et testé dans un environnement vierge, avec replay exact et tous les contrats API.

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

## Exécuter l’application

```sh
python -m venv .venv
# Activate .venv using the command for your shell.
python -m pip install -r requirements-runtime.lock
npm ci
npm run build
python scripts/serve_local.py
```

Ouvrir http://127.0.0.1:3000/en/ ou /fr/. Le serveur local sert l’export Next.js et la véritable API sur la même origine. `npm run dev` ne sert que le frontend ; utiliser le serveur ci-dessus pour vérifier le parcours scientifique complet.

```sh
python -m unittest discover -s tests -v
python scripts/verify_web_artifacts.py
npx playwright install chromium
npm run test:e2e
```

Les originaux sont sous `evidence/` ; les copies éditoriales corrigées sont sous `publication/`. `scripts/build_publication.py` régénère les copies à partir des preuves et des patches approuvés (requiert les dépendances de figures, dont qrcode et Pillow). Compiler ensuite `publication/latex/main.tex` avec pdflatex, bibtex, pdflatex deux fois, puis appeler `build_registry()` pour actualiser le PDF et les checksums avant le build web.

Le calcul public Vercel exige une règle de débit qualifiée. La règle du nouveau projet a été contrôlée : trois POST par minute et IP, puis HTTP 429. Les déploiements antérieurs à son activation peuvent encore annoncer le calcul indisponible. Le frontend ne transforme jamais une erreur ou un dépassement de temps en résultat de référence. Le DOI et les licences en attente interdisent le statut de release finale, pas l’inspection du candidat.

Voir [API](docs/API.md), [contribution](CONTRIBUTING.md), [sécurité](SECURITY.md) et [changements](CHANGELOG.md).

Voir le [rapport de livraison](docs/DELIVERY_REPORT.md) pour les vérifications et décisions restantes. Le replay synthétique Linux conserve son statut `DIVERGENT` à pleine précision ; le rapport documente l’écart sans changer la référence Windows.
