# IPL Cricket Performance Analysis: Exploring Cricket Performance Through Statistical Analysis and Data Visualisation

## Project overview

This undergraduate project analyses Indian Premier League (IPL) batting performance using ball-by-ball data from **Cricsheet**. The workflow moves from JSON extraction to cleaned CSVs, exploratory analysis, inferential statistics, and visualisation—including an interactive player view in the final notebook.

## Problem statement

Professional T20 leagues generate large volumes of structured match data. The project investigates how batting outcomes (runs, strike rate, phase scoring, and consistency) vary across players and seasons, and how key batting metrics relate statistically.

## Objectives

- Collect and parse Cricsheet IPL JSON match files.
- Build player-season and innings-level batting datasets.
- Clean and validate data for analysis.
- Explore top performances, season trends, and phase-wise scoring.
- Test correlations between runs and strike rate (Pearson and Spearman).
- Visualise performance patterns and export figures for reporting.

## Dataset source

- **Provider:** [Cricsheet](https://cricsheet.org/)
- **Download:** [IPL JSON ZIP](https://cricsheet.org/downloads/ipl_json.zip)
- **Format:** One JSON file per match with ball-by-ball `deliveries`.

## Technologies

Python 3, Pandas, NumPy, SciPy, Matplotlib, Seaborn, Requests, Jupyter, ipywidgets, Streamlit, Plotly.

## Project structure

```
IPL_Cricket_Performance_Analysis/
├── data/
│   ├── raw/                 # ipl_json.zip (after Notebook 01)
│   └── processed/           # CSV outputs from collection & cleaning
├── notebooks/
│   ├── 01_Data_Collection.ipynb
│   ├── 02_Data_Preprocessing.ipynb
│   ├── 03_Exploratory_Data_Analysis.ipynb
│   ├── 04_Statistical_Analysis.ipynb
│   └── 05_Data_Visualization.ipynb
├── outputs/
│   └── figures/             # Saved charts from Notebook 05 (and stats heatmap from 04)
├── ipl_dashboard.py         # Optional IPL web dashboard (Streamlit)
├── requirements.txt
├── README.md
└── .gitignore
```

## Notebooks

| Notebook | Purpose |
|----------|---------|
| **01 — Data Collection** | Download (if needed), verify ZIP, season table, `extract_ipl_innings()`, original player-season summary, save `IPL_Batting_Statistics.csv` and `IPL_Batting_Innings.csv`. |
| **02 — Data Preprocessing** | Load CSVs, inspect structure, handle duplicates/missing values, standardise types, recalculate rates, save cleaned CSVs. |
| **03 — EDA** | Descriptive stats, top scorers, season summaries, sixes and strike-rate leaders (100+ balls rule). |
| **04 — Statistical Analysis** | Pearson/Spearman (Runs vs Strike_Rate), correlation matrix, heatmap. |
| **05 — Visualisation** | Ten chart types from the original analysis + ipywidgets player dashboard (Runs, Average, SR, Sixes by season). |

## Methodology (summary)

**Collection:** Ball-by-ball JSON is parsed per innings; batting stats are accumulated with Powerplay (overs 0–5), Middle (6–14), and Death (15+) phases. Player-season rows merge aggregated innings with squad appearances (`Matches_Played`, `Teams_Played`).

**Preprocessing:** Duplicate removal, name trimming, numeric seasons, date parsing, super-over flags, and safe division for averages and percentages.

**Statistics:** SciPy `pearsonr` and `spearmanr` on player-season Runs and Strike_Rate; full metric correlation matrix.

**Visualisation:** Matplotlib/Seaborn charts saved under `outputs/figures/` at 300 dpi.

**Season labels:** The `Season` field is taken from Cricsheet match JSON as in the original course notebook (not re-mapped to calendar IPL years). In this download, **2007** matches were played in calendar **2008**, and **2009** can bundle more than one edition (e.g. 2009–2010). All notebooks and CSVs keep those values so outputs stay consistent with the source workflow.

## Install requirements

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name ipl-analysis
```

## Run order

1. `notebooks/01_Data_Collection.ipynb` — creates processed CSVs (skips download if `data/raw/ipl_json.zip` already exists).
2. `02_Data_Preprocessing.ipynb` — requires outputs from 01.
3. `03_Exploratory_Data_Analysis.ipynb` — uses `*_Cleaned.csv` files.
4. `04_Statistical_Analysis.ipynb`
5. `05_Data_Visualization.ipynb`

Open Jupyter from the **project root** so `Path.cwd()` resolves correctly, or run with the kernel started in that directory.

## Optional Streamlit UI

After notebooks 01–02:

```bash
streamlit run ipl_dashboard.py
```

Theme and UI: `.streamlit/config.toml` (cream + navy analytics layout in `ipl_dashboard.py`).

## Expected outputs

**`data/processed/`**

- `IPL_Batting_Statistics.csv`, `IPL_Batting_Innings.csv`
- `IPL_Batting_Statistics_Cleaned.csv`, `IPL_Batting_Innings_Cleaned.csv`

**`outputs/figures/`** (examples)

- `top_10_run_scorers.png`, `season_wise_runs.png`, `top_10_six_hitters.png`, `top_10_strike_rates.png`
- `average_vs_strike_rate.png`, `season_runs_boxplot.png`, `batting_correlation_heatmap.png`
- `phase_wise_runs_pie.png`, `batting_position_violin.png`
- `batting_correlation_heatmap_stats.png` (from Notebook 04)

## Academic note

The analysis logic follows the original course notebook (`pythondsehcricket.ipynb`), split into modular notebooks for marking and reproducibility.