# 🍽️ Cloud Kitchen PNL Dashboard

An interactive **Profit & Loss analytics dashboard** for a cloud kitchen company, built with Python using **Plotly Dash** and **Streamlit**. The project covers end-to-end data analysis — from raw CSV ingestion to filtered, interactive dashboards with KPI cards, charts, pivot tables, and heatmaps.

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Dashboards](#dashboards)
  - [Dashboard 1 – Kitchen Level PNL](#dashboard-1--kitchen-level-pnl)
  - [Dashboard 2 – Variance Level PNL](#dashboard-2--variance-level-pnl)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Key Insights](#key-insights)

---

## Project Overview

This project was built as a data analyst case study. The goal was to take a raw P&L dataset for a cloud kitchen company and turn it into two interactive dashboards that help business stakeholders understand:

- How each kitchen store is performing across revenue, margins, and profitability
- Where food material wastage (variance) is occurring and how it relates to revenue size

Two versions of the dashboard were built — **Plotly Dash** and **Streamlit** — so stakeholders can choose the interface that works best for them.

---

## Dataset

The dataset (`Kittchen_PNL_Data.csv`) contains monthly P&L records for cloud kitchen stores.

| Attribute | Value |
|---|---|
| Total Records | 2,100 rows |
| Unique Stores | 344 kitchens |
| Cities | 5 |
| Time Period | Oct-23 to Mar-24 (6 months) |

**Key columns:**

| Column | Description |
|---|---|
| `STORE` | Kitchen store identifier |
| `MONTH` | Month of the record |
| `CITY` | City where the store operates |
| `ZONE MAPPING` | Zone within the city |
| `NET REVENUE` | Total revenue after discounts |
| `GROSS MARGIN` | Revenue minus raw material cost |
| `KITCHEN EBITDA` | Earnings before interest, tax, depreciation & amortisation |
| `VARIANCE` | Food material wastage (absolute value in ₹) |
| `IDEAL FOOD COST` | Theoretical food cost (used to derive CM) |
| `REVENUE COHORT` | Pre-assigned revenue bracket |
| `CM COHORT` | Contribution margin bracket |
| `EBITDA CATEGORY` | EBITDA +ve or EBITDA -ve |
| `EBITDA COHORT` | EBITDA margin bracket |

**Derived columns computed in code:**

| Column | Formula |
|---|---|
| `GM%` | `(GROSS MARGIN / NET REVENUE) × 100` |
| `CM` | `NET REVENUE − IDEAL FOOD COST` |
| `CM%` | `(CM / NET REVENUE) × 100` |
| `EBITDA%` | `(KITCHEN EBITDA / NET REVENUE) × 100` |
| `VARIANCE%` | `(VARIANCE / NET REVENUE) × 100` |
| `VARIANCE CATEGORY` | Bucketed from VARIANCE% |
| `REV BUCKET` | Bucketed from NET REVENUE (in lacs) |

---

## Dashboards

### Dashboard 1 – Kitchen Level PNL

A store-level P&L snapshot with the following filters:

**Dropdown filters (multi-select):**
- Store, Month, Revenue Cohort, CM Cohort, EBITDA Category, EBITDA Cohort, Zone, City

**Range slider filters:**
- EBITDA range (₹), CM range (₹), Net Revenue range (₹)

**Visuals:**
- KPI cards — Total Revenue, Avg GM%, Avg CM%, Total EBITDA, Store Count
- Bar chart — Net Revenue by Month
- Bar chart — EBITDA by Month (green = positive, red = negative)
- Scatter plot — GM% vs CM% coloured by EBITDA Category
- Pie chart — Store count by Revenue Cohort
- Kitchen Snapshot table — sortable, filterable, paginated

---

### Dashboard 2 – Variance Level PNL

Variance is the wastage of food material. This dashboard analyses variance across revenue categories.

**Top-level filters:** Variance Category, Month

**Variance buckets:**
| Category | Range |
|---|---|
| (a) | Var < 2% |
| (b) | Var 2% to 3% |
| (c) | Var 3% to 5% |
| (d) | Var > 5% |

**Revenue buckets:**
| Category | Range |
|---|---|
| (a) | Below INR 15 lacs |
| (b) | INR 15 to 25 lacs |
| (c) | INR 25 to 35 lacs |
| (d) | INR 35 to 45 lacs |
| (e) | Above INR 45 lacs |

**Sub-Dashboard 1 — Average Variance % by Revenue Category:**
- Pivot table: average VARIANCE% per revenue cohort per month
- Grand total row per month
- Line chart showing trend over months

**Sub-Dashboard 2 — Store Count by Revenue Range:**
- Pivot table: count of unique stores per revenue bucket per month
- Grand total row per month
- Heatmap visualisation

---

## Project Structure

```
cloud-kitchen-pnl-dashboard/
│
├── Kittchen_PNL_Data.csv          # Raw dataset
│
├── plotly_dashboard.py            # Plotly Dash app (Dashboard 1 + 2)
├── streamlit_dashboard.py         # Streamlit app (Dashboard 1 + 2)
│
├── kitchen_pnl_eda.ipynb          # Jupyter notebook — full EDA
│
├── requirements.txt               # All Python dependencies
│
├── project_approach.docx          # Project approach document
└── code_explanation.docx          # Code concepts and interview prep
```

---

## Setup & Installation

**Prerequisites:** Python 3.10 or higher

**1. Clone the repository**

```bash
git clone https://github.com/your-username/cloud-kitchen-pnl-dashboard.git
cd cloud-kitchen-pnl-dashboard
```

**2. (Optional but recommended) Create a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## How to Run

### Plotly Dash

```bash
python plotly_dashboard.py
```

Open your browser at: `http://localhost:8050`

---

### Streamlit

```bash
streamlit run streamlit_dashboard.py
```

Browser opens automatically at: `http://localhost:8501`

---

### EDA Notebook

```bash
jupyter notebook kitchen_pnl_eda.ipynb
```

---

## Tech Stack

| Library | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Primary language |
| pandas | 2.2.2 | Data loading, filtering, pivoting |
| numpy | 1.26.4 | Numerical computation |
| plotly | 5.22.0 | Interactive charts |
| dash | 2.17.0 | Web app framework (Plotly version) |
| streamlit | 1.35.0 | Web app framework (Streamlit version) |
| matplotlib | 3.8.4 | EDA charts in notebook |
| seaborn | 0.13.2 | Statistical visualisations in notebook |
| jupyter | 1.0.0 | EDA notebook environment |

---

## Key Insights

- 344 unique kitchen stores across 5 cities, with data spanning 6 months
- Majority of stores are **EBITDA positive**, indicating healthy overall profitability
- Average **Gross Margin** is consistently around 65–70% across months
- **Variance %** (food wastage as % of revenue) stays below 2% for all stores — well within the acceptable threshold
- Revenue is spread across three cohorts: INR 20–30 lacs, 30–40 lacs, and above 40 lacs
- No missing or duplicate data — the dataset is clean and production-ready
