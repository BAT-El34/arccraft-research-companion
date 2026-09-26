# Livraison du compagnon ARCCRAFT — version candidate

Le projet indépendant est développé dans `arccraft-research-companion`. Il contient une application Next.js/TypeScript avec vingt routes EN/FR, une API FastAPI et le moteur scientifique figé. Aucun fichier de l’ancienne application ou de la recherche originale n’a été modifié : le contrôle final des 270 empreintes passe.

## Accès et identités

- Dépôt : https://github.com/BAT-El34/arccraft-research-companion
- Revue d’implémentation : https://github.com/BAT-El34/arccraft-research-companion/pull/1
- Domaine dédié : https://arccraft-research-companion.vercel.app/fr/
- Projet Vercel : `prj_DHuvL7QH4Kxsa8ELexvuAapkrkZM`, équipe `elia-btks-projects`.
- Commit scientifique : `b642f8238d86b5ec3a4115d9d06d582682d69f1e`.
- Le commit du build déployé se lit dans `/api/v1/health` ; il est distinct du commit scientifique.

## Produit livré

Accueil, article, preuves, figures, laboratoire, Failure Atlas, données/provenance, reproductibilité, limites et citation. Le changement de langue conserve la page ; le thème persiste. Les huit claims exposent définition, formule, unité, population, source, empreinte, version, commit de vérification et limites. Le producteur historique inconnu reste signalé.

Les références pré-calculées ne sont jamais présentées comme une exécution live. Le canonique verrouille les paramètres ; les variantes utilisent le registre d’ablation ; l’exploration a son propre identifiant et manifeste. Le laboratoire expose classes, seuils, corrélations, stress inverse, environnement, durée, versions, flux et checksums. Les exports JSON/CSV conservent le contexte du run. L’Atlas permet de filtrer et de rejouer un monde en exécutant d’abord le run complet. Les rejets structurels et les métriques nulles restent visibles.

Le PDF corrigé, compilé en 24 pages, les figures, les sources et les citations sont téléchargeables. La figure 3 a été régénérée avec la correction approuvée. Le QR du paper vise le nouveau compagnon. Les originaux demeurent dans `evidence/`, les copies corrigées dans `publication/`.

## Résultats de vérification

| Contrôle | Résultat | Preuve |
|---|---|---|
| Sources originales | 270 fichiers inchangés | `audit/application/source-integrity-final.json` |
| Artefacts historiques | 69 empreintes conformes | `scripts/verify_checksums.py` |
| Téléchargements | 50 fichiers avec checksums et provenance | `artifacts/web-registry.json` |
| Runtime vierge Windows | Canonique exact, neuf tests API, quinze paires enregistrées | `audit/application/api-tests-fresh.txt` |
| Interface | 32 tests passants : Chromium, Edge, Firefox, WebKit | `audit/application/browser-matrix.json` |
| Accessibilité automatisée | Axe sur parcours clés, deux thèmes, reflow 320 px | Même rapport, captures jointes |
| Interactions complémentaires | Atlas exploratoire distinct, clavier, zoom 200 %, annulation | Suite `tests/browser/companion.spec.ts` |
| Dépendances web de production | Aucun avis signalé lors du scan | `audit/application/npm-audit-runtime.json` |
| Débit Vercel | Trois POST par minute et IP ; quatrième requête HTTP 429 | `audit/application/rate-limit-check.json` |
| PDF candidat | Texte corrigé, commit et nouveau compagnon, mots-clés sur couverture | `audit/application/pdf-candidate-checks.json` |

WebKit sous Windows ne constitue pas un test sur Safari/iOS physique. Les vérifications axe et clavier ne remplacent pas une revue humaine avec lecteur d’écran.

## Divergence numérique interplateforme

Windows/Python 3.12.14/NumPy 2.3.5 reproduit exactement la référence à pleine précision. Vercel/Linux, avec les mêmes versions Python et NumPy, diffère sur 15 champs numériques, avec un écart absolu maximal de `2.220446049250313e-16`. Aucune différence non numérique n’a été relevée ; l’empreinte historique arrondie à douze décimales correspond. Le replay automobile est exact.

La comparaison à pleine précision reste **DIVERGENT** sur Linux. Aucun golden master n’a été remplacé et aucune tolérance n’a été ajoutée. La CI distingue le replay exact dans l’environnement Windows de référence et le test du contrat de comparaison sur Linux. Les empreintes, exemples et environnements sont disponibles dans `audit/application/vercel-cross-runtime.json` et sur la page Reproductibilité.

Le premier benchmark Vercel observé est d’environ 3,37 s côté serveur pour le synthétique complet avec diagnostics, et 0,03 s pour le moteur automobile. Ce sont des observations d’exécution, pas un engagement de latence. Les requêtes sont bornées ; le client attend au maximum 55 s et la fonction dispose de 60 s. Le WAF limite par IP et région, sans constituer un quota mondial de dépenses.

## Décisions et accès encore nécessaires

1. Licences du code, du texte et des figures. La licence externe automobile CC BY 4.0 est déjà vérifiée ; elle ne définit pas celle du logiciel ou du paper.
2. Affiliations, ORCID et auteur correspondant ; statut éditorial définitif.
3. DOI de version et archive scientifique immuable avant publication finale.
4. Autoriser l’application officielle Vercel sur le nouveau dépôt GitHub pour les déploiements automatiques. L’API Vercel a confirmé l’absence d’installation de cette intégration ; les déploiements CLI fonctionnent.
5. Revue humaine du candidat et tests sur appareils Safari/iOS et lecteur d’écran avant déclaration de conformité complète.

Ces éléments restent explicites dans l’application. Aucun DOI, droit de réutilisation, acceptation en revue, validation externe complète ou approbation scientifique supplémentaire n’est inventé.
