# Cahier des charges de l’application de publication scientifique ARCCRAFT

## 0. Fiche de cadrage

| Élément | Définition |
|---|---|
| Nom de travail | ARCCRAFT Research Companion |
| Objet | Application web scientifique associée au paper *Procedural Stress Testing of Actuarial Models: Design and Preliminary Evaluation of the ARCCRAFT Framework* |
| Auteurs affichés | Elia Batako et Manuel Ntumba |
| Langues | Anglais par défaut, français intégralement disponible |
| Dépôt cible proposé | `BAT-El34/arccraft-research-companion` |
| Projet Vercel cible proposé | `arccraft-research-companion` |
| Domaine cible proposé | Sous-domaine ou domaine propre à confirmer après création du projet |
| Statut du présent document | Spécification fonctionnelle, scientifique, technique et éditoriale, version 1.0 |
| Date de référence | 25 septembre 2026 |
| Application auditée | `actuarial_digital_dashboard_rd`, plateforme MAPTA, COMPASS et ARCCRAFT v2.1 |
| Déploiement audité | [Démonstrateur intégré existant](https://actuarial-digital-dashboard-rd-v3.vercel.app/fr#/home) |
| Code local audité | `mapta-compass-arccraft-platform-v2.1-FINAL/mapta-compass-arccraft-poc` |

## 1. Résumé exécutif

La nouvelle application doit être une publication scientifique interactive consacrée exclusivement à ARCCRAFT. Elle ne doit pas être une nouvelle version générale de la plateforme MAPTA, COMPASS et ARCCRAFT. Elle doit permettre à un lecteur, un reviewer, un actuaire ou un chercheur de comprendre le paper, vérifier les résultats annoncés, consulter les données et leurs provenances, rejouer les expériences enregistrées, télécharger les artefacts, citer correctement le logiciel et identifier précisément la version qui a produit chaque résultat.

L’application existante constitue une base graphique et fonctionnelle utile. Elle dispose déjà d’une identité éditoriale forte, d’un thème clair et sombre, d’une interface bilingue, d’un moteur ARCCRAFT exécutable, d’un catalogue de données et de garde-fous explicites. Elle ne peut toutefois pas être utilisée telle quelle comme artefact scientifique officiel du paper pour quatre raisons principales:

1. elle agrège trois projets scientifiques différents, MAPTA, COMPASS et ARCCRAFT;
2. son backend public ne correspond pas exactement à l’état local actuel du moteur ARCCRAFT;
3. plusieurs résultats affichés sont embarqués ou illustratifs alors que d’autres proviennent du backend, sans séparation toujours assez forte pour un lecteur scientifique;
4. la capture longue révèle des blocs dupliqués dans plusieurs écrans, ce qui impose une correction de rendu avant publication.

La solution cible doit donc séparer trois objets:

| Objet | Rôle | Autorité scientifique |
|---|---|---|
| Application Vercel | Consultation, navigation, visualisation et replay contrôlé | Interface vivante, non autorité unique |
| Release GitHub immuable | Code, configurations, tests, résultats dérivés et manifestes | Version logicielle citée |
| Archive scientifique avec DOI | Snapshot pérenne du code, des données redistribuables, des checksums et du paquet de réplication | Artefact scientifique de référence |

## 2. Objectifs

### 2.1 Objectif principal

Transformer le paper ARCCRAFT en une publication web vérifiable, lisible et reproductible, sans présenter le cadre proposé comme une théorie établie ni convertir une démonstration computationnelle en validation empirique.

### 2.2 Objectifs secondaires

- Donner accès au paper anglais en PDF et à une présentation web structurée.
- Relier chaque affirmation quantitative à sa métrique, sa table, sa figure et son fichier source.
- Permettre le replay exact de l’expérience canonique enregistrée.
- Permettre des explorations paramétriques clairement séparées du résultat publié.
- Exposer le Failure Atlas et les mécanismes de validation, réparation et rejet.
- Rendre visibles les versions du moteur, de la grammaire, de la calibration, des données, du schéma de sortie et du commit.
- Fournir des téléchargements vérifiables par empreinte SHA-256.
- Proposer une citation correcte du paper, du logiciel et des données.
- Conserver les modes clair et sombre ainsi que l’interface anglais et français.
- Déployer l’ensemble dans un dépôt GitHub et un projet Vercel totalement distincts.

### 2.3 Non-objectifs

- Ne pas reproduire MAPTA ou COMPASS dans le nouveau produit.
- Ne pas fournir une plateforme de souscription, de tarification ou de décision opérationnelle.
- Ne pas traiter de données personnelles.
- Ne pas prétendre que le portefeuille automobile externe représente le Togo, la CIMA ou un assureur particulier.
- Ne pas offrir de requête SQL libre.
- Ne pas permettre de modifier le résultat canonique ou son historique.
- Ne pas utiliser le déploiement Vercel vivant comme seule archive scientifique.

## 3. Méthode d’inventaire de l’existant

L’inventaire repose sur quatre sources complémentaires:

1. inspection visuelle et fonctionnelle du déploiement public;
2. lecture du code TypeScript, Python, CSS, des configurations et de la documentation;
3. interrogation en lecture seule des routes API publiques;
4. comparaison de la réponse publique du moteur avec l’état du code local.

Les captures réalisées pendant l’audit sont conservées dans `audit_existing_app/screenshots/`.

## 4. Inventaire de l’application existante

### 4.1 État du dépôt et du déploiement

| Élément | État constaté |
|---|---|
| Dépôt actuel | `BAT-El34/actuarial_digital_dashboard_rd` |
| Branche locale | `main` |
| Commit de base local | `b3df670227efa4aecf5383979b90f3eab15ae528` |
| Version déclarée | 2.1.0 |
| Frontend | TypeScript compilé en JavaScript, SPA à routes par hash |
| Backend | FastAPI dans une fonction Python Vercel |
| Magasin analytique local | SQLite, environ 205 Mo |
| Données embarquées dans le magasin | 8 ressources, environ 1,22 million de lignes cumulées |
| API publique | Disponible, santé `ok`, version 2.1.0, magasin de données disponible |
| État Git local | Modifications non commitées dans le moteur ARCCRAFT, le service de modèle, les tests et `.gitignore` |
| Correspondance public et local | Partielle, les sorties de stress inverse divergent |

### 4.2 Inventaire des écrans

| Écran existant | Route actuelle | Fonctions principales | Données utilisées | Santé générale | Décision pour la nouvelle application |
|---|---|---|---|---|---|
| Accueil intégré | `#/home` | Présentation de la chaîne MAPTA, COMPASS, ARCCRAFT, statuts et pré-pilote | Résultats embarqués | Bonne structure, mais hors périmètre et présence de duplications visuelles | Ne pas reprendre le contenu, reprendre la grammaire éditoriale |
| MAPTA | `#/mapta` | Simulation de fit, distributions, rang, portes, readiness, comparaison par paires | Moteur MAPTA synthétique | Fonctionnel, mais hors sujet du paper | Exclure du nouveau produit |
| COMPASS | `#/compass` | Questionnaire, recommandation, abstention, sous-scores, variables interdites | Moteur COMPASS synthétique | Fonctionnel, mais hors sujet du paper | Exclure du nouveau produit |
| ARCCRAFT | `#/arccraft` | Simulation procédurale, classes, Failure Atlas, stress inverse, corrélations, validation automobile | Moteur synthétique, résultats embarqués, portefeuille automobile externe | Pertinent, mais mélange valeurs illustratives et sorties backend | Reconcevoir comme noyau du nouveau produit |
| Données | `#/data` | Catalogue, recherche de séries, courbes, requêtes tabulaires contrôlées, agrégats automobiles | SQLite analytique et API whitelistée | Fonctionnel, riche, trop large pour le paper | Réduire aux données et résultats du paper |
| Méthode | `#/methode` | Statuts de preuve, contrats de sortie, garde-fous, KPI et règles d’arrêt | Contenu éditorial embarqué | Bonne base de gouvernance, contenu trop transversal | Reprendre et spécialiser pour ARCCRAFT |
| Anglais | État local de l’interface | Traduction de la vue courante sans changement de route | Dictionnaire TypeScript | Fonctionnel | Reprendre avec routes propres `/en` et `/fr` |
| Mode sombre | État local de l’interface | Bascule jour et nuit mémorisée | `localStorage` | Fonctionnel et cohérent | Reprendre |

### 4.3 Captures de référence

| Étape | Capture | Observation principale |
|---:|---|---|
| 1 | [Accueil français, mode clair](audit_existing_app/screenshots/01-home-fr-light.png) | Identité éditoriale forte, navigation compacte, contenu multi-projet à isoler |
| 2 | [ARCCRAFT français, mode clair](audit_existing_app/screenshots/02-arccraft-fr-light.png) | Bon inventaire fonctionnel, mais ambiguïté entre données embarquées, projection illustrative et calcul live |
| 3 | [Catalogue de données](audit_existing_app/screenshots/03-data-fr-light.png) | Provenance et statuts visibles, volume fonctionnel supérieur au besoin du paper |
| 4 | [Méthode et gouvernance](audit_existing_app/screenshots/04-method-fr-light.png) | Bonne pédagogie des statuts et portes, duplications visibles dans le rendu long |
| 5 | [ARCCRAFT anglais, mode sombre](audit_existing_app/screenshots/05-arccraft-en-dark.png) | Bilingue et thème sombre opérationnels |
| 6 | [MAPTA](audit_existing_app/screenshots/06-mapta-current-theme.png) | Référence de mise en page uniquement |
| 7 | [COMPASS](audit_existing_app/screenshots/07-compass-current-theme.png) | Référence de formulaires et d’explicabilité uniquement |

### 4.4 Fonctions ARCCRAFT actuellement disponibles

#### Console synthétique

- Choix visuel d’une classe de scénario.
- Curseur de perturbation illustrative de 0 à 50.
- Choix du nombre de mondes, entre 100 et 20 000 côté API.
- Choix d’une seed.
- Lancement du moteur Python.
- Affichage des comptes PASS, REPAIR et REJECT.
- Affichage des taux d’échec par classe.
- Affichage des variables les plus associées au ratio combiné.
- Affichage du stress inverse le plus proche trouvé.
- Affichage du statut de readiness.

Limite importante: le choix de classe et le curseur de perturbation alimentent une projection illustrative côté interface. L’appel backend `/api/arccraft/simulate` ne reçoit actuellement que `n_worlds` et `seed`. La nouvelle application devra supprimer cette ambiguïté. Tout contrôle visible devra soit modifier effectivement l’expérience exécutée, soit être explicitement présenté comme une visualisation pédagogique non exécutée.

#### Validation automobile externe

- Calibration sur 2022 et 2023.
- Projection sur 2024.
- Choix du nombre de simulations.
- Multiplicateurs de fréquence et de sévérité.
- Affichage des moyennes, quantiles, erreurs et couverture d’intervalle.
- Mention explicite du caractère expérimental et non transférable.

#### Data Lab

- Catalogue de sources avec type, statut, volume, périmètre et note.
- Recherche de séries pour FAS, WDI, Findex et GFD.
- Sélection de géographies et période.
- Courbe générée depuis les observations du backend.
- Requête tabulaire sur champs et opérateurs whitelistés.
- Agrégats automobiles annuels.

### 4.5 Inventaire des API existantes

| Méthode | Route | Fonction | Décision cible |
|---|---|---|---|
| GET | `/api/health` | Santé et version API | Reprendre et enrichir avec commit et release |
| GET | `/api/data/catalog` | Catalogue de données | Reprendre sous forme limitée aux artefacts du paper |
| GET | `/api/data/fields/{dataset}` | Champs autorisés | Optionnel |
| POST | `/api/data/query` | Requête tabulaire whitelistée | Reprendre uniquement si nécessaire |
| GET | `/api/data/series/search` | Recherche de séries | Ne pas reprendre dans le MVP |
| GET | `/api/data/series` | Séries temporelles externes | Ne pas reprendre dans le MVP |
| GET | `/api/benchmark/summary` | Résumé benchmark Togo | Exclure |
| GET | `/api/motor/summary/year` | Agrégats annuels automobile | Reprendre en artefact statique ou endpoint léger |
| GET | `/api/motor/summary/segment` | Agrégats par segment | P1, avec contrôle de divulgation |
| GET | `/api/motor/calibration` | Paramètres de calibration | Reprendre avec version et checksum |
| POST | `/api/mapta/simulate` | Simulation MAPTA | Exclure |
| POST | `/api/compass/recommend` | Recommandation COMPASS | Exclure |
| POST | `/api/arccraft/simulate` | Simulation synthétique | Reprendre après alignement scientifique |
| POST | `/api/arccraft/motor-stress` | Simulation fréquence-sévérité | Reprendre avec paramètres figés et manifestes |

### 4.6 Données existantes

| Ressource | Lignes | Statut actuel | Utilité pour le nouveau produit |
|---|---:|---|---|
| Benchmark assurance Togo v26 | 200 | USER_UPLOAD, DOCUMENTARY_EVIDENCE | Exclure |
| Portefeuille automobile public | 354 140 | PUBLIC_EXTERNAL, EXTERNAL_VALIDATION | Conserver comme source empirique principale |
| IMF FAS | 19 256 | PUBLIC_EXTERNAL | Exclure du MVP |
| World Development Indicators | 764 129 | PUBLIC_EXTERNAL | Exclure du MVP |
| Global Findex | 8 702 | PUBLIC_EXTERNAL | Exclure du MVP |
| Global Financial Development | 17 180 | PUBLIC_EXTERNAL | Exclure du MVP |
| GSMA Mobile Money | 58 975 | PUBLIC_EXTERNAL | Exclure du MVP |
| Mobile Money Prevalence Index | 618 | PUBLIC_EXTERNAL | Exclure du MVP |

Le fichier SQLite de 205 217 792 octets ne doit pas être transféré tel quel dans la nouvelle fonction scientifique. Le nouveau produit doit versionner les résultats dérivés nécessaires au paper et pointer vers une archive pérenne pour les données redistribuables. Cette séparation réduit le bundle, évite une dépendance inutile aux sources hors périmètre et facilite le contrôle des versions.

### 4.7 Architecture existante

```text
Navigateur TypeScript
        |
        v
API FastAPI sur Vercel
        |
        +--> SQLite analytique
        |
        +--> Moteurs MAPTA, COMPASS et ARCCRAFT
        |
        v
JSON versionné, graphiques et tableaux
```

Points forts:

- séparation frontend et moteur Python;
- validation Pydantic des paramètres;
- champs et opérateurs de données whitelistés;
- absence de requête SQL libre;
- fichiers sensibles non exposés comme statiques;
- schémas de sortie identifiés;
- tests de compilation, design, backend et données;
- garde-fous visibles dans l’interface.

Points à renforcer:

- absence d’un commit et d’une release visibles dans chaque réponse;
- absence d’une archive scientifique citée comme autorité;
- mélange de résultats embarqués, de projections illustratives et de sorties calculées;
- SPA par hash, moins adaptée à l’indexation, aux citations stables et au partage de pages;
- base trop large pour le périmètre scientifique du paper;
- absence de téléchargement direct d’un manifeste complet de chaque run;
- absence de correspondance obligatoire entre figures, métriques, fichiers et versions;
- absence de tests E2E navigateur revendiqués dans la documentation existante;
- duplications visibles de blocs dans les captures longues;
- divergence entre le backend public et l’état local actuel.

### 4.8 Vérification publique réalisée

Le 25 septembre 2026:

- `/api/health` retourne `status=ok`, `api_version=2.1.0` et `data_store=true`;
- le catalogue retourne les huit ressources attendues;
- une simulation de 100 mondes avec seed 20260825 termine en environ 3,58 secondes;
- le stress inverse public retourne `world_id_perturbation=184` et une distance standardisée de `0.9534068136`;
- le code local actuel retourne, avec les mêmes paramètres, `world_id_perturbation=196` et une distance standardisée de `1.0123246493`.

Cette divergence interdit de présenter le déploiement actuel comme la source exacte des résultats du paper.

### 4.9 Matrice de décision

| Élément | Reprendre | Isoler | Renforcer | Supprimer |
|---|:---:|:---:|:---:|:---:|
| Direction artistique éditoriale | Oui |  | Oui |  |
| Mode clair et sombre | Oui |  | Oui |  |
| Anglais et français | Oui |  | Oui |  |
| Navigation par hash |  |  |  | Oui |
| Pages MAPTA et COMPASS |  | Oui |  | Oui du nouveau dépôt |
| Moteur ARCCRAFT Python | Oui | Oui | Oui |  |
| Portefeuille automobile | Oui | Oui | Oui |  |
| Données FAS, WDI, Findex, GFD, GSMA et MMPI |  | Oui |  | Oui du MVP |
| SQLite généraliste de 205 Mo |  | Oui |  | Oui du runtime Vercel |
| Résultats embarqués | Oui pour fallback | Oui | Oui, étiquetage obligatoire |  |
| Projection illustrative |  | Oui | Oui, séparation explicite |  |
| Failure Atlas | Oui | Oui | Oui |  |
| Stress inverse | Oui | Oui | Oui |  |
| API whitelistée | Oui | Oui | Oui |  |
| Statuts de preuve | Oui | Oui | Oui |  |
| Garde-fous d’inférence | Oui | Oui | Oui |  |
| Blocs dupliqués au rendu |  |  |  | Oui |

## 5. Positionnement du nouveau produit

### 5.1 Proposition de valeur

Le produit permet de lire, vérifier, rejouer et citer le paper ARCCRAFT depuis une interface unique, tout en maintenant une frontière explicite entre résultat publié, replay computationnel, exploration utilisateur et validation empirique.

### 5.2 Publics cibles

| Public | Besoin principal |
|---|---|
| Reviewer académique | Vérifier les claims, les métriques, les données et les limites |
| Chercheur en actuariat | Reproduire les runs, inspecter les hypothèses et télécharger le code |
| Actuaire praticien | Comprendre les stress, les portes et les régions de vulnérabilité |
| Spécialiste de reproductibilité | Vérifier commit, versions, seeds, checksums et sorties |
| Lecteur non technique | Comprendre la contribution sans exécuter de code |

### 5.3 Principes scientifiques non négociables

1. Toute valeur numérique affichée doit avoir une source, une version et un statut.
2. Une sortie issue du navigateur ne doit jamais être présentée comme le résultat publié si son environnement ou son code diffère de la release citée.
3. Les résultats synthétiques, externes et dérivés doivent être visuellement et sémantiquement distincts.
4. La reproductibilité computationnelle ne doit pas être décrite comme une validation prédictive.
5. Une observation au-dessus du quantile 97,5 ne doit pas être transformée en validation complète.
6. Les métriques de discrimination, calibration agrégée, calibration par groupes et couverture d’intervalle doivent rester séparées.
7. Le Failure Atlas démontre actuellement la traçabilité et le replay des échecs, pas l’exactitude diagnostique ni l’attribution causale.
8. Les explorations personnalisées ne modifient jamais les artefacts canoniques.

## 6. Architecture de l’information cible

### 6.1 Routes publiques

| Route anglaise | Route française | Contenu |
|---|---|---|
| `/en` | `/fr` | Accueil scientifique |
| `/en/paper` | `/fr/article` | Résumé structuré, PDF, citation, sections du paper |
| `/en/evidence` | `/fr/preuves` | Claims, métriques, tables, figures et verdicts |
| `/en/figures` | `/fr/figures` | Galerie des figures 1 à 7 et provenance |
| `/en/lab` | `/fr/laboratoire` | Replay canonique et explorations |
| `/en/failure-atlas` | `/fr/failure-atlas` | Échecs, portes, seeds et filtres |
| `/en/data` | `/fr/donnees` | Catalogue scientifique, licences, empreintes et téléchargements |
| `/en/reproducibility` | `/fr/reproductibilite` | Release, commit, environnement, manifestes et procédures |
| `/en/limitations` | `/fr/limites` | Limites, menaces à la validité et interprétation autorisée |
| `/en/cite` | `/fr/citer` | Citations du paper, du logiciel et des données |
| `/api/v1/health` | Identique | Santé et identité de build |
| `/api/v1/runs/canonical` | Identique | Métadonnées du run publié |
| `/api/v1/simulate/synthetic` | Identique | Simulation procédurale contrôlée |
| `/api/v1/simulate/motor` | Identique | Expérience fréquence-sévérité contrôlée |
| `/api/v1/artifacts/{id}` | Identique | Métadonnées d’artefact et checksum |

### 6.2 Parcours principaux

#### Parcours A, reviewer

1. Ouvrir l’accueil.
2. Lire la contribution et le verdict empirique.
3. Ouvrir la matrice claim-métrique.
4. Cliquer une métrique pour accéder à la figure, la table et le CSV source.
5. Vérifier la version du code et le checksum.
6. Télécharger le paquet de réplication.

#### Parcours B, reproducteur

1. Ouvrir la page Reproducibility.
2. Vérifier release, commit, versions et environnement.
3. Lancer le replay canonique.
4. Comparer l’empreinte du résultat au résultat publié.
5. Télécharger le manifeste du run et les sorties.
6. Accéder à la release GitHub et à l’archive DOI.

#### Parcours C, explorateur actuariel

1. Ouvrir le laboratoire.
2. Choisir le mode Exploration, distinct du mode Canonical replay.
3. Modifier les paramètres autorisés.
4. Exécuter le run.
5. Inspecter les classes, le Failure Atlas, le stress inverse et les avertissements.
6. Télécharger le manifeste de l’exploration avec le statut `EXPLORATORY`.

## 7. Spécification des écrans

### 7.1 Accueil scientifique

Contenu obligatoire:

- titre complet du paper;
- auteurs;
- abstract anglais;
- résumé français distinct, identifié comme traduction;
- statut de la publication;
- trois résultats clés, avec unités et limites;
- accès direct au PDF, au laboratoire, aux données et à la citation;
- badge indiquant la release scientifique active;
- mention que le résultat externe est partiel et que l’observation dépasse le quantile prédictif 97,5;
- encadré de séparation entre `PUBLISHED RESULT`, `LIVE REPLAY` et `USER EXPLORATION`.

### 7.2 Paper

- PDF lisible dans le navigateur et téléchargeable.
- Sommaire navigable.
- HTML accessible des sections ou résumé structuré si la conversion complète n’est pas retenue.
- Liens bidirectionnels entre texte, figures, tables, références et artefacts.
- Métadonnées bibliographiques exportables en BibTeX et RIS.
- Aucun auteur masqué sur le site, même si la maquette PDF actuelle suit une règle éditoriale différente.

### 7.3 Evidence

La page doit reprendre le registre claim-métrique du paper.

| Claim | Métrique obligatoire | Résultat publié | Limite affichée |
|---|---|---|---|
| Le modèle de fréquence individuel améliore la discrimination | Réduction relative de déviance | 7,19 % en 2023, 8,99 % en 2024 | Ne prouve pas la calibration agrégée |
| Les intervalles prédictifs sont insuffisamment calibrés | Résultats dans l’intervalle 95 | 3 sur 12, dont 0 sur 6 pour les charges | Deux origines temporelles seulement |
| Les runs enregistrés se rejouent exactement | Empreintes identiques | 15 sur 15 | Vérification computationnelle locale |
| Les flux nommés isolent les tirages non pertinents | Réponse à 100 tirages monde inutilisés | Inchangé avec flux nommés, changé avec flux partagé | Une intervention enregistrée |
| Le validateur change la population sélectionnée | Différence du mode strict | 19,87 % de mondes acceptés en moins, 13,43 points de failure-or-rejection en plus | Effet de sélection et de reporting |
| Les transitions ont un faible effet observé | Différence de taux d’échec | moins 0,247 point, moins 0,69 % relatif | Résultat descriptif sur trois seeds |
| Le Failure Atlas est dominé par la traçabilité | Part des échecs simulés | 3 588 sur 3 589, soit 99,97 % | Ne prouve pas l’exactitude diagnostique |
| Le benchmark de temps est bruité | Moyenne, écart-type et coefficient de variation | 3,59 s, 1,05 s, 29,09 | Dépend de la machine |

Chaque ligne doit ouvrir une fiche détaillée avec définition, formule, unité, provenance, fichier, figure, période, population, version et interprétation autorisée.

### 7.4 Galerie des figures

Les figures 1 à 7 sont des artefacts scientifiques. La figure 8 actuelle, qui pointe vers l’ancien démonstrateur, doit être remplacée dans une future version du paper par un QR code vers la nouvelle application.

| Figure | Titre fonctionnel | Source principale |
|---:|---|---|
| 1 | Architecture procédurale et frontières de preuve | Spécification ARCCRAFT |
| 2 | Échelle du portefeuille, dynamiques et composition | Profils de données 2022 à 2024 |
| 3 | Performance des comparateurs temporels | Résultats de benchmark |
| 4 | Calibration par décile et couverture d’intervalle | Calibration et diagnostics |
| 5 | Surface de stress fréquence-sévérité | Résultats de stress |
| 6 | Taux d’échec et composition du Failure Atlas | Run canonique |
| 7 | Ablations, coût et isolation des flux | Résultats d’ablation |

Chaque figure doit proposer:

- image haute résolution;
- caption complète;
- texte alternatif;
- données CSV de la figure;
- script de génération;
- checksum du PNG et du script;
- référence à la release et au commit;
- bouton `Open evidence`.

### 7.5 Laboratoire

Trois modes obligatoires:

1. `CANONICAL REPLAY`, paramètres verrouillés, reproduction du run publié;
2. `REGISTERED VARIANT`, configurations d’ablation définies dans le paper;
3. `EXPLORATORY`, paramètres utilisateur, résultat non publiable par défaut.

Contrôles synthétiques:

- seed maître;
- nombre de mondes;
- politique du validateur;
- transitions activées ou non;
- architecture de flux nommés ou partagés;
- classes de scénario réellement exécutées;
- export du manifeste.

Contrôles automobile:

- période de calibration verrouillée par défaut sur 2022 et 2023;
- année de projection verrouillée par défaut sur 2024;
- seed;
- nombre de simulations;
- multiplicateur de fréquence;
- multiplicateur de sévérité;
- frais et commissions uniquement s’ils sont explicitement renseignés comme hypothèses;
- aucun recalibrage silencieux sur 2024.

Le résultat doit toujours afficher:

- statut du run;
- environnement;
- durée;
- release et commit;
- versions du moteur, de la grammaire, de la calibration, du produit et du schéma;
- registre de seeds et sous-flux;
- checksum d’entrée;
- checksum de sortie;
- avertissements scientifiques;
- bouton de téléchargement JSON et CSV.

### 7.6 Failure Atlas

- Tableau filtrable par monde, régime, classe, statut du validateur, porte, seed et run.
- Inclusion des échecs simulés et des rejets structurels.
- Valeurs non définies représentées par `null`, jamais `NaN` dans le JSON.
- Lien de replay vers le monde ou le run.
- Résumé par porte et classe.
- Affichage logarithmique lorsque nécessaire.
- Avertissement permanent sur l’absence actuelle de vérité terrain diagnostique.
- Export CSV et JSON.
- P1: chronologie du premier échec lorsque l’instrumentation le permettra.

### 7.7 Données et provenance

- Catalogue limité aux sources réellement utilisées par le paper.
- Statut de chaque ressource: `PUBLIC_EXTERNAL`, `DERIVED_RESULT`, `SYNTHETIC`, `AUTHORED_ARTIFACT`.
- Institution, titre, version, période, licence, accès, checksum et transformations.
- Téléchargement direct lorsque la redistribution est autorisée.
- Lien vers l’institution ou l’archive lorsque la redistribution n’est pas autorisée.
- Dictionnaire des variables du portefeuille.
- Diagramme de transformation depuis la source brute vers les tableaux et figures.
- Aucune donnée manquante imputée silencieusement.

### 7.8 Reproductibilité

- Release scientifique active.
- Commit SHA complet.
- Date de build.
- Version de Python, de NumPy et des dépendances critiques.
- Système d’exploitation et architecture du run canonique.
- Instructions locales, Docker et notebook si disponibles.
- Paquet de réplication.
- Checksums.
- Tableau des tests et résultats.
- Différence éventuelle entre le runtime web et le runtime canonique.
- Lien vers la release GitHub immuable.
- Lien vers l’archive DOI.

### 7.9 Limites

La page doit rendre visibles au minimum:

- validation externe partielle;
- sous-couverture des queues;
- nombre limité d’origines temporelles;
- proxy de dispersion de sévérité construit sur des moyennes police-année;
- absence de frais et commissions calibrés dans le portefeuille;
- non-transférabilité au Togo et à la CIMA;
- domination du Failure Atlas par la porte de traçabilité;
- absence actuelle de précision, rappel, délai de détection et attribution causale;
- timings dépendants du matériel.

### 7.10 Citer

- Citation du paper.
- Citation du logiciel.
- Citation du dataset ou de l’archive.
- Export BibTeX, RIS et texte.
- `CITATION.cff` présent à la racine du dépôt.
- ORCID ajoutés lorsque les auteurs les fourniront.
- DOI ajouté après archivage.

## 8. Exigences fonctionnelles

Priorités: P0 obligatoire pour publication, P1 souhaitée pour la première version complète, P2 évolution.

| ID | Priorité | Exigence | Critère d’acceptation |
|---|---|---|---|
| FR-001 | P0 | L’application est exclusivement consacrée à ARCCRAFT | Aucun écran MAPTA ou COMPASS dans le dépôt cible |
| FR-002 | P0 | L’anglais est la langue par défaut | Une première visite ouvre `/en` |
| FR-003 | P0 | Toutes les pages existent en anglais et français | Parité de contenu vérifiée par test |
| FR-004 | P0 | Mode clair et sombre | Préférence persistante et contraste conforme |
| FR-005 | P0 | PDF du paper téléchargeable | Fichier versionné, checksum visible |
| FR-006 | P0 | Chaque claim quantitatif est lié à une métrique | Les huit claims du registre disposent d’une fiche |
| FR-007 | P0 | Chaque figure est liée à ses données et son script | Figures 1 à 7 complètes |
| FR-008 | P0 | Replay canonique | Paramètres verrouillés, empreinte comparée |
| FR-009 | P0 | Exploration distincte | Badge `EXPLORATORY` permanent |
| FR-010 | P0 | Manifeste téléchargeable pour chaque run | JSON valide et complet |
| FR-011 | P0 | Failure Atlas filtrable | Filtres et export fonctionnels |
| FR-012 | P0 | Version complète affichée | Release, commit, moteur, grammaire, schéma et données visibles |
| FR-013 | P0 | Catalogue de données spécifique au paper | Aucune source hors périmètre dans le MVP |
| FR-014 | P0 | Citation machine-readable | `CITATION.cff` valide |
| FR-015 | P0 | Archive DOI | DOI visible avant soumission finale ou statut clairement indiqué |
| FR-016 | P0 | Health endpoint enrichi | Identité de build complète retournée |
| FR-017 | P0 | Résultats canoniques immuables | Le frontend ne peut pas les écraser |
| FR-018 | P0 | Avertissements scientifiques | Présents sur toutes les sorties concernées |
| FR-019 | P0 | Liens propres | Aucun routage par hash |
| FR-020 | P0 | Téléchargements contrôlés | Licence et checksum visibles avant ou avec le téléchargement |
| FR-021 | P1 | Comparateur run publié contre run utilisateur | Différences de métriques explicites |
| FR-022 | P1 | Export d’un run en archive ZIP | JSON, CSV, manifeste et README inclus |
| FR-023 | P1 | Vue détaillée d’un monde | Variables, états, portes et résultat |
| FR-024 | P1 | Partage d’un run | URL stable ne contenant aucune donnée sensible |
| FR-025 | P1 | API documentée | OpenAPI accessible et versionnée |
| FR-026 | P1 | Dictionnaire de données interactif | Recherche et définitions disponibles |
| FR-027 | P2 | File de calcul asynchrone | Reprise des runs plus longs avec identifiant |
| FR-028 | P2 | Comparaison de releases | Diff des métriques, schémas et paramètres |
| FR-029 | P2 | Fault injection contrôlée | Métriques de détection et attribution possibles |

## 9. Modèle de données scientifique

### 9.1 Manifeste d’artefact

Chaque artefact doit avoir au minimum:

```json
{
  "artifact_id": "figure-6",
  "artifact_type": "figure",
  "title": "Scenario class failure rates and Failure Atlas composition",
  "release": "v1.0.0-paper",
  "commit_sha": "FULL_SHA",
  "created_at": "ISO_8601",
  "content_sha256": "SHA256",
  "source_files": [],
  "data_status": "DERIVED_RESULT",
  "license": "TO_BE_CONFIRMED",
  "paper_references": ["Figure 6", "Section 4.3"],
  "limitations": []
}
```

### 9.2 Manifeste de run

```json
{
  "run_id": "UUID",
  "run_status": "CANONICAL_REPLAY",
  "release": "v1.0.0-paper",
  "commit_sha": "FULL_SHA",
  "schema_version": "arccraft-output-1.0",
  "engine_version": "0.1.0",
  "world_grammar_version": "world_grammar-0.1.0",
  "calibration_version": "SCENARIO_ASSUMPTION",
  "master_seed": 20260825,
  "named_streams": {
    "world": {"algorithm": "PCG64", "spawn_key": [0]},
    "claims": {"algorithm": "PCG64", "spawn_key": [1]},
    "behaviour": {"algorithm": "PCG64", "spawn_key": [2]}
  },
  "parameters": {},
  "input_sha256": "SHA256",
  "output_sha256": "SHA256",
  "runtime": {},
  "warnings": []
}
```

### 9.3 Artefacts à intégrer depuis le dossier de recherche

P0:

- `31_ARCCRAFT_FULL_MANUSCRIPT.md`;
- PDF final compilé;
- `references.bib`;
- figures 1 à 7;
- scripts de figures;
- `19_POLICY_BENCHMARK_RESULTS.csv`;
- `20_POLICY_DECILE_CALIBRATION.csv`;
- `21_POLICY_MODEL_DIAGNOSTICS.csv`;
- `22_NUMERIC_PROFILE.csv`;
- `23_CATEGORY_PROFILE.csv`;
- `24_TEMPORAL_CATEGORY_SHIFT.csv`;
- `25_ARCCRAFT_ABLATION_RESULTS.csv`;
- `26_ARCCRAFT_ABLATION_SUMMARY.csv`;
- `27_STREAM_ISOLATION_TEST.csv`;
- `32_CLAIM_METRIC_AUDIT.csv`;
- moteur ARCCRAFT figé;
- script d’ablation;
- notebooks de benchmark;
- fichier d’environnement verrouillé;
- manifestes et checksums.

P1:

- données agrégées de la surface de stress;
- Failure Atlas complet du run canonique;
- paquet de replay local;
- image de conteneur ou recette Docker reproductible.

### 9.4 Politique de stockage

| Type | GitHub | Vercel | Archive DOI |
|---|---|---|---|
| Code source | Oui | Build déployé | Oui |
| Petits CSV dérivés | Oui | Oui, statiques | Oui |
| Figures | Oui | Oui | Oui |
| PDF | Oui ou release | Oui | Oui |
| Dataset automobile brut | Selon licence et taille, pas dans l’historique Git standard | Non | Oui si redistribution autorisée, sinon lien et checksum |
| SQLite généraliste de 205 Mo | Non | Non | Non nécessaire au paper |
| Failure Atlas complet | Release ou archive | Lecture optimisée | Oui |
| Manifestes et checksums | Oui | Oui | Oui |

## 10. Architecture technique cible

### 10.1 Choix recommandé

- Frontend: application TypeScript avec rendu statique ou hybride, routes propres et métadonnées SEO.
- Framework recommandé: Next.js avec App Router, version explicitement figée dans le lockfile.
- Backend scientifique: Python et FastAPI dans une fonction Vercel dédiée.
- Moteur: module Python pur, sans dépendance au frontend.
- Résultats publiés: JSON et CSV statiques versionnés.
- Données lourdes: archive DOI ou stockage externe en lecture seule.
- Observabilité: logs structurés sans données personnelles.
- CI: GitHub Actions.
- Déploiement: intégration GitHub vers un projet Vercel dédié.

Le runtime Python de Vercel prend officiellement en charge FastAPI. La documentation actuelle impose également de contrôler précisément les fichiers inclus dans le bundle Python. Le cahier des charges retient donc un backend scientifique minimal et exclut le magasin SQLite généraliste du bundle.

### 10.2 Schéma cible

```text
Lecteur
  |
  v
Application web bilingue
  |              |
  |              +--> Artefacts statiques versionnés
  |                   PDF, figures, CSV, manifestes
  |
  +--> API /api/v1
         |
         +--> Moteur ARCCRAFT figé
         |
         +--> Calibration compacte versionnée
         |
         +--> Génération du manifeste et des empreintes

GitHub release immuable <--> Archive DOI
          |
          +--> source d’autorité citée par l’application
```

### 10.3 Arborescence proposée

```text
arccraft-research-companion/
  app/
    [locale]/
      page.tsx
      paper/
      evidence/
      figures/
      lab/
      failure-atlas/
      data/
      reproducibility/
      limitations/
      cite/
  api/
    index.py
  arccraft/
    engine.py
    schemas.py
    calibration/
    canonical/
  artifacts/
    figures/
    results/
    manifests/
    paper/
  public/
    downloads/
  tests/
    unit/
    contract/
    e2e/
    visual/
    reproducibility/
  scripts/
    build_artifacts.py
    verify_checksums.py
    verify_canonical_run.py
  .github/
    workflows/
  CITATION.cff
  LICENSE
  LICENSES_DATA.md
  README.md
  REPRODUCIBILITY.md
  SECURITY.md
  pyproject.toml
  uv.lock
  package.json
  package-lock.json
  vercel.json
```

### 10.4 Contrat de l’endpoint santé

```json
{
  "status": "ok",
  "api_version": "1.0.0",
  "release": "v1.0.0-paper",
  "commit_sha": "FULL_SHA",
  "build_time": "ISO_8601",
  "engine_version": "0.1.0",
  "world_grammar_version": "world_grammar-0.1.0",
  "schema_version": "arccraft-output-1.0",
  "artifact_manifest_sha256": "SHA256",
  "canonical_run_available": true
}
```

### 10.5 Limites d’exécution

- Bornes serveur sur tous les paramètres.
- Taille maximale d’un run web définie après benchmark du projet Vercel cible.
- Aucun run web ne doit menacer la disponibilité de l’application.
- Le run canonique peut être servi depuis un artefact pré-calculé et vérifié, avec option de replay live séparée.
- Les runs longs doivent être refusés proprement ou dirigés vers la procédure locale.
- Un timeout ne doit jamais afficher un ancien résultat comme s’il s’agissait du run demandé.
- Les limites de durée et de bundle doivent être contrôlées dans la CI à partir des contraintes Vercel applicables au plan retenu.

## 11. Dépôt GitHub distinct

### 11.1 Création

- Créer un nouveau dépôt public, sans historique du dépôt intégré.
- Nom recommandé: `arccraft-research-companion`.
- Description: `Reproducible research companion for the ARCCRAFT procedural actuarial stress-testing paper`.
- Ajouter les topics: `actuarial-science`, `stress-testing`, `reproducibility`, `monte-carlo`, `insurance`, `research-software`.
- Ajouter les auteurs comme collaborateurs selon les rôles convenus.
- Ne pas utiliser le dépôt actuel comme remote de production.

### 11.2 Stratégie Git

- `main`: branche protégée et déployable.
- branches courtes par fonctionnalité.
- pull request obligatoire.
- CI verte obligatoire avant merge.
- revue obligatoire pour les changements de moteur, de données ou de claims.
- commits signés recommandés.
- tags sémantiques.
- release paper initiale proposée: `v1.0.0-paper`.

### 11.3 Release scientifique

La release doit contenir:

- archive du code;
- PDF du paper;
- paquet de réplication;
- manifestes;
- checksums;
- résultats canoniques;
- figures et scripts;
- notes de release;
- SBOM si disponible;
- attestation de provenance de build.

GitHub permet de rendre une release immuable, ce qui verrouille son tag et ses assets. Cette option doit être activée avant la release scientifique finale. La release doit d’abord être préparée en brouillon avec tous les assets, puis publiée.

### 11.4 Citation et archivage

- Ajouter `CITATION.cff` à la racine.
- Utiliser la citation du paper comme `preferred-citation` lorsque les métadonnées de publication seront connues.
- Connecter le dépôt à Zenodo ou à une archive équivalente.
- Réserver le DOI si nécessaire avant la dernière compilation du paper.
- Archiver la release GitHub.
- Ajouter le DOI dans `CITATION.cff`, le README, l’application et le paper.
- Conserver un DOI de concept et un DOI de version lorsque la plateforme d’archive le fournit.

## 12. Projet Vercel distinct

### 12.1 Isolation obligatoire

- Créer un nouveau projet Vercel.
- Connecter uniquement le nouveau dépôt.
- Utiliser un nom, un domaine, des variables et un historique de déploiement distincts.
- Ne pas réutiliser le projet `actuarial-digital-dashboard-rd-v3`.
- Ne pas réutiliser une base ou un backend dont la version n’est pas contrôlée par le nouveau dépôt.

### 12.2 Environnements

| Environnement | Branche | Usage | Données |
|---|---|---|---|
| Preview | Pull request | Revue fonctionnelle et visuelle | Artefacts de test |
| Staging | Branche de préparation ou alias | Validation prépublication | Artefacts candidats |
| Production | `main` et tag validé | Publication publique | Artefacts de release |

### 12.3 Variables d’environnement

Variables publiques autorisées:

- `NEXT_PUBLIC_RELEASE_TAG`;
- `NEXT_PUBLIC_COMMIT_SHA`;
- `NEXT_PUBLIC_ARCHIVE_DOI`;
- `NEXT_PUBLIC_PAPER_URL`;
- `NEXT_PUBLIC_GITHUB_REPOSITORY`.

Variables serveur possibles:

- stockage externe en lecture seule;
- token d’observabilité si retenu;
- limite de calcul et rate limit.

Aucune clé secrète ne doit être accessible au navigateur. Le produit ne nécessite pas d’authentification pour le MVP.

## 13. Design et expérience utilisateur

### 13.1 Éléments à reprendre

- esthétique éditoriale scientifique;
- grands titres serif;
- corps sans serif;
- métadonnées monospace;
- accent cobalt unique;
- surfaces mates;
- absence de gradients et d’ombres décoratives;
- mode clair papier;
- mode sombre charbon prune;
- navigation compacte;
- statut, provenance et limites visibles.

### 13.2 Palette de référence

| Usage | Sombre | Clair |
|---|---|---|
| Fond | `#18141F` | `#F4F1EA` |
| Panneau | `#221C2B` | `#FFFDF8` ou `#EEE9E2` |
| Texte principal | `#F1EAE0` | `#211B28` |
| Texte secondaire | `#A79E92` | `#655D58` |
| Accent | `#4A5CD8` | `#4A5CD8` |

### 13.3 Règles de contenu visuel

- Une couleur ne doit jamais être le seul moyen de transmettre un statut.
- Chaque graphique doit avoir un titre, des axes, des unités, une source, une période et un texte alternatif.
- Les données publiées, recalculées et exploratoires doivent avoir des styles distincts.
- Aucun résultat ne doit apparaître avant la fin effective de son calcul.
- Les erreurs API doivent produire un état explicite, sans fallback trompeur.
- Les duplications de blocs observées doivent être couvertes par des tests de régression visuelle.
- Les polices doivent être correctement licenciées et idéalement auto-hébergées.

### 13.4 Responsive

- Desktop: lecture en grille et comparaisons multi-panneaux.
- Tablette: colonnes réduites sans perte de labels.
- Mobile: contenu linéaire, tables scrollables avec annonce accessible, graphiques adaptés.
- Largeur minimale testée: 320 px.
- Zoom à 200 sans perte d’information ni chevauchement.

## 14. Accessibilité

Objectif: WCAG 2.2 niveau AA.

Exigences:

- structure sémantique cohérente;
- un seul `h1` par page;
- ordre de titres sans saut arbitraire;
- navigation clavier complète;
- focus visible;
- lien d’évitement;
- labels reliés aux contrôles;
- messages de chargement et d’erreur annoncés;
- tableaux avec en-têtes corrects;
- graphiques avec résumé textuel et données téléchargeables;
- `prefers-reduced-motion` respecté;
- contraste testé dans les deux thèmes;
- langue du document mise à jour;
- texte alternatif scientifique, pas décoratif;
- tests axe automatisés complétés par une revue clavier et lecteur d’écran.

L’audit sur captures ne permet pas de certifier la conformité complète. Les comportements clavier, lecteur d’écran, zoom, reflow et annonces dynamiques doivent être testés sur l’implémentation finale.

## 15. Sécurité, confidentialité et intégrité

- Aucun compte utilisateur dans le MVP.
- Aucune donnée personnelle collectée.
- Pas de cookies non essentiels par défaut.
- Analytics uniquement si justifié et avec configuration respectueuse de la vie privée.
- Validation stricte des entrées serveur.
- Rate limiting sur les routes de simulation.
- Taille maximale des payloads.
- CORS limité au domaine de l’application si nécessaire.
- Content Security Policy.
- En-têtes de sécurité.
- Dépendances scannées en CI.
- Secrets uniquement dans Vercel.
- Logs sans payload complet si celui-ci peut devenir volumineux.
- Aucune exécution de code arbitraire.
- Aucune requête SQL libre.
- Artefacts vérifiés par SHA-256.
- Sorties JSON strictes, sans `NaN` ou `Infinity`.

## 16. Performance et fiabilité

Objectifs initiaux:

- pages éditoriales rendues statiquement;
- pas de téléchargement automatique du dataset brut;
- JavaScript initial limité au strict nécessaire;
- chargement différé des figures lourdes;
- feedback immédiat au lancement d’un calcul;
- annulation ou timeout géré;
- health check indépendant du calcul;
- aucune dépendance au SQLite généraliste;
- résultats canoniques disponibles même si le moteur live est momentanément indisponible;
- les résultats canoniques statiques doivent toujours indiquer qu’ils sont pré-calculés et vérifiés.

Critères Web recommandés:

- LCP inférieur à 2,5 secondes au 75e percentile sur les pages statiques;
- CLS inférieur à 0,1;
- INP inférieur à 200 ms hors calcul serveur;
- aucun décalage de mise en page à l’apparition des graphiques.

## 17. Tests et assurance qualité

### 17.1 Tests scientifiques

- replay exact avec même seed;
- isolation des sous-flux;
- stabilité du validateur;
- conservation des rejets dans le Failure Atlas;
- JSON strict;
- comparaison des résultats au golden master;
- contrôle des huit claims et métriques;
- vérification des 3 588 échecs de traçabilité, de l’échec de ratio combiné et des cinq rejets du run canonique;
- vérification du stress joint 1,25 et du ratio moyen proche de 1,11;
- vérification des résultats externes 38 340, 39 276, 36,25 M et 38,11 M selon les règles d’arrondi du paper.

### 17.2 Tests de données

- schéma attendu;
- volumes;
- types;
- valeurs manquantes;
- doublons;
- bornes;
- empreintes;
- périodes;
- absence de recalibrage sur l’année d’évaluation;
- correspondance figure vers fichier source.

### 17.3 Tests logiciels

- tests unitaires TypeScript et Python;
- tests de contrat API;
- tests E2E des parcours reviewer, replay et téléchargement;
- tests de thème et langue;
- tests de routes propres;
- tests de téléchargement;
- tests de visual regression desktop et mobile;
- tests d’accessibilité automatisés;
- tests de sécurité des paramètres;
- test de déploiement Preview.

### 17.4 Matrice de navigateurs

- Chrome courant;
- Firefox courant;
- Safari courant;
- Edge courant;
- Safari iOS et Chrome Android pour les parcours principaux.

## 18. CI et CD

Chaque pull request doit exécuter:

1. formatage et lint;
2. vérification TypeScript;
3. tests unitaires frontend;
4. tests Python;
5. tests de contrat API;
6. vérification des checksums;
7. replay scientifique réduit;
8. comparaison au golden master;
9. accessibilité automatisée;
10. build Vercel;
11. tests E2E sur Preview;
12. capture visuelle des pages principales.

Avant une release:

1. replay canonique complet dans l’environnement enregistré;
2. génération de tous les artefacts;
3. génération du manifeste global;
4. validation du claim register;
5. compilation du paper;
6. génération des checksums;
7. création de la release brouillon;
8. ajout de tous les assets;
9. publication de la release immuable;
10. archivage DOI;
11. déploiement production depuis le commit exact;
12. vérification que l’application affiche le bon SHA et le bon DOI.

## 19. Observabilité

- logs structurés par `run_id`;
- durée, statut HTTP, version et type de run;
- pas de journalisation des résultats complets par défaut;
- métriques de taux d’erreur et timeout;
- alerte sur incompatibilité entre release déclarée et commit déployé;
- alerte si le manifeste canonique manque ou échoue au checksum;
- page de statut simple dans la reproductibilité;
- conservation raisonnable des logs, sans donnée personnelle.

## 20. Livrables

### 20.1 Produit

- nouveau dépôt GitHub;
- nouveau projet Vercel;
- application bilingue responsive;
- moteur ARCCRAFT aligné;
- API v1;
- pages définies dans l’architecture de l’information;
- thème clair et sombre;
- galerie des figures;
- laboratoire;
- Failure Atlas;
- catalogue de données;
- page de reproductibilité;
- page de citation.

### 20.2 Reproductibilité

- release GitHub immuable;
- archive DOI;
- paquet de réplication;
- `CITATION.cff`;
- manifestes;
- checksums;
- lockfiles;
- procédure locale;
- procédure de build;
- résultats canoniques;
- rapport de tests.

### 20.3 Documentation

- README;
- architecture;
- dictionnaire de données;
- documentation API;
- guide de contribution;
- politique de sécurité;
- licences;
- limites scientifiques;
- journal de changements.

## 21. Plan de réalisation proposé

### Phase 0, gel scientifique

- choisir l’état exact du moteur à publier;
- intégrer ou rejeter les modifications locales non commitées;
- exécuter toute la validation;
- fixer les versions;
- générer le golden master;
- approuver la matrice claim-métrique.

Critère de sortie: un commit local propre reproduit tous les résultats du paper.

### Phase 1, extraction et isolation

- créer le nouveau dépôt;
- copier uniquement les composants visuels réutilisables;
- extraire le moteur ARCCRAFT;
- supprimer MAPTA, COMPASS et les données hors périmètre;
- créer l’arborescence des artefacts.

Critère de sortie: le nouveau dépôt construit une application ARCCRAFT minimale sans dépendance à l’ancien dépôt.

### Phase 2, publication éditoriale

- accueil;
- paper;
- figures;
- evidence;
- limites;
- citation;
- anglais et français;
- thèmes.

Critère de sortie: un reviewer peut comprendre et télécharger le paper sans utiliser le laboratoire.

### Phase 3, reproductibilité

- API enrichie;
- replay canonique;
- manifestes;
- checksums;
- Failure Atlas;
- téléchargements;
- golden master.

Critère de sortie: le replay correspond à l’empreinte publiée ou signale clairement la divergence.

### Phase 4, qualité et déploiement

- E2E;
- accessibilité;
- visual regression;
- sécurité;
- performance;
- Preview et staging;
- correction des duplications;
- déploiement production.

Critère de sortie: tous les P0 sont validés.

### Phase 5, release scientifique

- release immuable;
- archive DOI;
- mise à jour de la citation;
- nouveau QR code;
- recompilation du paper si nécessaire;
- contrôle final des liens et checksums.

Critère de sortie: le paper, le site, GitHub et l’archive pointent vers la même version scientifique.

## 22. Critères de recette finale

La publication est acceptée uniquement si:

1. le dépôt GitHub et le projet Vercel sont distincts de l’application actuelle;
2. le dépôt de production est propre et le commit déployé est visible;
3. le backend public et la release scientifique utilisent le même moteur;
4. le replay canonique est exact;
5. les huit claims sont reliés à des métriques et des fichiers;
6. les figures 1 à 7 sont reliées à leurs données et scripts;
7. le PDF, la bibliographie et les citations sont téléchargeables;
8. l’archive DOI existe ou son absence bloque explicitement le statut final;
9. les résultats publiés et exploratoires sont clairement séparés;
10. la page Limites est complète;
11. les routes propres fonctionnent sans hash;
12. anglais, français, clair et sombre sont testés;
13. aucune duplication de bloc n’apparaît;
14. les parcours clavier sont complets;
15. les tests P0 sont verts;
16. les checksums sont valides;
17. les URLs du nouveau QR code et du paper correspondent;
18. aucun contenu MAPTA ou COMPASS n’est présenté comme composant du nouveau produit;
19. aucune donnée lourde ou hors périmètre n’est incluse par accident dans le bundle Vercel;
20. la page d’accueil qualifie correctement la validation externe de partielle.

## 23. Risques et mesures de contrôle

| Risque | Impact | Contrôle |
|---|---|---|
| Divergence entre moteur web et paper | Critique | Golden master, commit visible, release immuable |
| Confusion entre résultat publié et exploration | Critique | Modes séparés, badges et manifestes |
| Surinterprétation de la validation externe | Critique | Limites permanentes, wording contrôlé |
| Bundle trop volumineux | Élevé | Exclure SQLite et données hors périmètre |
| Timeout de simulation | Élevé | Bornes, pré-calcul canonique, procédure locale |
| Modification d’un artefact après publication | Critique | Release immuable, DOI et checksums |
| Licence de données insuffisante | Élevé | Registre de licence, lien externe si redistribution interdite |
| Duplication ou défaut responsive | Moyen | Visual regression et E2E |
| Inaccessibilité des graphiques | Élevé | Résumés textuels, CSV et revue lecteur d’écran |
| QR code obsolète | Moyen | QR généré uniquement après URL production stable |
| Dépendance à un service vivant | Élevé | Archive DOI et paquet local |

## 24. Décisions à confirmer avant implémentation

1. Nom final du dépôt et du projet Vercel.
2. Visibilité publique immédiate ou publication après staging.
3. Licence du code.
4. Licence de chaque dataset et droit de redistribution.
5. ORCID des auteurs.
6. Statut de publication du paper et métadonnées de la revue.
7. État exact du moteur à geler, commit de base ou modifications locales actuelles.
8. Choix du service d’archive, Zenodo recommandé.
9. Domaine final.
10. Niveau de calcul autorisé sur Vercel.

## 25. Sources de cadrage technique

- [Runtime Python et FastAPI sur Vercel](https://vercel.com/docs/functions/runtimes/python)
- [Limites des fonctions Vercel](https://vercel.com/docs/functions/limitations)
- [Releases GitHub immuables](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)
- [Fichiers de citation GitHub](https://docs.github.com/en/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files)
- [Intégration GitHub et Zenodo](https://help.zenodo.org/docs/github/)
- [Archivage d’une release GitHub dans Zenodo](https://help.zenodo.org/docs/github/archive-software/github-upload/)
- [Réservation d’un DOI Zenodo](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)

## 26. Verdict

L’application existante est une bonne référence de design et une preuve de faisabilité fonctionnelle. Elle ne doit pas être prolongée comme artefact officiel du paper. La voie correcte consiste à créer un produit ARCCRAFT dédié, construit depuis une version scientifique gelée, avec des artefacts petits et traçables, une release immuable, une archive DOI, des routes propres et une séparation stricte entre résultat publié, replay et exploration.

Le premier travail d’implémentation doit être le gel du moteur scientifique. Tant que les modifications locales actuelles et le backend public ne sont pas réconciliés, la création de l’interface risquerait de figer une incohérence au lieu de la résoudre.
