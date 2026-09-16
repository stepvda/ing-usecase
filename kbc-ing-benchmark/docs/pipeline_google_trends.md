# Pipeline Google Trends — ING vs KBC vs CBC

Document de passation technique, destiné à un agent qui doit comprendre et
pouvoir opérer ce pipeline sans contexte préalable. Décrit uniquement le
pipeline **Trends** (collecte, anomalies, visualisation, export). Le
pipeline `campaigns/` (rapprochement avec des campagnes publicitaires
réelles) est construit **en aval** de celui-ci, en lecture seule sur ses
tables — il est mentionné en fin de document mais pas détaillé ici.

## 1. Objectif

Mesurer, par produit bancaire (compte à vue, carte de crédit, app mobile,
etc.), l'intérêt de recherche Google en Belgique pour trois banques — **ING**,
**KBC** et **CBC** — sur 5 ans, et détecter automatiquement les pics
anormaux d'intérêt de recherche. Ces pics sont les dates candidates à
vérifier manuellement (le pipeline ne collecte aucune donnée publicitaire
lui-même).

**Fait métier clé** : CBC Banque & Assurance est la marque commerciale de
KBC Group pour la Wallonie et Bruxelles francophone — l'équivalent de la
marque KBC en Flandre. Même groupe, marques distinctes, recherches Google
distinctes. Le pipeline les traite comme 3 entités de recherche
indépendantes, mais garde la trace de leur lien de parenté à certains
endroits précis (voir section 7).

## 2. Vue d'ensemble du flux

```
config.py (référentiel produits)
        │
        ▼
collectors/trends_collector.py  ──►  pytrends (API Google Trends)
        │
        ▼
benchmark.db : table trends_data (+ data/csv/*.csv, un CSV par fiche)
        │
        ▼
analysis/anomaly_detection.py
        │
        ▼
benchmark.db : table anomalies
        │
        ├──► app.py (Streamlit, visualisation)
        └──► export/*.py (Markdown + CSV, données à plat)
```

Chaque étape lit dans SQLite et/ou écrit dans SQLite — il n'y a pas
d'état caché ailleurs. La base est `benchmark.db` à la racine du projet
(`kbc-ing-benchmark/benchmark.db`), absente du dépôt git (regénérée
localement).

## 3. Le référentiel produits (`config.py`)

Tout part de `PRODUCTS`, une liste de **18 fiches** (`dict`), chacune avec :

```python
{
    "product_id": "compte_professionnel",       # identifiant stable, clé primaire logique
    "product_label": "Compte professionnel / indépendant",  # libellé humain (FR)
    "terms": [
        {"term": "KBC zakelijke rekening", "bank": "KBC", "language": "nl"},
        {"term": "compte professionnel ING", "bank": "ING", "language": "fr"},
        ...
    ],
}
```

**Contrainte dure : au maximum 5 `terms` par fiche.** C'est la limite
imposée par l'API `pytrends` (paramètre `kw_list` d'un appel
`build_payload`). `trends_collector.py` lève une exception si une fiche
en a plus.

Les 18 fiches se répartissent en 3 groupes :

1. **9 fiches "KBC vs ING"** (`compte_professionnel`, `compte_a_vue`,
   `compte_epargne`, `investissement_courtage`, `app_mobile`,
   `carte_credit`, `epargne_pension`, `assurance_habitation`,
   `pret_hypothecaire`) — chacune compare les termes KBC et ING pour ce
   produit.
2. **8 fiches "CBC vs ING"** (mêmes noms de produit, suffixées `_cbc`,
   ex. `compte_professionnel_cbc`) — même principe mais avec les termes
   CBC à la place de KBC. Il n'existe **pas** de fiche
   `investissement_courtage_cbc` : CBC n'a pas d'offre de courtage propre
   (Bolero est une plateforme partagée par tout KBC Group), donc pas de
   terme CBC distinct à interroger.
3. **1 fiche `marque_generique`** : les 3 marques seules (`KBC`, `ING`,
   et le topic CBC — voir section 7), sans contexte produit. C'est la
   seule fiche à contenir les 3 banques dans la même requête.

`GEO = "BE"` et `TIMEFRAME = "today 5-y"` sont fixes pour tout le
pipeline (mêmes constantes utilisées partout, jamais codées en dur
ailleurs).

## 4. Collecte (`collectors/trends_collector.py`)

**Principe** : une fiche = un appel `pytrends.build_payload(kw_list, ...)`
+ `interest_over_time()`. Les valeurs Google Trends (0-100) ne sont
comparables **qu'à l'intérieur d'un même appel** — c'est pour ça que la
structure est "une fiche = une requête indépendante" plutôt que 18 appels
mélangés : comparer une valeur de la fiche `app_mobile` à une valeur de
`carte_credit` n'a aucun sens.

**Granularité réelle** : Google Trends bascule automatiquement en
hebdomadaire au-delà d'environ 270 jours de plage — sur 5 ans, on obtient
donc des points **hebdomadaires** (~262 points par terme), jamais
journaliers ni mensuels, quel que soit ce que le nom `TIMEFRAME` suggère.

**Robustesse réseau** (Google Trends limite agressivement le débit) :
- séquentiel strict, aucune parallélisation ;
- pause fixe de `MIN_DELAY_SECONDS = 60` s après **chaque** fiche traitée
  avec succès ;
- sur erreur 429, backoff exponentiel avec jitter : jusqu'à
  `MAX_RETRIES = 5` tentatives, délai initial `INITIAL_BACKOFF_SECONDS = 30` s
  (doublé + jitter aléatoire à chaque échec) ;
- **reprenable** : avant de traiter une fiche, le script vérifie si
  `trends_data` contient déjà des lignes pour ce `product_id` — si oui, il
  la saute. Un lancement interrompu peut être relancé tel quel, seules les
  fiches manquantes sont retéléchargées. Piège : si on modifie les termes
  d'une fiche déjà collectée (ex. ajout d'un terme), il faut supprimer ses
  lignes existantes (`DELETE FROM trends_data WHERE product_id = ...`)
  avant de relancer, sinon la fiche est sautée avec l'ancien contenu.

**Sorties** : un CSV par fiche dans `data/csv/{product_id}.csv` (colonne
`Time` + une colonne par terme, format brut pytrends) **et** une écriture
en base dans `trends_data` au format long (une ligne par
terme × date), via upsert sur `UNIQUE(product_id, term, date)`.

Durée réelle observée pour une collecte complète à froid (18 fiches) :
entre ~9 minutes (sans rate-limit) et ~25 minutes (avec 429 fréquents).

## 5. Schéma de base (`db/schema.sql`)

```sql
CREATE TABLE trends_data (
    product_id TEXT NOT NULL, product_label TEXT NOT NULL, term TEXT NOT NULL,
    bank TEXT NOT NULL, language TEXT NOT NULL, date TEXT NOT NULL, value INTEGER NOT NULL,
    UNIQUE (product_id, term, date)
);

CREATE TABLE products (
    product_id TEXT PRIMARY KEY, product_label TEXT NOT NULL, term_count INTEGER NOT NULL
);

CREATE TABLE anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL, term TEXT NOT NULL, bank TEXT NOT NULL,
    date TEXT NOT NULL, value INTEGER NOT NULL,
    anomaly_type TEXT NOT NULL CHECK (anomaly_type IN ('isolated_spike', 'sustained_trend')),
    deviation_score REAL NOT NULL,
    UNIQUE (product_id, term, date)
);
```

Points d'attention :
- `bank` est un `TEXT` libre, **sans contrainte `CHECK`** — les valeurs
  réelles utilisées sont `'KBC'`, `'CBC'`, `'ING'`, mais rien n'empêche
  d'en insérer une autre en base. Ne pas supposer une énumération stricte
  côté SQL ; elle n'existe que dans `config.py` (implicitement, via les
  `terms` déclarés) et dans le code applicatif.
- `products` est un simple annuaire (label + nombre de termes), synchronisé
  automatiquement par `trends_collector.py` à chaque run — pas de logique
  métier dessus.
- `date` est stockée en `TEXT` format `YYYY-MM-DD` partout (jamais de type
  `DATE` natif SQLite, qui n'existe pas).
- État réel constaté au moment de la rédaction : 18 602 lignes dans
  `trends_data`, 473 dans `anomalies`, 18 dans `products`, plage de dates
  2021-09-12 → 2026-09-13.

## 6. Détection d'anomalies (`analysis/anomaly_detection.py`)

Exécutée comme étape séparée (`python analysis/anomaly_detection.py`),
**jamais** recalculée à l'affichage — l'app Streamlit lit uniquement la
table déjà peuplée.

Pour chaque série `(product_id, term)` (donc pour chaque terme
individuellement — KBC et ING d'une même fiche ne sont jamais comparés
entre eux ici, seulement chacun contre sa propre historique) :

1. `overall_mean`, `overall_std` = moyenne et écart-type de la série
   entière. Si `overall_std == 0` (série constante, typiquement des zéros
   plats), la série est ignorée — aucune anomalie possible.
2. `seasonal_mean` = moyenne des valeurs groupées par mois calendaire
   (`date.dt.month`), sur toutes les années disponibles — profil de
   saisonnalité de référence pour ce terme.
3. Un point est **candidat anomalie** s'il vérifie **simultanément** :
   - `z_score = (valeur - overall_mean) / overall_std >= Z_SCORE_THRESHOLD` (1.5)
   - `valeur / seasonal_mean[mois] >= SEASONAL_RATIO_THRESHOLD` (1.3)
4. Les points candidats consécutifs (mêmes index adjacents dans la série
   triée par date) sont regroupés en "runs" :
   - run de longueur 1 → `anomaly_type = 'isolated_spike'`
   - run de longueur ≥ 2 → `anomaly_type = 'sustained_trend'`
5. `deviation_score` stocké = le `z_score` de ce point précis (pas une
   moyenne du run).

Le script fait un `DELETE FROM anomalies` puis réinsère tout à chaque
run — **les `id` ne sont pas stables d'un run à l'autre**. Toute table qui
référence `anomalies.id` par clé étrangère (c'est le cas de
`campaign_anomaly_matches` dans le pipeline aval) doit être régénérée
après un nouveau run de détection.

## 7. Le cas CBC : désambiguïsation Google Trends

Problème découvert empiriquement : la chaîne `"CBC"` seule est polluée au
niveau international sur Google Trends — elle capte aussi *Carcinome
basocellulaire*, *CBC News* / Radio-Canada, *CBC Kids*, et *hémogramme*
(numération formule sanguine), même avec `geo='BE'`.

Test réalisé via `pytrends.suggestions()` puis comparaison de couverture
réelle (`interest_over_time()`, geo=BE, 5 ans) :

| Formulation | Type | Moyenne | Points non-nuls |
|---|---|---|---|
| `"CBC"` | string brute | 71.6 | 262/262 (mais pollué) |
| `"CBC Banque"` | string | 7.3 | 262/262 |
| `"CBC Banque et Assurance"` | string | 0.008 | 1/262 (quasi vide, trop spécifique) |
| `/g/1z3t2x3c8` | **topic Knowledge Graph** | **54.2** | **262/262** |

`/g/1z3t2x3c8` est le topic Knowledge Graph "CBC Banque & Assurance"
(type "Sujet"), retourné en premier résultat par
`pytrends.suggestions(keyword="CBC Banque")`. C'est le seul terme CBC du
pipeline à être un **topic mid** plutôt qu'une chaîne de recherche brute
— tous les autres termes (KBC, ING, et les termes produits CBC comme
`"compte à vue CBC"`) sont des chaînes classiques passées telles quelles à
`pytrends`.

Conséquence pratique : la colonne `term` de `trends_data`/`anomalies`
contient littéralement la chaîne `"/g/1z3t2x3c8"` pour ce terme précis (
c'est ce que `pytrends` retourne comme nom de colonne pour un topic).
Pour l'affichage humain, `config.TERM_DISPLAY_LABELS` fait la
correspondance :

```python
TERM_DISPLAY_LABELS = {"/g/1z3t2x3c8": "CBC Banque & Assurance"}
```

Toute UI ou export qui affiche un `term` doit passer par
`TERM_DISPLAY_LABELS.get(term, term)` (fonction `display_term()`,
dupliquée à l'identique dans `app.py` et `export/export_common.py`) —
sinon ce terme précis s'affiche comme un identifiant technique illisible.

**KBC et CBC dans le code** : en dehors de ce topic mid, KBC et CBC sont
traités comme deux valeurs de `bank` totalement indépendantes dans tout le
pipeline Trends (aucun regroupement). Le regroupement "KBC = CBC" n'existe
que dans le pipeline `campaigns/` en aval (voir section 9), pas ici.

## 8. Visualisation (`app.py`, Streamlit)

`streamlit run app.py` (port par défaut 8501). Lecture seule sur
`trends_data` et `anomalies`, via `@st.cache_data`.

Un onglet par fiche (18 onglets, ordre = ordre de `config.PRODUCTS`).
Chaque onglet :
- un graphique Plotly : une courbe par terme de la fiche, couleur par
  index de terme (palette fixe à 5 couleurs), style de trait par banque
  (`solid` KBC, `dash` ING, `dashdot` CBC — dict `BANK_DASH`), marqueurs
  distincts pour `isolated_spike` (losange) vs `sustained_trend` (étoile) ;
- un tableau des anomalies de cette fiche ;
- un tableau de données brutes filtrable (par terme, par période).

Aucune écriture en base depuis cette app — purement consultatif.

## 9. Exports (`export/`)

Chaque script `export_*.py` est un point d'entrée fin qui appelle
`export_common.run_export(bank, ...)` ou `run_export_all(...)` :

| Script | Filtre | Sorties |
|---|---|---|
| `export_kbc_data.py` | `bank='KBC'` | `kbc_trends_data.csv`, `kbc_data_export.md` |
| `export_ing_data.py` | `bank='ING'` | `ing_trends_data.csv`, `ing_data_export.md` |
| `export_cbc_data.py` | `bank='CBC'` | `cbc_trends_data.csv`, `cbc_data_export.md` |
| `export_all_data.py` | aucun | `all_trends_data.csv`, `all_data_export.md` |

Chaque `.md` contient : méthodologie (source, granularité, seuils de
détection), liste des fiches concernées avec leurs termes, référence au
CSV joint, et un tableau complet des anomalies détectées. Le CSV contient
la série `trends_data` brute correspondante (toutes les colonnes de la
table, sans transformation).

Ces exports sont la donnée d'entrée officielle pour tout pipeline externe
qui veut consommer ce projet sans toucher à SQLite directement.

## 10. Comment tout relancer depuis zéro

```bash
cd kbc-ing-benchmark
pip install -r requirements.txt

python collectors/trends_collector.py      # ~10-25 min, reprenable si interrompu
python analysis/anomaly_detection.py       # quelques secondes

python export/export_kbc_data.py
python export/export_ing_data.py
python export/export_cbc_data.py
python export/export_all_data.py

streamlit run app.py                       # UI sur http://localhost:8501
```

Pour ajouter une fiche produit ou un terme : éditer `config.PRODUCTS`,
relancer `trends_collector.py` (skip automatique de ce qui existe déjà,
voir section 4) puis `anomaly_detection.py` et les exports.

## 11. Pièges connus (déjà rencontrés, à ne pas re-découvrir)

- **Encodage console Windows** : les caractères accentués (`é`, `à`...)
  s'affichent parfois comme `�` dans un terminal Git Bash/PowerShell. Les
  données elles-mêmes sont en UTF-8 correct en base — c'est uniquement un
  problème d'affichage du terminal, vérifié à plusieurs reprises en
  écrivant dans un fichier puis en le relisant.
- **`pytrends.suggestions()` et bare strings pour des noms de marque
  courts/ambigus** : toujours vérifier la désambiguïsation Knowledge Graph
  avant d'ajouter un nouveau terme de marque générique (voir méthode
  section 7) — un nom court peut être pollué sans que le volume élevé ne
  le laisse deviner.
- **Limite pytrends de 5 termes/requête** : toute nouvelle fiche ou tout
  ajout de terme à une fiche existante doit être vérifié contre cette
  limite avant collecte (le script lève une exception si dépassée, mais
  autant l'anticiper).
- **`ON CONFLICT` vs suppression complète** : `trends_data` et `products`
  utilisent un upsert (les anciennes lignes non concernées survivent).
  `anomalies` est entièrement vidée et régénérée à chaque run de
  `anomaly_detection.py` (voir section 6) — les deux tables n'ont pas la
  même politique de rafraîchissement, à garder en tête si on modifie l'un
  des deux scripts.

## 12. Ce qui n'est PAS dans ce pipeline

- Aucune collecte de données publicitaires (Meta Ad Library, Google Ads
  Transparency Center, presse) — volontairement hors périmètre.
- Le rapprochement anomalies ↔ campagnes réelles et le scoring d'impact
  vivent dans `campaigns/` (tables `campaigns`, `campaign_anomaly_matches`,
  `campaign_scores`, app Streamlit séparée sur le port 8502). Ce module
  **lit** `anomalies` en lecture seule mais ne fait partie d'aucune étape
  décrite ci-dessus — c'est un pipeline distinct, construit après coup,
  avec son propre catalogue de campagnes saisi manuellement (pas de
  scraping automatisé).
