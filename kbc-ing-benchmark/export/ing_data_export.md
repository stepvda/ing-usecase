# Export des données ING — Benchmark marketing ING · KBC · CBC

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
| Compte professionnel / indépendant (CBC vs ING) (`compte_professionnel_cbc`) | compte professionnel ING, ING zakelijke rekening, Business'Bank ING |
| Compte à vue particulier (CBC vs ING) (`compte_a_vue_cbc`) | compte à vue ING, ING zichtrekening, ING Do Basic |
| Compte épargne particulier (CBC vs ING) (`compte_epargne_cbc`) | compte épargne ING, ING spaarrekening, ING Orange Savings |
| Application mobile bancaire (CBC vs ING) (`app_mobile_cbc`) | ING Banking, ING Smart Banking |
| Carte de crédit (CBC vs ING) (`carte_credit_cbc`) | carte de crédit ING, ING kredietkaart, ING Card |
| Épargne-pension (CBC vs ING) (`epargne_pension_cbc`) | épargne pension ING, ING pensioensparen, ING Star Fund |
| Assurance habitation (CBC vs ING) (`assurance_habitation_cbc`) | assurance habitation ING, ING Home Insurance |
| Prêt hypothécaire (CBC vs ING) (`pret_hypothecaire_cbc`) | prêt hypothécaire ING, ING hypothecair krediet |
| Marque (recherche générique) (`marque_generique`) | ING |

## Données Google Trends brutes

11528 points hebdomadaires, 23 termes, du 2021-09-12 au 2026-09-13. Fournies séparément dans **`ing_trends_data.csv`** (colonnes : product_id, product_label, term, bank, language, date, value) — non incluses ici pour garder ce document lisible.

## Anomalies détectées (268)

| Fiche produit | Terme | Date | Valeur | Type d'anomalie | Score de déviation |
|---|---|---|---|---|---|
| app_mobile | ING Banking | 2021-09-19 | 15 | Tendance soutenue | 1.985 |
| app_mobile_cbc | ING Banking | 2021-09-19 | 58 | Tendance soutenue | 1.924 |
| epargne_pension | ING pensioensparen | 2021-09-19 | 51 | Pic isolé | 12.41 |
| epargne_pension_cbc | ING pensioensparen | 2021-09-19 | 51 | Pic isolé | 12.398 |
| app_mobile | ING Banking | 2021-09-26 | 15 | Tendance soutenue | 1.985 |
| app_mobile_cbc | ING Banking | 2021-09-26 | 59 | Tendance soutenue | 2.028 |
| marque_generique | ING | 2021-09-26 | 77 | Pic isolé | 2.698 |
| app_mobile | ING Banking | 2021-10-03 | 17 | Tendance soutenue | 2.799 |
| app_mobile_cbc | ING Banking | 2021-10-03 | 67 | Tendance soutenue | 2.863 |
| epargne_pension | ING Star Fund | 2021-10-03 | 49 | Pic isolé | 3.152 |
| epargne_pension_cbc | ING Star Fund | 2021-10-03 | 49 | Pic isolé | 3.154 |
| app_mobile | ING Banking | 2021-10-10 | 16 | Tendance soutenue | 2.392 |
| app_mobile_cbc | ING Banking | 2021-10-10 | 62 | Tendance soutenue | 2.341 |
| app_mobile | ING Banking | 2021-10-17 | 15 | Tendance soutenue | 1.985 |
| app_mobile_cbc | ING Banking | 2021-10-17 | 58 | Tendance soutenue | 1.924 |
| app_mobile | ING Banking | 2021-10-24 | 16 | Tendance soutenue | 2.392 |
| app_mobile | ING Smart Banking | 2021-10-24 | 1 | Pic isolé | 11.402 |
| app_mobile_cbc | ING Banking | 2021-10-24 | 62 | Tendance soutenue | 2.341 |
| app_mobile_cbc | ING Smart Banking | 2021-10-24 | 4 | Pic isolé | 11.402 |
| carte_credit | ING Card | 2021-10-24 | 80 | Pic isolé | 1.808 |
| carte_credit_cbc | ING Card | 2021-10-24 | 80 | Pic isolé | 1.808 |
| app_mobile | ING Banking | 2021-10-31 | 15 | Tendance soutenue | 1.985 |
| app_mobile_cbc | ING Banking | 2021-10-31 | 59 | Tendance soutenue | 2.028 |
| epargne_pension | ING Star Fund | 2021-10-31 | 50 | Pic isolé | 3.223 |
| epargne_pension_cbc | ING Star Fund | 2021-10-31 | 50 | Pic isolé | 3.224 |
| app_mobile | ING Banking | 2021-11-07 | 19 | Tendance soutenue | 3.613 |
| app_mobile_cbc | ING Banking | 2021-11-07 | 75 | Tendance soutenue | 3.697 |
| app_mobile_cbc | ING Banking | 2021-11-14 | 56 | Tendance soutenue | 1.715 |
| app_mobile | ING Banking | 2021-11-21 | 15 | Tendance soutenue | 1.985 |
| app_mobile_cbc | ING Banking | 2021-11-21 | 59 | Tendance soutenue | 2.028 |
| epargne_pension | ING Star Fund | 2021-11-21 | 53 | Pic isolé | 3.435 |
| epargne_pension_cbc | ING Star Fund | 2021-11-21 | 53 | Pic isolé | 3.437 |
| app_mobile | ING Banking | 2021-11-28 | 15 | Tendance soutenue | 1.985 |
| app_mobile_cbc | ING Banking | 2021-11-28 | 58 | Tendance soutenue | 1.924 |
| carte_credit | ING kredietkaart | 2021-11-28 | 25 | Pic isolé | 6.225 |
| carte_credit_cbc | ING kredietkaart | 2021-11-28 | 25 | Pic isolé | 6.272 |
| app_mobile_cbc | ING Banking | 2021-12-05 | 56 | Tendance soutenue | 1.715 |
| pret_hypothecaire | prêt hypothécaire ING | 2021-12-05 | 71 | Pic isolé | 9.541 |
| pret_hypothecaire_cbc | prêt hypothécaire ING | 2021-12-05 | 61 | Pic isolé | 9.546 |
| app_mobile | ING Banking | 2021-12-12 | 16 | Tendance soutenue | 2.392 |
| app_mobile_cbc | ING Banking | 2021-12-12 | 61 | Tendance soutenue | 2.237 |
| app_mobile | ING Banking | 2021-12-19 | 16 | Tendance soutenue | 2.392 |
| app_mobile_cbc | ING Banking | 2021-12-19 | 61 | Tendance soutenue | 2.237 |
| app_mobile | ING Banking | 2021-12-26 | 15 | Tendance soutenue | 1.985 |
| app_mobile_cbc | ING Banking | 2021-12-26 | 57 | Tendance soutenue | 1.819 |
| epargne_pension | ING Star Fund | 2021-12-26 | 63 | Pic isolé | 4.142 |
| epargne_pension_cbc | ING Star Fund | 2021-12-26 | 63 | Pic isolé | 4.144 |
| app_mobile | ING Banking | 2022-01-02 | 15 | Tendance soutenue | 1.985 |
| app_mobile_cbc | ING Banking | 2022-01-02 | 60 | Tendance soutenue | 2.132 |
| carte_credit | ING Card | 2022-01-09 | 81 | Pic isolé | 1.862 |
| carte_credit_cbc | ING Card | 2022-01-09 | 81 | Pic isolé | 1.862 |
| app_mobile | ING Banking | 2022-01-16 | 15 | Pic isolé | 1.985 |
| app_mobile_cbc | ING Banking | 2022-01-16 | 59 | Pic isolé | 2.028 |
| app_mobile | ING Banking | 2022-01-30 | 17 | Tendance soutenue | 2.799 |
| app_mobile_cbc | ING Banking | 2022-01-30 | 66 | Tendance soutenue | 2.758 |
| carte_credit | ING Card | 2022-01-30 | 77 | Tendance soutenue | 1.646 |
| carte_credit_cbc | ING Card | 2022-01-30 | 77 | Tendance soutenue | 1.646 |
| marque_generique | ING | 2022-01-30 | 78 | Pic isolé | 2.816 |
| app_mobile | ING Banking | 2022-02-06 | 14 | Tendance soutenue | 1.578 |
| app_mobile_cbc | ING Banking | 2022-02-06 | 56 | Tendance soutenue | 1.715 |
| carte_credit | ING Card | 2022-02-06 | 76 | Tendance soutenue | 1.592 |
| carte_credit_cbc | ING Card | 2022-02-06 | 76 | Tendance soutenue | 1.592 |
| app_mobile | ING Banking | 2022-02-13 | 14 | Tendance soutenue | 1.578 |
| app_mobile_cbc | ING Banking | 2022-02-13 | 56 | Tendance soutenue | 1.715 |
| epargne_pension | ING Star Fund | 2022-02-20 | 41 | Pic isolé | 2.587 |
| epargne_pension_cbc | ING Star Fund | 2022-02-20 | 41 | Pic isolé | 2.588 |
| app_mobile | ING Banking | 2022-02-27 | 14 | Pic isolé | 1.578 |
| app_mobile_cbc | ING Banking | 2022-02-27 | 56 | Tendance soutenue | 1.715 |
| marque_generique | ING | 2022-02-27 | 75 | Pic isolé | 2.462 |
| app_mobile_cbc | ING Banking | 2022-03-06 | 57 | Tendance soutenue | 1.819 |
| investissement_courtage | ING Self Invest | 2022-03-06 | 2 | Tendance soutenue | 4.342 |
| compte_a_vue | ING zichtrekening | 2022-03-13 | 19 | Pic isolé | 4.71 |
| compte_a_vue_cbc | ING zichtrekening | 2022-03-13 | 48 | Pic isolé | 4.545 |
| investissement_courtage | ING Self Invest | 2022-03-13 | 2 | Tendance soutenue | 4.342 |
| epargne_pension | ING Star Fund | 2022-04-03 | 36 | Pic isolé | 2.234 |
| epargne_pension_cbc | ING Star Fund | 2022-04-03 | 36 | Pic isolé | 2.235 |
| compte_a_vue | ING zichtrekening | 2022-05-01 | 12 | Pic isolé | 2.913 |
| compte_a_vue_cbc | ING zichtrekening | 2022-05-01 | 31 | Pic isolé | 2.874 |
| marque_generique | ING | 2022-05-01 | 69 | Pic isolé | 1.754 |
| carte_credit | ING Card | 2022-05-22 | 83 | Pic isolé | 1.97 |
| carte_credit_cbc | ING Card | 2022-05-22 | 83 | Pic isolé | 1.97 |
| carte_credit | ING Card | 2022-07-03 | 79 | Pic isolé | 1.754 |
| carte_credit_cbc | ING Card | 2022-07-03 | 79 | Pic isolé | 1.754 |
| marque_generique | ING | 2022-07-03 | 69 | Pic isolé | 1.754 |
| compte_professionnel | ING zakelijke rekening | 2022-07-31 | 81 | Pic isolé | 12.661 |
| compte_professionnel_cbc | ING zakelijke rekening | 2022-07-31 | 79 | Pic isolé | 12.702 |
| carte_credit | ING Card | 2022-08-07 | 77 | Pic isolé | 1.646 |
| carte_credit_cbc | ING Card | 2022-08-07 | 77 | Pic isolé | 1.646 |
| epargne_pension | ING Star Fund | 2022-08-28 | 48 | Pic isolé | 3.082 |
| epargne_pension_cbc | ING Star Fund | 2022-08-28 | 48 | Pic isolé | 3.083 |
| epargne_pension | ING Star Fund | 2022-09-11 | 41 | Pic isolé | 2.587 |
| epargne_pension_cbc | ING Star Fund | 2022-09-11 | 41 | Pic isolé | 2.588 |
| compte_a_vue | compte à vue ING | 2022-10-02 | 15 | Pic isolé | 15.876 |
| compte_a_vue_cbc | compte à vue ING | 2022-10-02 | 39 | Pic isolé | 15.942 |
| epargne_pension | ING Star Fund | 2022-10-09 | 57 | Pic isolé | 3.718 |
| epargne_pension_cbc | ING Star Fund | 2022-10-09 | 57 | Pic isolé | 3.719 |
| carte_credit | carte de crédit ING | 2022-10-16 | 23 | Pic isolé | 6.18 |
| carte_credit_cbc | carte de crédit ING | 2022-10-16 | 23 | Pic isolé | 6.18 |
| epargne_pension | ING Star Fund | 2022-11-06 | 48 | Tendance soutenue | 3.082 |
| epargne_pension_cbc | ING Star Fund | 2022-11-06 | 48 | Tendance soutenue | 3.083 |
| carte_credit | ING kredietkaart | 2022-11-13 | 25 | Pic isolé | 6.225 |
| carte_credit_cbc | ING kredietkaart | 2022-11-13 | 25 | Pic isolé | 6.272 |
| epargne_pension | ING Star Fund | 2022-11-13 | 40 | Tendance soutenue | 2.516 |
| epargne_pension_cbc | ING Star Fund | 2022-11-13 | 40 | Tendance soutenue | 2.517 |
| epargne_pension | ING Star Fund | 2022-11-27 | 39 | Pic isolé | 2.446 |
| epargne_pension_cbc | ING Star Fund | 2022-11-27 | 39 | Pic isolé | 2.447 |
| epargne_pension | ING pensioensparen | 2022-12-18 | 42 | Pic isolé | 10.203 |
| epargne_pension_cbc | ING pensioensparen | 2022-12-18 | 42 | Pic isolé | 10.193 |
| compte_epargne | ING spaarrekening | 2022-12-25 | 38 | Tendance soutenue | 2.95 |
| compte_epargne_cbc | ING spaarrekening | 2022-12-25 | 77 | Tendance soutenue | 2.907 |
| epargne_pension | ING Star Fund | 2022-12-25 | 50 | Pic isolé | 3.223 |
| epargne_pension_cbc | ING Star Fund | 2022-12-25 | 50 | Pic isolé | 3.224 |
| compte_epargne | ING spaarrekening | 2023-01-01 | 47 | Tendance soutenue | 3.81 |
| compte_epargne_cbc | ING spaarrekening | 2023-01-01 | 97 | Tendance soutenue | 3.839 |
| compte_professionnel | ING zakelijke rekening | 2023-01-01 | 63 | Pic isolé | 9.826 |
| compte_professionnel_cbc | ING zakelijke rekening | 2023-01-01 | 61 | Pic isolé | 9.786 |
| compte_epargne | ING spaarrekening | 2023-01-08 | 35 | Tendance soutenue | 2.663 |
| compte_epargne_cbc | ING spaarrekening | 2023-01-08 | 72 | Tendance soutenue | 2.674 |
| epargne_pension | ING Star Fund | 2023-01-08 | 48 | Tendance soutenue | 3.082 |
| epargne_pension_cbc | ING Star Fund | 2023-01-08 | 48 | Tendance soutenue | 3.083 |
| compte_epargne | ING Orange Savings | 2023-01-15 | 11 | Pic isolé | 6.485 |
| compte_epargne | ING spaarrekening | 2023-01-15 | 24 | Tendance soutenue | 1.612 |
| compte_epargne_cbc | ING Orange Savings | 2023-01-15 | 22 | Pic isolé | 6.557 |
| compte_epargne_cbc | ING spaarrekening | 2023-01-15 | 49 | Tendance soutenue | 1.602 |
| epargne_pension | ING Star Fund | 2023-01-15 | 48 | Tendance soutenue | 3.082 |
| epargne_pension_cbc | ING Star Fund | 2023-01-15 | 48 | Tendance soutenue | 3.083 |
| compte_epargne | ING spaarrekening | 2023-01-22 | 25 | Tendance soutenue | 1.708 |
| compte_epargne_cbc | ING spaarrekening | 2023-01-22 | 51 | Tendance soutenue | 1.695 |
| compte_epargne | ING spaarrekening | 2023-01-29 | 29 | Tendance soutenue | 2.09 |
| compte_epargne_cbc | ING spaarrekening | 2023-01-29 | 60 | Tendance soutenue | 2.115 |
| carte_credit | ING Card | 2023-02-05 | 80 | Pic isolé | 1.808 |
| carte_credit | ING kredietkaart | 2023-02-05 | 26 | Pic isolé | 6.48 |
| carte_credit_cbc | ING Card | 2023-02-05 | 80 | Pic isolé | 1.808 |
| carte_credit_cbc | ING kredietkaart | 2023-02-05 | 26 | Pic isolé | 6.529 |
| investissement_courtage | ING Self Invest | 2023-02-05 | 3 | Pic isolé | 6.595 |
| epargne_pension | ING Star Fund | 2023-03-05 | 42 | Pic isolé | 2.658 |
| epargne_pension_cbc | ING Star Fund | 2023-03-05 | 42 | Pic isolé | 2.659 |
| compte_epargne | compte épargne ING | 2023-04-23 | 13 | Pic isolé | 8.862 |
| compte_epargne_cbc | compte épargne ING | 2023-04-23 | 26 | Pic isolé | 8.405 |
| epargne_pension | ING Star Fund | 2023-05-21 | 49 | Pic isolé | 3.152 |
| epargne_pension_cbc | ING Star Fund | 2023-05-21 | 49 | Pic isolé | 3.154 |
| compte_professionnel | compte professionnel ING | 2023-05-28 | 73 | Pic isolé | 9.898 |
| compte_professionnel_cbc | compte professionnel ING | 2023-05-28 | 71 | Pic isolé | 9.883 |
| compte_a_vue | ING Do Basic | 2023-06-04 | 18 | Pic isolé | 16.155 |
| compte_a_vue_cbc | ING Do Basic | 2023-06-04 | 46 | Pic isolé | 16.155 |
| compte_epargne | ING spaarrekening | 2023-07-30 | 32 | Tendance soutenue | 2.377 |
| compte_epargne_cbc | ING spaarrekening | 2023-07-30 | 66 | Tendance soutenue | 2.394 |
| carte_credit | ING Card | 2023-08-06 | 75 | Pic isolé | 1.538 |
| carte_credit_cbc | ING Card | 2023-08-06 | 75 | Pic isolé | 1.538 |
| compte_epargne | ING spaarrekening | 2023-08-06 | 27 | Tendance soutenue | 1.899 |
| compte_epargne_cbc | ING spaarrekening | 2023-08-06 | 55 | Tendance soutenue | 1.882 |
| compte_epargne | ING spaarrekening | 2023-08-20 | 45 | Tendance soutenue | 3.619 |
| compte_epargne_cbc | ING spaarrekening | 2023-08-20 | 92 | Tendance soutenue | 3.606 |
| investissement_courtage | ING Self Invest | 2023-08-20 | 3 | Tendance soutenue | 6.595 |
| compte_epargne | ING spaarrekening | 2023-08-27 | 37 | Tendance soutenue | 2.854 |
| compte_epargne_cbc | ING spaarrekening | 2023-08-27 | 76 | Tendance soutenue | 2.86 |
| investissement_courtage | ING Self Invest | 2023-08-27 | 3 | Tendance soutenue | 6.595 |
| marque_generique | ING | 2023-08-27 | 71 | Pic isolé | 1.99 |
| epargne_pension | ING Star Fund | 2023-09-24 | 59 | Pic isolé | 3.859 |
| epargne_pension_cbc | ING Star Fund | 2023-09-24 | 59 | Pic isolé | 3.861 |
| compte_epargne | ING spaarrekening | 2023-10-29 | 42 | Pic isolé | 3.332 |
| compte_epargne_cbc | ING spaarrekening | 2023-10-29 | 87 | Pic isolé | 3.373 |
| epargne_pension | ING Star Fund | 2023-11-12 | 47 | Tendance soutenue | 3.011 |
| epargne_pension_cbc | ING Star Fund | 2023-11-12 | 47 | Tendance soutenue | 3.012 |
| epargne_pension | ING Star Fund | 2023-11-19 | 43 | Tendance soutenue | 2.728 |
| epargne_pension_cbc | ING Star Fund | 2023-11-19 | 43 | Tendance soutenue | 2.73 |
| compte_epargne | ING spaarrekening | 2023-11-26 | 27 | Pic isolé | 1.899 |
| compte_epargne_cbc | ING spaarrekening | 2023-11-26 | 56 | Pic isolé | 1.928 |
| compte_epargne | compte épargne ING | 2023-12-03 | 14 | Pic isolé | 9.554 |
| compte_epargne_cbc | compte épargne ING | 2023-12-03 | 30 | Pic isolé | 9.719 |
| epargne_pension | ING Star Fund | 2023-12-17 | 60 | Tendance soutenue | 3.93 |
| epargne_pension_cbc | ING Star Fund | 2023-12-17 | 60 | Tendance soutenue | 3.932 |
| compte_a_vue | ING zichtrekening | 2023-12-24 | 16 | Pic isolé | 3.94 |
| compte_a_vue_cbc | ING zichtrekening | 2023-12-24 | 43 | Pic isolé | 4.053 |
| epargne_pension | ING Star Fund | 2023-12-24 | 50 | Tendance soutenue | 3.223 |
| epargne_pension_cbc | ING Star Fund | 2023-12-24 | 50 | Tendance soutenue | 3.224 |
| compte_epargne | ING spaarrekening | 2024-01-28 | 23 | Pic isolé | 1.517 |
| compte_epargne_cbc | ING spaarrekening | 2024-01-28 | 48 | Pic isolé | 1.556 |
| compte_epargne | ING spaarrekening | 2024-03-10 | 23 | Pic isolé | 1.517 |
| compte_epargne_cbc | ING spaarrekening | 2024-03-10 | 47 | Pic isolé | 1.509 |
| app_mobile | ING Banking | 2024-03-24 | 26 | Pic isolé | 6.461 |
| app_mobile_cbc | ING Banking | 2024-03-24 | 100 | Pic isolé | 6.306 |
| carte_credit | ING Card | 2024-03-24 | 100 | Pic isolé | 2.888 |
| carte_credit_cbc | ING Card | 2024-03-24 | 100 | Pic isolé | 2.889 |
| marque_generique | ING | 2024-03-24 | 90 | Pic isolé | 4.233 |
| carte_credit | carte de crédit ING | 2024-04-07 | 35 | Pic isolé | 9.472 |
| carte_credit_cbc | carte de crédit ING | 2024-04-07 | 35 | Pic isolé | 9.472 |
| carte_credit | ING kredietkaart | 2024-04-28 | 24 | Pic isolé | 5.969 |
| carte_credit_cbc | ING kredietkaart | 2024-04-28 | 24 | Pic isolé | 6.014 |
| carte_credit | carte de crédit ING | 2024-05-26 | 23 | Pic isolé | 6.18 |
| carte_credit_cbc | carte de crédit ING | 2024-05-26 | 23 | Pic isolé | 6.18 |
| compte_a_vue | ING zichtrekening | 2024-08-25 | 24 | Tendance soutenue | 5.993 |
| compte_a_vue_cbc | ING zichtrekening | 2024-08-25 | 62 | Tendance soutenue | 5.921 |
| compte_epargne | ING spaarrekening | 2024-08-25 | 41 | Tendance soutenue | 3.237 |
| compte_epargne_cbc | ING spaarrekening | 2024-08-25 | 84 | Tendance soutenue | 3.233 |
| marque_generique | ING | 2024-08-25 | 73 | Tendance soutenue | 2.226 |
| compte_a_vue | ING zichtrekening | 2024-09-01 | 39 | Tendance soutenue | 9.843 |
| compte_a_vue_cbc | ING zichtrekening | 2024-09-01 | 100 | Tendance soutenue | 9.657 |
| compte_epargne | ING spaarrekening | 2024-09-01 | 49 | Tendance soutenue | 4.001 |
| compte_epargne_cbc | ING spaarrekening | 2024-09-01 | 100 | Tendance soutenue | 3.979 |
| marque_generique | ING | 2024-09-01 | 82 | Tendance soutenue | 3.288 |
| carte_credit | ING kredietkaart | 2024-09-08 | 26 | Pic isolé | 6.48 |
| carte_credit_cbc | ING kredietkaart | 2024-09-08 | 26 | Pic isolé | 6.529 |
| compte_a_vue | ING zichtrekening | 2024-09-08 | 28 | Tendance soutenue | 7.02 |
| compte_a_vue_cbc | ING zichtrekening | 2024-09-08 | 74 | Tendance soutenue | 7.101 |
| compte_epargne | ING spaarrekening | 2024-09-08 | 32 | Tendance soutenue | 2.377 |
| compte_epargne_cbc | ING spaarrekening | 2024-09-08 | 65 | Tendance soutenue | 2.348 |
| compte_a_vue | ING zichtrekening | 2024-09-22 | 19 | Pic isolé | 4.71 |
| compte_a_vue_cbc | ING zichtrekening | 2024-09-22 | 49 | Pic isolé | 4.643 |
| compte_epargne | ING spaarrekening | 2024-12-29 | 25 | Pic isolé | 1.708 |
| compte_epargne_cbc | ING spaarrekening | 2024-12-29 | 52 | Pic isolé | 1.742 |
| epargne_pension | ING Star Fund | 2025-01-19 | 71 | Pic isolé | 4.708 |
| epargne_pension_cbc | ING Star Fund | 2025-01-19 | 71 | Pic isolé | 4.709 |
| investissement_courtage | ING Self Invest | 2025-02-16 | 3 | Pic isolé | 6.595 |
| compte_professionnel | Business'Bank ING | 2025-03-02 | 79 | Pic isolé | 10.904 |
| compte_professionnel_cbc | Business'Bank ING | 2025-03-02 | 76 | Pic isolé | 10.885 |
| investissement_courtage | ING Self Invest | 2025-05-25 | 3 | Pic isolé | 6.595 |
| pret_hypothecaire | prêt hypothécaire ING | 2025-05-25 | 75 | Pic isolé | 10.085 |
| pret_hypothecaire_cbc | prêt hypothécaire ING | 2025-05-25 | 64 | Pic isolé | 10.022 |
| assurance_habitation | ING Home Insurance | 2025-06-08 | 79 | Pic isolé | 16.155 |
| assurance_habitation_cbc | ING Home Insurance | 2025-06-08 | 64 | Pic isolé | 16.155 |
| compte_epargne | ING Orange Savings | 2025-08-10 | 19 | Pic isolé | 11.278 |
| compte_epargne_cbc | ING Orange Savings | 2025-08-10 | 38 | Pic isolé | 11.401 |
| compte_epargne | ING spaarrekening | 2025-08-24 | 23 | Pic isolé | 1.517 |
| compte_epargne_cbc | ING spaarrekening | 2025-08-24 | 48 | Pic isolé | 1.556 |
| compte_professionnel | compte professionnel ING | 2025-11-02 | 93 | Pic isolé | 12.636 |
| compte_professionnel_cbc | compte professionnel ING | 2025-11-02 | 90 | Pic isolé | 12.553 |
| pret_hypothecaire | ING hypothecair krediet | 2025-12-14 | 69 | Pic isolé | 9.396 |
| pret_hypothecaire_cbc | ING hypothecair krediet | 2025-12-14 | 59 | Pic isolé | 9.327 |
| pret_hypothecaire | prêt hypothécaire ING | 2026-01-25 | 60 | Pic isolé | 8.046 |
| pret_hypothecaire_cbc | prêt hypothécaire ING | 2026-01-25 | 52 | Pic isolé | 8.121 |
| compte_epargne | ING spaarrekening | 2026-02-22 | 25 | Pic isolé | 1.708 |
| compte_epargne_cbc | ING spaarrekening | 2026-02-22 | 51 | Pic isolé | 1.695 |
| carte_credit | ING kredietkaart | 2026-04-05 | 29 | Pic isolé | 7.248 |
| carte_credit_cbc | ING kredietkaart | 2026-04-05 | 29 | Pic isolé | 7.301 |
| epargne_pension | épargne pension ING | 2026-04-12 | 100 | Pic isolé | 16.148 |
| epargne_pension_cbc | épargne pension ING | 2026-04-12 | 100 | Pic isolé | 16.148 |
| pret_hypothecaire | ING hypothecair krediet | 2026-04-19 | 96 | Pic isolé | 13.106 |
| pret_hypothecaire_cbc | ING hypothecair krediet | 2026-04-19 | 83 | Pic isolé | 13.156 |
| app_mobile | ING Smart Banking | 2026-05-17 | 1 | Pic isolé | 11.402 |
| app_mobile_cbc | ING Smart Banking | 2026-05-17 | 4 | Pic isolé | 11.402 |
| compte_epargne | compte épargne ING | 2026-06-07 | 12 | Pic isolé | 8.17 |
| compte_epargne_cbc | compte épargne ING | 2026-06-07 | 25 | Pic isolé | 8.076 |
| compte_professionnel | Business'Bank ING | 2026-07-05 | 86 | Pic isolé | 11.878 |
| compte_professionnel_cbc | Business'Bank ING | 2026-07-05 | 83 | Pic isolé | 11.896 |
| carte_credit | carte de crédit ING | 2026-08-02 | 35 | Pic isolé | 9.472 |
| carte_credit_cbc | carte de crédit ING | 2026-08-02 | 35 | Pic isolé | 9.472 |
| assurance_habitation | assurance habitation ING | 2026-08-30 | 4 | Tendance soutenue | 7.181 |
| assurance_habitation_cbc | assurance habitation ING | 2026-08-30 | 6 | Tendance soutenue | 11.402 |
| compte_a_vue | compte à vue ING | 2026-08-30 | 2 | Tendance soutenue | 2.05 |
| compte_a_vue_cbc | compte à vue ING | 2026-08-30 | 5 | Tendance soutenue | 1.978 |
| compte_epargne | ING Orange Savings | 2026-08-30 | 16 | Pic isolé | 9.481 |
| compte_epargne | compte épargne ING | 2026-08-30 | 4 | Tendance soutenue | 2.633 |
| compte_epargne_cbc | ING Orange Savings | 2026-08-30 | 31 | Pic isolé | 9.282 |
| compte_epargne_cbc | compte épargne ING | 2026-08-30 | 8 | Tendance soutenue | 2.491 |
| compte_professionnel_cbc | compte professionnel ING | 2026-08-30 | 14 | Pic isolé | 1.87 |
| assurance_habitation | assurance habitation ING | 2026-09-06 | 8 | Tendance soutenue | 14.444 |
| assurance_habitation_cbc | assurance habitation ING | 2026-09-06 | 6 | Tendance soutenue | 11.402 |
| compte_a_vue | ING zichtrekening | 2026-09-06 | 7 | Pic isolé | 1.63 |
| compte_a_vue | compte à vue ING | 2026-09-06 | 2 | Tendance soutenue | 2.05 |
| compte_a_vue_cbc | ING zichtrekening | 2026-09-06 | 18 | Tendance soutenue | 1.596 |
| compte_a_vue_cbc | compte à vue ING | 2026-09-06 | 4 | Tendance soutenue | 1.568 |
| compte_epargne | compte épargne ING | 2026-09-06 | 4 | Tendance soutenue | 2.633 |
| compte_epargne_cbc | compte épargne ING | 2026-09-06 | 8 | Tendance soutenue | 2.491 |
| carte_credit | ING kredietkaart | 2026-09-13 | 7 | Pic isolé | 1.622 |
| compte_a_vue_cbc | ING zichtrekening | 2026-09-13 | 24 | Tendance soutenue | 2.186 |
| compte_epargne | compte épargne ING | 2026-09-13 | 4 | Tendance soutenue | 2.633 |
| compte_epargne_cbc | compte épargne ING | 2026-09-13 | 12 | Tendance soutenue | 3.806 |
