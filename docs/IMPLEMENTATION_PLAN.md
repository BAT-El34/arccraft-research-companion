# Plan d’implémentation et portes de sortie

## Phase 0 — clôture scientifique

Travail accompli : lecture du cahier, inventaire des 270 fichiers, moteur extrait, données réconciliées, suite historique, replays synthétiques et empiriques, golden master, registre C1–C8, proposition de commit.

Reste pour la clôture officielle : approuver les corrections éditoriales, désigner le run automobile de référence, qualifier l’installation vierge et approuver la matrice claim–métrique. Un changement de calcul ultérieur déclenchera de nouveaux replays ; une modification seulement éditoriale ne justifie pas de recalibrer le modèle.

## Phase 1 — extraction et isolation du produit

- Créer le dépôt GitHub et le projet Vercel distincts, avec les noms et la visibilité décidés.
- Scaffolder Next.js/TypeScript et les dépendances figées ; produire `package-lock.json` et le lock Python vérifié en environnement vierge.
- Garder le code scientifique revu, ses versions et ses tests ; écrire l’adaptateur FastAPI.
- Définir les registres de métriques, artefacts, variantes et licences et leur validation à la construction.
- Limiter le build web au code runtime et aux artefacts nécessaires ; aucune base générale ni brut.
- Établir le routage Next/Python et le valider sur une Preview du nouveau projet.

Sortie : build autonome, smoke test API, manifeste lisible, aucune dépendance au chemin ou au déploiement de l’ancienne application.

## Phase 2 — publication éditoriale

- Construire les dix pages et leur correspondance EN/FR, avec anglais par défaut et thème persistant.
- Reprendre le contenu approuvé, distinguer l’abstract anglais de sa traduction française.
- Générer les fiches des huit claims à partir des valeurs et formules versionnées.
- Relier figures 1–7, données, scripts, captions, alternatives textuelles et empreintes.
- Générer les graphiques depuis leurs CSV pour éviter la duplication manuelle des valeurs.
- Exposer PDF, bibliographie, citations BibTeX/RIS/CFF, limites et téléchargements conditionnés aux licences.

Sortie : le parcours reviewer permet de lire, vérifier et télécharger sans utiliser le laboratoire ; aucune valeur scientifique sans provenance ; erreurs D2/D3/D6 corrigées dans la version candidate.

## Phase 3 — reproductibilité interactive

- Implémenter les trois modes du laboratoire ; isoler chaque résultat et manifeste.
- Servir le canonique statique avec son statut pré-calculé ; proposer le replay live distinctement après qualification de l’environnement.
- Implémenter le registre des variantes d’ablation, leurs paramètres et seeds.
- Ajouter les filtres de l’Atlas complet, le statut du validateur, exports et replay par run.
- Contrôler la calibration automobile et les hypothèses non calibrées ; interdire l’usage des sinistres 2024 pour entraîner un modèle 2024.
- Implémenter erreurs, annulation, dépassement de budget et comparaison explicite des empreintes.

Sortie : un replay conforme est identifié avec son commit et son environnement ; une divergence est affichée comme divergence ; une exploration ne remplace jamais le canonique.

## Phase 4 — qualité, sécurité et déploiement

- Unitaires pertinents et contrats API ; JSON strict ; rejets/seed/validation/flux.
- E2E reviewer, replay, exploration, filtres et téléchargement ; tests d’échec réseau et timeout sans résultat périmé.
- Parité EN/FR, routes sans hash, thème persistant, titres et unités.
- Axe, clavier, zoom, lecteur d’écran ; captures visuelles desktop/mobile et absence de duplications.
- CSP, en-têtes, paramètres stricts, débit et taille, scans de dépendances et absence de secrets.
- Benchmarks réels du nouveau runtime ; limites serveur fondées sur le plan et mesures observées.
- Tests Chrome, Firefox, Safari, Edge et parcours mobiles ; noter les matrices non accessibles.
- Vérification Preview/staging puis production depuis le SHA approuvé.

Sortie : tous les P0 du cahier sont verts, limites du runtime mesurées et manifeste du build vérifié. Aucune promesse de conformité WCAG complète ne repose uniquement sur axe ou une capture.

## Phase 5 — publication scientifique

- Réexécuter le canonique dans l’environnement enregistré ; vérifier les artefacts et la matrice de claims.
- Recompiler une copie corrigée du LaTeX ; conserver le PDF original comme historique.
- Préparer la release brouillon, checksums, code, réplication, figures, SBOM/provenance si disponibles.
- Activer l’immutabilité avant publication finale, archiver et obtenir le DOI de version.
- Mettre à jour citations, site, paper et QR vers les identifiants définitifs.
- Vérifier les liens, SHA, DOI, licences et les vingt critères de recette.

Sortie : GitHub, archive, paper et site citent la même version ; domaine vivant et archive sont distingués.

## Critères de CI

À chaque PR : lint/formatage, TypeScript, tests Python/frontend et API, checksums, replay réduit et golden, build et contrôle du bundle, axe et E2E Preview, captures. Avant release : canonique complet, variantes enregistrées, benchmark empirique, compilation LaTeX et revue scientifique.

Les modifications du moteur, des données ou des claims nécessitent une revue. Les timings ne sont pas testés par égalité : leur environnement et leur statut historique restent explicites. La CI doit refuser un statut `PUBLISHED` si une provenance, une licence requise ou l’archive finale manque.

## Décisions attendues

| Décision | Proposition prête à examiner | Dépendance |
|---|---|---|
| Moteur à geler | État local corrigé ; commit source `b642f8238d86b5ec3a4115d9d06d582682d69f1e` | Fin de phase 0 |
| Corrections du paper | Patch séparé, CSV faisant autorité pour les valeurs et déciles | Publication éditoriale finale |
| Run automobile de référence | Seed 42, 50 000 simulations, calibration 2022–2023, évaluation 2024 | Chiffres d’accueil et replay automobile |
| Noms | `BAT-El34/arccraft-research-companion` et Vercel `arccraft-research-companion` | Création des services distincts |
| Visibilité | Publique immédiate ou après staging | Publication distante |
| Licences | Choix des auteurs pour code/texte/figures ; source automobile CC BY 4.0 documentée | Redistribution et citation |
| Auteurs | ORCID, affiliations, correspondant, rôles collaborateurs | Citations et paper final |
| Publication | Statut exact et métadonnées de revue | Citation finale |
| Archive | Zenodo proposé, DOI à réserver | Release finale |
| Domaine et budget | Domaine final, plan Vercel, plafond de calcul et débit | Production et QR |

Les autres datasets ne sont pas nécessaires à ce MVP. Leur présence sur disque n’autorise pas leur utilisation dans de nouvelles métriques.
