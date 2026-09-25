# ARCCRAFT — rapport de phase 0

Date : 25 septembre 2026. Périmètre : audit des ressources, réconciliation du moteur, replays et proposition du gel scientifique avant développement de l’interface.

**Verdict : moteur candidat reproduit ; gel officiel de la publication encore ouvert.** Les calculs enregistrés sont reproduits. Des incohérences éditoriales et des décisions de publication empêchent d’affirmer que tous les résultats affichables du paper constituent déjà une release cohérente et approuvée.

## 1. Séquence et protection des originaux

Le cahier des charges a été lu intégralement avant l’inventaire et toute écriture. Les chemins du message comportaient des échappements : les dossiers réels sont `D:\Projet\SOUTENANCE\POC_ARCCRAFT` et `D:\Projet\SOUTENANCE\Quantitative_Datasets_Clean_Final`.

Les nouvelles écritures sont isolées dans `arccraft-research-companion`. Après exécution, les 270 fichiers inventorés ont conservé leurs empreintes et l’état Git de l’ancienne application est inchangé. Preuve : [source-integrity-after.json](../audit/source-integrity-after.json). Les caches, `.git`, `node_modules` et `.vercel` sont exclus du périmètre de cette comparaison. Aucun nettoyage des disques ni changement du déploiement existant n’a été effectué.

## 2. Inventaire

Inventaire détaillé : [inventory.json](../audit/inventory.json), avec chemin absolu, taille et SHA-256 pour chaque fichier. Total : 270 fichiers, 708 043 970 octets, avec doublons et copies de livraison conservés comme tels.

| Ressource | Constat | Usage retenu |
|---|---|---|
| Recherche ARCCRAFT | 161 fichiers inventoriés : protocole, revue, registres, manuscrits, CSV, notebooks, figures, sources LaTeX, archives, captures | Preuves et historique ; sélectionner les artefacts P0 |
| Manuscrit 31 | Présent, draft complet, auteurs identifiés, affiliations et correspondant encore manquants | Source éditoriale à corriger dans une nouvelle version |
| Audit 32 | Huit claims C1–C8 ; fichiers sources présents | Registre enrichi calculé dans `audit/claim-register.json` |
| PDF demandé | Présent, 2 312 776 octets ; source LaTeX et bibliographie présentes | Conserver comme PDF historique ; recompiler la version approuvée |
| Figures | PNG 1–8, TikZ pour 1, Python pour 2–8, captions et record de provenance | 1–7 pour la nouvelle application ; remplacer le QR 8 après URL stable |
| Application de référence | 57 fichiers hors dépendances/caches ; base Git `b3df670227efa4aecf5383979b90f3eab15ae528` ; quatre fichiers modifiés | Lecture seule, comparaison du moteur et référence visuelle |
| Démonstrateur public | Santé `ok`, API 2.1.0 ; calcul de 100 mondes contrôlé | Preuve du comportement actuel, pas autorité du paper |
| Sources quantitatives | 51 fichiers : CSV automobile, dictionnaire XLSX, ZIP identique, Findex, WDI, HCI, IMF, autres classeurs et rapports | Automobile uniquement pour le paper ; autres ressources inventoriées, exclues du MVP |
| Environnement | Python 3.12.14, NumPy 2.3.5, pandas 3.0.1, SciPy 1.18.1, Matplotlib 3.11.2 | Environnement observé enregistré ; installation vierge encore à qualifier |

Le venv historique `mapta-verify-venv-20260921` ne contient pas pandas. Les validations ont donc utilisé le runtime Python fourni par l’environnement, avec versions correspondant aux dépendances scientifiques annoncées. Cela est enregistré, pas assimilé à un nouvel environnement vierge.

## 3. Données : autorisation, identité et correspondance

La [fiche du dépôt Mendeley, version 1](https://data.mendeley.com/datasets/sw4jmdb2sm/1) confirme le DOI `10.17632/sw4jmdb2sm.1`, les contributeurs Priscila Espinosa, Josep Lledó et David Atance, la période 2022–2024 et la licence CC BY 4.0. Vérification le 25 septembre 2026. La copie locale n’a pas été comparée à un téléchargement neuf de l’éditeur ; son identité est établie vis-à-vis du manifeste de recherche et de l’archive ZIP locale.

| Contrôle | Résultat |
|---|---|
| SHA-256 du CSV | `6a47d19d5278a049ea0aeaf39c955cc26068639bdc58cb4523b201e740f0faf4` — identique au manifeste historique |
| SHA-256 du dictionnaire | `cde44e797a7fd34de29199c78c9301d6f00ed94fd725b4fe8e67e6c2c4cc2e41` — identique au manifeste historique |
| Contenu du ZIP | Les deux fichiers ont les mêmes empreintes que les fichiers fournis séparément |
| Volume et schéma | 354 140 lignes, 47 colonnes ; schéma identique à la table normalisée |
| Comparaison exhaustive | 16 644 580 cellules normalisées comparées, zéro différence |
| Grain | 185 678 identifiants, zéro doublon assuré–année |
| Intégrité SQLite | `ok` |
| Conversion en valeurs manquantes | 513 valeurs de véhicule, 2 âges de véhicule, 2 valeurs de permis — comptabilisées explicitement |

La normalisation testée reproduit exactement celle du constructeur de base : séparateur `;`, espaces retirés, colonnes textuelles conservées, conversion numérique, valeurs non convertibles signalées puis nulles. Le statut `NA` du carburant reste une catégorie, pas une imputation silencieuse.

Le fichier brut retrouvé corrige une information désormais obsolète du manuscrit. Il ne corrige pas les limites statistiques : champ de permis ambigu, coûts agrégés par police–année, absence de frais et commissions, exercice rétrospectif et absence d’année prospectivement intacte.

Les 48 autres ressources quantitatives ne sont ni calibrées, ni incorporées, ni redistribuées. Leur licence et leur utilité scientifique n’ont pas été qualifiées, car elles sont hors du périmètre du paper. Leurs checksums sont disponibles pour une éventuelle analyse ultérieure.

## 4. Réconciliation public / base / local

Test du 25 septembre 2026 : `n_worlds=100`, `seed=20260825`. Réponses et code de comparaison conservés dans [audit/public](../audit/public).

| Champ | Public | Base Git b3df670 | Local corrigé / paper |
|---|---:|---:|---:|
| Monde du stress inverse | 184 | 184 | 196 |
| Distance standardisée | 0,9534068136272545 | 0,9534068136272545 | 1,0123246492985973 |
| Traçabilité | 0,9482548446253604 | 0,9482548446253604 | 0,9320731505217082 |
| Ratio combiné | 0,4175040666250729 | 0,4175040666250729 | 0,4017452053356689 |

Sur cette requête, classes, corrélations et synthèse de l’Atlas public correspondent aussi au moteur de base. Ce test démontre une concordance de comportement sur les champs comparés ; **il ne prouve pas le SHA du backend déployé**, que la réponse publique n’expose pas.

La différence du stress inverse est expliquée par le domaine de seed indépendant introduit dans le code local : `SeedSequence([master_seed, 0xAACC])` avec trois sous-flux. L’ancien calcul dépendait des flux de la simulation principale.

Modifications scientifiques locales à retenir :

1. Copie des tableaux d’état avant simulation : le validateur n’est plus muté.
2. Commutateur de transitions : les ablations enregistrées sont exécutables.
3. Atlas conservant les rejets, la seed réellement exécutée et les descripteurs stables de sous-flux.
4. Conversion des nombres non finis des rejets en `null`.
5. Stress inverse indépendant de la consommation antérieure des flux.
6. Adaptation des deux appels de service et des contrôles de régression.

Le patch complet est conservé dans [legacy-working-tree.patch](../audit/legacy-working-tree.patch). Le candidat reprend l’état local corrigé, pas le comportement historique du backend public. Aucun déploiement correctif n’a été effectué sur l’application existante.

## 5. Contrôles exécutés

| Contrôle | Résultat / limite |
|---|---|
| Suite backend historique | 27/27 PASS ; suite de l’application de référence, pas recette du futur produit |
| Ablations | 15 configurations–seeds, deux exécutions chacune ; 15 empreintes identiques aux fichiers du paper |
| Colonnes d’ablation hors durée | Toutes identiques aux résultats enregistrés |
| Isolation des flux | Les empreintes d’origine et perturbées correspondent au fichier 27 ; flux nommés invariants, flux partagé modifié |
| Canonique | 8 037 PASS, 1 958 REPAIR, 5 REJECT ; 3 594 événements dans l’Atlas |
| Composition de l’Atlas | 3 588 traçabilité, 1 ratio combiné, 5 rejets structurels |
| Rejeu en pleine précision | Sérialisation déterministe des 10 000 résultats identique sur deux exécutions |
| Stress inverse | Résultat local identique aux arrondis du manuscrit |
| Contrôles scientifiques supplémentaires | 15/15 PASS dans `scientific-checks.json` |
| Notebook 08 | 9/9 cellules de code exécutées |
| Notebook 17 | 10/10 cellules de code exécutées |
| Résultats des notebooks | Les 13 CSV 09–14 et 18–24 sont identiques octet pour octet |
| Benchmark autonome depuis CSV | Résultats 19 et déciles 20 reproduits ; contrôle par colonne à `rtol=atol=1e-10` |
| Surface de stress | 25 moyennes et intervalles reproduits ; stress conjoint 1,25 : ratio moyen 1,1098536718903744 |
| Figures 2–7 | 24/25 contrôles des principaux tableaux numériques réussis ; une dernière décimale erronée en figure 3 |
| Originaux | 270/270 empreintes inchangées ; état Git historique inchangé |

Les notebooks ont été rejoués cellule par cellule dans un processus Python, avec répertoire de sortie redirigé et accès SQLite forcé en lecture seule. Ce n’est pas un test de l’interface Jupyter. Le contrôle des doublons du notebook 17 a d’abord échoué à cause du disque système presque plein, puis réussi avec `temp_store=MEMORY`. Aucun fichier utilisateur n’a été supprimé.

L’empreinte historique `61616d6739a13b3fb5f53b9d6df04790db4cc744dbd0ba4bca49be86ecf23cf6` utilise des métriques arrondies à 12 décimales. L’empreinte sémantique pleine précision et les empreintes des fichiers sont enregistrées séparément. Le nouvel audit ne transforme pas le contrôle historique en garantie d’identité binaire sur tous les OS.

Le timing historique reste une observation du paper : moyenne 3,592942 s, écart-type 1,045028 s, CV 29,085576 %. Les durées de cet audit ont été mesurées sous charge concurrente ; elles ne remplacent pas C8 et ne constituent pas un benchmark Vercel.

## 6. Divergences et blocages

| ID | Gravité / nature | Constat | Traitement proposé |
|---|---|---|---|
| D1 | Bloquant scientifique | Public et moteur du paper différents | Retenir le moteur local corrigé, extrait et vérifié ; nouveau backend uniquement |
| D2 | Bloquant éditorial | Manuscrit §4.2 et discussion : premier décile de coût 2023 annoncé à 1,68 ; CSV et figure : 1,505619. 1,684032 appartient au deuxième décile | Patch proposé ; porter la même correction dans les sources LaTeX de la future version |
| D3 | Bloquant de traçabilité | Exigence 38 340 / 36,25 M non rattachée à un run unique. Le run enregistré de 50 000 simulations, seed 42, donne 38 341,0563 / 36 248 443,3859, erreur −4,875586 %. Le run de 10 000 donne 38 342,3769 / 36 254 608,7437, erreur −4,859407 % | Retenir 50 000 comme expérience enregistrée ; exposer les autres comme variantes nommées ; corriger −4,86 % en −4,88 % lorsqu’on cite le run enregistré |
| D4 | Métadonnées obsolètes | Manuscrit : brut absent ; CSV et dictionnaire désormais retrouvés et réconciliés | Actualiser la future déclaration de disponibilité, en conservant l’historique |
| D5 | Risque de mauvais rattachement | CSV 13/14 : 3 000 mondes ; figure 6 et paper : 10 000 mondes | Nouveaux CSV canoniques explicitement suffixés `10000` ; ne pas écraser 13/14 |
| D6 | Mineur, arrondi | Figure 3 embarque −4,4435 pour B2 2024 ; source −4,443445612… s’arrondit à −4,4434 | Corriger le générateur de la future figure ; produire les graphiques à partir des CSV |
| D7 | Bloquant publication | Code, paper et figures sans licence de publication confirmée ; DOI et métadonnées finales absents | Décisions des auteurs et archive avant release finale |
| D8 | Validation technique restante | Installation vierge, replay Linux/Vercel, CI, navigateur et accessibilité pas encore exécutés | Préparer dans les phases suivantes ; aucune garantie multiplateforme revendiquée |
| D9 | Déploiement non traçable | SHA public non exposé ; mêmes anciennes versions déclarées malgré code différent | Versionner le nouveau contrat et afficher SHA complet + empreinte moteur |

Le patch éditorial [manuscript-corrections.patch](../proposals/manuscript-corrections.patch) est prêt à relire. Il ne modifie ni le manuscrit source ni le PDF original. L’erreur D2 est reproduite dans le LaTeX actuel et devra être corrigée avant recompilation.

Les corrections LaTeX et de la figure 3 sont aussi proposées dans [latex-and-figure-corrections.patch](../proposals/latex-and-figure-corrections.patch). Le PDF de 24 pages a été inspecté par extraction de texte ; sa mise en page n’a pas été recertifiée. Le test historique à 2 000 simulations, seed 42, produit 38 339,8075, qui s’arrondit à 38 340 : ce constat ne prouve pas que c’était l’origine de la valeur embarquée, mais montre pourquoi le nombre de simulations doit accompagner cette valeur.

## 7. Commit scientifique proposé

**Commit source candidat : `b642f8238d86b5ec3a4115d9d06d582682d69f1e`.** Il contient le moteur extrait, la calibration compacte, le benchmark autonome et les outils de contrôle. Il succède au commit d’extraction `5cb162d07fed2187644a017ad2e6eb9411efa2ca` ; la seconde modification corrige seulement la lecture UTF-8 des chemins de provenance sous Windows.

Le commit de livraison suivant contient les preuves, golden masters et ce rapport. Cette séparation évite une référence circulaire : les artefacts indiquent le commit des sources qui les vérifient, et leurs propres octets sont liés par SHA-256. Les producteurs historiques non commités restent explicitement non identifiés par un SHA unique.

Versions candidates : package `0.1.0.dev1`, moteur historique `0.1.0`, grammaire `world_grammar-0.1.0`, schéma historique `arccraft-output-1.0`, calibration compacte `motor-mendeley-v1-reconciled-20260925`. Avant publication, attribuer une nouvelle version de moteur/API pour distinguer le nouveau produit de l’ancien backend. Ne pas réécrire rétrospectivement les versions historiques.

Le gel officiel n’est pas prononcé. La condition « un commit propre reproduit tous les résultats du paper » est satisfaite pour les sorties computationnelles contrôlées, mais pas pour les assertions éditoriales incohérentes D2/D3/D6. La matrice C1–C8 est prête pour l’approbation scientifique des auteurs.

## 8. Architecture et suite

L’[architecture](ARCHITECTURE.md) retient Next.js/TypeScript statique ou hybride, un module Python pur et FastAPI, des artefacts immuables et une calibration compacte. Aucun SQLite généraliste, dataset brut, calcul de fitting de politique, module MAPTA ou COMPASS dans le runtime cible.

Le [plan](IMPLEMENTATION_PLAN.md) décrit l’extraction finale, les pages bilingues, les contrats de preuve, les replays, la qualité, le nouveau GitHub/Vercel et l’archivage.

## 9. Décisions humaines

Décisions nécessaires pour conclure le gel : approuver le moteur corrigé proposé, la matrice C1–C8 et les corrections D2/D3/D6 ; retenir explicitement le run automobile de 50 000 simulations comme référence, avec les autres paramètres comme variantes distinctes.

Décisions de publication : nom final (proposition du cahier : `BAT-El34/arccraft-research-companion` et Vercel `arccraft-research-companion`), visibilité immédiate ou après staging, licences du code et des artefacts rédigés, auteurs/collaborateurs et rôles, ORCID/affiliations/correspondant, statut de publication/revue, archive DOI (Zenodo proposé), domaine et budget de calcul Vercel.

Ces décisions viennent des sections 21 et 24 du cahier des charges et des incohérences mesurées, pas d’une exigence d’autorisation ajoutée par une compétence. GitHub distant, Vercel, release et DOI ne sont pas créés à ce stade de phase 0.
