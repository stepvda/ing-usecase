# Export des données ING — Benchmark marketing KBC vs ING

Document généré automatiquement à partir de `benchmark.db`, destiné à servir d'entrée à un autre pipeline (rapprochement avec les campagnes publicitaires réelles). Toutes les données ci-dessous concernent uniquement la banque ING.

## Méthodologie

- **Source Google Trends** : bibliothèque `pytrends`, geo=`BE`, timeframe=`today 5-y`.
- **Granularité réelle** : hebdomadaire (Google Trends bascule automatiquement en hebdomadaire pour une fenêtre de 5 ans, pas mensuel).
- **Détection d'anomalies** (par terme) : moyenne d'intérêt calculée par mois calendaire sur toutes les années disponibles (profil de saisonnalité de référence). Un point est flagué s'il dépasse à la fois (a) la moyenne générale du terme de plus de 1.5 écart-type (z-score ≥ 1.5) et (b) 1.3× la moyenne saisonnière normale de son mois. Les points flagués consécutifs sont groupés : un seul point isolé est un **pic isolé** (`isolated_spike`), deux points consécutifs ou plus sont une **tendance soutenue** (`sustained_trend`).
- **Hors périmètre** : ce projet ne collecte aucune donnée publicitaire (Meta Ad Library, Google Ads Transparency Center). Le rapprochement entre ces anomalies et des campagnes publicitaires réelles est fait dans un pipeline séparé, en utilisant cet export comme donnée d'entrée.

## Fiches produits ING

| Fiche produit | Termes de recherche ING |
|---|---|
| Compte professionnel / indépendant (`compte_professionnel`) | compte professionnel ING, ING zakelijke rekening, Business'Bank ING |
| Compte à vue particulier (`compte_a_vue`) | compte à vue ING, ING zichtrekening, ING Do Basic |
| Compte épargne particulier (`compte_epargne`) | compte épargne ING, ING spaarrekening, ING Orange Savings |
| Investissement / courtage en ligne (`investissement_courtage`) | ING Self Invest |
| Application mobile bancaire (`app_mobile`) | ING Banking, ING Smart Banking |
| Carte de crédit (`carte_credit`) | carte de crédit ING, ING kredietkaart, ING Card |
| Épargne-pension (`epargne_pension`) | épargne pension ING, ING pensioensparen, ING Star Fund |
| Assurance habitation (`assurance_habitation`) | assurance habitation ING, ING Home Insurance |
| Prêt hypothécaire (`pret_hypothecaire`) | prêt hypothécaire ING, ING hypothecair krediet |

## Données Google Trends brutes

5764 points hebdomadaires, 22 termes, du 2021-09-12 au 2026-09-13. Fournies séparément dans **`ing_trends_data.csv`** (colonnes : product_id, product_label, term, bank, language, date, value) — non incluses ici pour garder ce document lisible.

## Anomalies détectées (131)

| Fiche produit | Terme | Date | Valeur | Type d'anomalie | Score de déviation |
|---|---|---|---|---|---|
| app_mobile | ING Banking | 2021-09-19 | 15 | Tendance soutenue | 1.985 |
| epargne_pension | ING pensioensparen | 2021-09-19 | 51 | Pic isolé | 12.41 |
| app_mobile | ING Banking | 2021-09-26 | 15 | Tendance soutenue | 1.985 |
| app_mobile | ING Banking | 2021-10-03 | 17 | Tendance soutenue | 2.799 |
| epargne_pension | ING Star Fund | 2021-10-03 | 49 | Pic isolé | 3.152 |
| app_mobile | ING Banking | 2021-10-10 | 16 | Tendance soutenue | 2.392 |
| app_mobile | ING Banking | 2021-10-17 | 15 | Tendance soutenue | 1.985 |
| app_mobile | ING Banking | 2021-10-24 | 16 | Tendance soutenue | 2.392 |
| app_mobile | ING Smart Banking | 2021-10-24 | 1 | Pic isolé | 11.402 |
| carte_credit | ING Card | 2021-10-24 | 80 | Pic isolé | 1.808 |
| app_mobile | ING Banking | 2021-10-31 | 15 | Tendance soutenue | 1.985 |
| epargne_pension | ING Star Fund | 2021-10-31 | 50 | Pic isolé | 3.223 |
| app_mobile | ING Banking | 2021-11-07 | 19 | Tendance soutenue | 3.613 |
| app_mobile | ING Banking | 2021-11-21 | 15 | Tendance soutenue | 1.985 |
| epargne_pension | ING Star Fund | 2021-11-21 | 53 | Pic isolé | 3.435 |
| app_mobile | ING Banking | 2021-11-28 | 15 | Tendance soutenue | 1.985 |
| carte_credit | ING kredietkaart | 2021-11-28 | 25 | Pic isolé | 6.225 |
| pret_hypothecaire | prêt hypothécaire ING | 2021-12-05 | 71 | Pic isolé | 9.541 |
| app_mobile | ING Banking | 2021-12-12 | 16 | Tendance soutenue | 2.392 |
| app_mobile | ING Banking | 2021-12-19 | 16 | Tendance soutenue | 2.392 |
| app_mobile | ING Banking | 2021-12-26 | 15 | Tendance soutenue | 1.985 |
| epargne_pension | ING Star Fund | 2021-12-26 | 63 | Pic isolé | 4.142 |
| app_mobile | ING Banking | 2022-01-02 | 15 | Tendance soutenue | 1.985 |
| carte_credit | ING Card | 2022-01-09 | 81 | Pic isolé | 1.862 |
| app_mobile | ING Banking | 2022-01-16 | 15 | Pic isolé | 1.985 |
| app_mobile | ING Banking | 2022-01-30 | 17 | Tendance soutenue | 2.799 |
| carte_credit | ING Card | 2022-01-30 | 77 | Tendance soutenue | 1.646 |
| app_mobile | ING Banking | 2022-02-06 | 14 | Tendance soutenue | 1.578 |
| carte_credit | ING Card | 2022-02-06 | 76 | Tendance soutenue | 1.592 |
| app_mobile | ING Banking | 2022-02-13 | 14 | Tendance soutenue | 1.578 |
| epargne_pension | ING Star Fund | 2022-02-20 | 41 | Pic isolé | 2.587 |
| app_mobile | ING Banking | 2022-02-27 | 14 | Pic isolé | 1.578 |
| investissement_courtage | ING Self Invest | 2022-03-06 | 2 | Tendance soutenue | 4.342 |
| compte_a_vue | ING zichtrekening | 2022-03-13 | 19 | Pic isolé | 4.71 |
| investissement_courtage | ING Self Invest | 2022-03-13 | 2 | Tendance soutenue | 4.342 |
| epargne_pension | ING Star Fund | 2022-04-03 | 36 | Pic isolé | 2.234 |
| compte_a_vue | ING zichtrekening | 2022-05-01 | 12 | Pic isolé | 2.913 |
| carte_credit | ING Card | 2022-05-22 | 83 | Pic isolé | 1.97 |
| carte_credit | ING Card | 2022-07-03 | 79 | Pic isolé | 1.754 |
| compte_professionnel | ING zakelijke rekening | 2022-07-31 | 81 | Pic isolé | 12.661 |
| carte_credit | ING Card | 2022-08-07 | 77 | Pic isolé | 1.646 |
| epargne_pension | ING Star Fund | 2022-08-28 | 48 | Pic isolé | 3.082 |
| epargne_pension | ING Star Fund | 2022-09-11 | 41 | Pic isolé | 2.587 |
| compte_a_vue | compte à vue ING | 2022-10-02 | 15 | Pic isolé | 15.876 |
| epargne_pension | ING Star Fund | 2022-10-09 | 57 | Pic isolé | 3.718 |
| carte_credit | carte de crédit ING | 2022-10-16 | 23 | Pic isolé | 6.18 |
| epargne_pension | ING Star Fund | 2022-11-06 | 48 | Tendance soutenue | 3.082 |
| carte_credit | ING kredietkaart | 2022-11-13 | 25 | Pic isolé | 6.225 |
| epargne_pension | ING Star Fund | 2022-11-13 | 40 | Tendance soutenue | 2.516 |
| epargne_pension | ING Star Fund | 2022-11-27 | 39 | Pic isolé | 2.446 |
| epargne_pension | ING pensioensparen | 2022-12-18 | 42 | Pic isolé | 10.203 |
| compte_epargne | ING spaarrekening | 2022-12-25 | 38 | Tendance soutenue | 2.95 |
| epargne_pension | ING Star Fund | 2022-12-25 | 50 | Pic isolé | 3.223 |
| compte_epargne | ING spaarrekening | 2023-01-01 | 47 | Tendance soutenue | 3.81 |
| compte_professionnel | ING zakelijke rekening | 2023-01-01 | 63 | Pic isolé | 9.826 |
| compte_epargne | ING spaarrekening | 2023-01-08 | 35 | Tendance soutenue | 2.663 |
| epargne_pension | ING Star Fund | 2023-01-08 | 48 | Tendance soutenue | 3.082 |
| compte_epargne | ING Orange Savings | 2023-01-15 | 11 | Pic isolé | 6.485 |
| compte_epargne | ING spaarrekening | 2023-01-15 | 24 | Tendance soutenue | 1.612 |
| epargne_pension | ING Star Fund | 2023-01-15 | 48 | Tendance soutenue | 3.082 |
| compte_epargne | ING spaarrekening | 2023-01-22 | 25 | Tendance soutenue | 1.708 |
| compte_epargne | ING spaarrekening | 2023-01-29 | 29 | Tendance soutenue | 2.09 |
| carte_credit | ING Card | 2023-02-05 | 80 | Pic isolé | 1.808 |
| carte_credit | ING kredietkaart | 2023-02-05 | 26 | Pic isolé | 6.48 |
| investissement_courtage | ING Self Invest | 2023-02-05 | 3 | Pic isolé | 6.595 |
| epargne_pension | ING Star Fund | 2023-03-05 | 42 | Pic isolé | 2.658 |
| compte_epargne | compte épargne ING | 2023-04-23 | 13 | Pic isolé | 8.862 |
| epargne_pension | ING Star Fund | 2023-05-21 | 49 | Pic isolé | 3.152 |
| compte_professionnel | compte professionnel ING | 2023-05-28 | 73 | Pic isolé | 9.898 |
| compte_a_vue | ING Do Basic | 2023-06-04 | 18 | Pic isolé | 16.155 |
| compte_epargne | ING spaarrekening | 2023-07-30 | 32 | Tendance soutenue | 2.377 |
| carte_credit | ING Card | 2023-08-06 | 75 | Pic isolé | 1.538 |
| compte_epargne | ING spaarrekening | 2023-08-06 | 27 | Tendance soutenue | 1.899 |
| compte_epargne | ING spaarrekening | 2023-08-20 | 45 | Tendance soutenue | 3.619 |
| investissement_courtage | ING Self Invest | 2023-08-20 | 3 | Tendance soutenue | 6.595 |
| compte_epargne | ING spaarrekening | 2023-08-27 | 37 | Tendance soutenue | 2.854 |
| investissement_courtage | ING Self Invest | 2023-08-27 | 3 | Tendance soutenue | 6.595 |
| epargne_pension | ING Star Fund | 2023-09-24 | 59 | Pic isolé | 3.859 |
| compte_epargne | ING spaarrekening | 2023-10-29 | 42 | Pic isolé | 3.332 |
| epargne_pension | ING Star Fund | 2023-11-12 | 47 | Tendance soutenue | 3.011 |
| epargne_pension | ING Star Fund | 2023-11-19 | 43 | Tendance soutenue | 2.728 |
| compte_epargne | ING spaarrekening | 2023-11-26 | 27 | Pic isolé | 1.899 |
| compte_epargne | compte épargne ING | 2023-12-03 | 14 | Pic isolé | 9.554 |
| epargne_pension | ING Star Fund | 2023-12-17 | 60 | Tendance soutenue | 3.93 |
| compte_a_vue | ING zichtrekening | 2023-12-24 | 16 | Pic isolé | 3.94 |
| epargne_pension | ING Star Fund | 2023-12-24 | 50 | Tendance soutenue | 3.223 |
| compte_epargne | ING spaarrekening | 2024-01-28 | 23 | Pic isolé | 1.517 |
| compte_epargne | ING spaarrekening | 2024-03-10 | 23 | Pic isolé | 1.517 |
| app_mobile | ING Banking | 2024-03-24 | 26 | Pic isolé | 6.461 |
| carte_credit | ING Card | 2024-03-24 | 100 | Pic isolé | 2.888 |
| carte_credit | carte de crédit ING | 2024-04-07 | 35 | Pic isolé | 9.472 |
| carte_credit | ING kredietkaart | 2024-04-28 | 24 | Pic isolé | 5.969 |
| carte_credit | carte de crédit ING | 2024-05-26 | 23 | Pic isolé | 6.18 |
| compte_a_vue | ING zichtrekening | 2024-08-25 | 24 | Tendance soutenue | 5.993 |
| compte_epargne | ING spaarrekening | 2024-08-25 | 41 | Tendance soutenue | 3.237 |
| compte_a_vue | ING zichtrekening | 2024-09-01 | 39 | Tendance soutenue | 9.843 |
| compte_epargne | ING spaarrekening | 2024-09-01 | 49 | Tendance soutenue | 4.001 |
| carte_credit | ING kredietkaart | 2024-09-08 | 26 | Pic isolé | 6.48 |
| compte_a_vue | ING zichtrekening | 2024-09-08 | 28 | Tendance soutenue | 7.02 |
| compte_epargne | ING spaarrekening | 2024-09-08 | 32 | Tendance soutenue | 2.377 |
| compte_a_vue | ING zichtrekening | 2024-09-22 | 19 | Pic isolé | 4.71 |
| compte_epargne | ING spaarrekening | 2024-12-29 | 25 | Pic isolé | 1.708 |
| epargne_pension | ING Star Fund | 2025-01-19 | 71 | Pic isolé | 4.708 |
| investissement_courtage | ING Self Invest | 2025-02-16 | 3 | Pic isolé | 6.595 |
| compte_professionnel | Business'Bank ING | 2025-03-02 | 79 | Pic isolé | 10.904 |
| investissement_courtage | ING Self Invest | 2025-05-25 | 3 | Pic isolé | 6.595 |
| pret_hypothecaire | prêt hypothécaire ING | 2025-05-25 | 75 | Pic isolé | 10.085 |
| assurance_habitation | ING Home Insurance | 2025-06-08 | 79 | Pic isolé | 16.155 |
| compte_epargne | ING Orange Savings | 2025-08-10 | 19 | Pic isolé | 11.278 |
| compte_epargne | ING spaarrekening | 2025-08-24 | 23 | Pic isolé | 1.517 |
| compte_professionnel | compte professionnel ING | 2025-11-02 | 93 | Pic isolé | 12.636 |
| pret_hypothecaire | ING hypothecair krediet | 2025-12-14 | 69 | Pic isolé | 9.396 |
| pret_hypothecaire | prêt hypothécaire ING | 2026-01-25 | 60 | Pic isolé | 8.046 |
| compte_epargne | ING spaarrekening | 2026-02-22 | 25 | Pic isolé | 1.708 |
| carte_credit | ING kredietkaart | 2026-04-05 | 29 | Pic isolé | 7.248 |
| epargne_pension | épargne pension ING | 2026-04-12 | 100 | Pic isolé | 16.148 |
| pret_hypothecaire | ING hypothecair krediet | 2026-04-19 | 96 | Pic isolé | 13.106 |
| app_mobile | ING Smart Banking | 2026-05-17 | 1 | Pic isolé | 11.402 |
| compte_epargne | compte épargne ING | 2026-06-07 | 12 | Pic isolé | 8.17 |
| compte_professionnel | Business'Bank ING | 2026-07-05 | 86 | Pic isolé | 11.878 |
| carte_credit | carte de crédit ING | 2026-08-02 | 35 | Pic isolé | 9.472 |
| assurance_habitation | assurance habitation ING | 2026-08-30 | 4 | Tendance soutenue | 7.181 |
| compte_a_vue | compte à vue ING | 2026-08-30 | 2 | Tendance soutenue | 2.05 |
| compte_epargne | ING Orange Savings | 2026-08-30 | 16 | Pic isolé | 9.481 |
| compte_epargne | compte épargne ING | 2026-08-30 | 4 | Tendance soutenue | 2.633 |
| assurance_habitation | assurance habitation ING | 2026-09-06 | 8 | Tendance soutenue | 14.444 |
| compte_a_vue | ING zichtrekening | 2026-09-06 | 7 | Pic isolé | 1.63 |
| compte_a_vue | compte à vue ING | 2026-09-06 | 2 | Tendance soutenue | 2.05 |
| compte_epargne | compte épargne ING | 2026-09-06 | 4 | Tendance soutenue | 2.633 |
| carte_credit | ING kredietkaart | 2026-09-13 | 7 | Pic isolé | 1.622 |
| compte_epargne | compte épargne ING | 2026-09-13 | 4 | Tendance soutenue | 2.633 |
