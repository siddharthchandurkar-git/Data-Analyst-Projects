# SQL Data Warehouse Project

A modern data warehouse built in **SQL Server**, following the **Medallion Architecture** (Bronze → Silver → Gold). The project ingests raw CRM and ERP data from CSV files, cleans and standardizes it, and models it into a business-ready **Star Schema** for analytics, reporting, and ad-hoc analysis.

---

## 📐 Data Architecture

![Data Architecture](docs/data%20architecture.png)

The warehouse is built using SQL Server across three layers:

| Layer | Object Type | Purpose | Transformations |
|-------|-------------|---------|------------------|
| **Bronze** | Tables | Raw data, as-is from source | None (Truncate & Bulk Insert) |
| **Silver** | Tables | Cleaned, standardized data | Data cleansing, standardization, normalization, derived columns, enrichment |
| **Gold** | Views | Business-ready data | Integration, aggregation, business logic, star schema modeling |

Consumption layer: **BI & Reporting**, **Ad-hoc Analysis**, and **Machine Learning**.

**Sources:** CRM and ERP systems, delivered as CSV files.

---

## 🔄 Data Flow

![Data Flow](docs/data%20flow.png)

Data flows from source CSVs through each layer, one-to-one at the table level in Bronze/Silver, and is then combined into fact/dimension objects in Gold:

- `crm_sales_details` → `fact_sales`
- `crm_cust_info`, `erp_cust_az12`, `erp_loc_a101` → `dim_customers`
- `crm_prd_info`, `erp_px_cat_g1v2` → `dim_products`

---

## 🔗 Data Integration

![Data Integration](docs/data%20integeration.png)

Before modeling, the relationships between CRM and ERP tables were mapped by tracing shared keys:

- **CRM** (`crm_sales_details`, `crm_prd_info`, `crm_cust_info`) is the transactional core — sales/order records, product info, and customer info.
- **ERP** (`erp_px_cat_g1v2`, `erp_cust_az12`, `erp_loc_a101`) enriches CRM data — product categories, extra customer info (birthdate), and customer location (country).
- Keys connecting the two systems: `prd_key` ↔ `id` (category), and `cst_key` ↔ `cid` (customer, in both `erp_cust_az12` and `erp_loc_a101`).

---

## ⭐ Data Model (Star Schema)

![Star Schema](docs/Sales_data_model(star_schema).png)

The Gold layer exposes a classic star schema:

- **`gold.fact_sales`** — grain: one row per order line. Contains `order_number`, foreign keys (`product_key`, `customer_key`), dates (`order_date`, `shipping_date`, `due_date`), and measures (`sales_amount`, `quantity`, `price`).
- **`gold.dim_customers`** — surrogate key `customer_key`, customer demographics (name, gender, marital status, birthdate, country).
- **`gold.dim_products`** — surrogate key `product_key`, product attributes (name, category, subcategory, cost, product line, maintenance flag).

**Business rule:** `Sales = Quantity * Price`

---

## 🛠️ What I Did (Step by Step)

### 1. Explored & Planned
Examined the source tables and planned the end-to-end data flow before writing any code — mapping how CRM and ERP CSVs would move through Bronze → Silver → Gold, and how tables would eventually connect via shared keys.

### 2. Examined the Raw Data
Reviewed the raw CRM and ERP CSV files (`cust_info`, `prd_info`, `sales_details` from CRM; `loc_a101`, `cust_az12`, `px_cat_g1v2` from ERP) to understand structure, data types, and quality issues before designing the Bronze schema.

### 3. Built the Bronze Layer
- **DDL:** Created raw tables mirroring the source CSV structure exactly — no transformations, no business logic. Each table is dropped and recreated if it already exists (`IF OBJECT_ID ... DROP TABLE`).
- **Load:** Built `bronze.load_bronze`, a stored procedure that truncates each Bronze table and reloads it using `BULK INSERT` from the source CSVs, with `TRY...CATCH` error handling and load-duration logging per table.

### 4. Built the Silver Layer
- **DDL:** Created Silver tables with the same core columns as Bronze, plus a `dwh_create_date` metadata column (`DATETIME2 DEFAULT GETDATE()`) to track when each record was loaded into the warehouse.
- **Transform & Load:** Built `silver.load_silver`, which truncates and reloads each Silver table with cleaned data:
  - **`crm_cust_info`** — trimmed names, standardized `marital_status` (`S`/`M` → `Single`/`Married`) and `gndr` (`F`/`M` → `Female`/`Male`), deduplicated by `cst_id` keeping the most recent record via `ROW_NUMBER() ... ORDER BY cst_create_date DESC`.
  - **`crm_prd_info`** — split `prd_key` into `cat_id` (category, matched to ERP) and a cleaned `prd_key`; standardized `prd_line` codes into readable values (`M` → `Mountain`, `R` → `Road`, `S` → `Other Sales`, `T` → `Touring`); handled null costs; derived `prd_end_dt` using `LEAD()` (one day before the next start date).
  - **`crm_sales_details`** — converted integer date fields (`YYYYMMDD`) into proper `DATE` values with validity checks; recalculated `sls_sales` when missing, zero, or inconsistent with `quantity * price`; derived `sls_price` when missing or invalid.
  - **`erp_cust_az12`** — stripped `NAS` prefix from `cid` to align with CRM's customer key; nulled out future birthdates; standardized gender values.
  - **`erp_loc_a101`** — removed dashes from `cid`; standardized country codes (`DE` → `Germany`, `US`/`USA` → `United States`, blank/null → `n/a`).
  - **`erp_px_cat_g1v2`** — loaded as-is (already clean).

### 5. Integrated the Silver Tables
Traced and parsed the keys linking CRM and ERP tables (`prd_key` ↔ category `id`, `cst_key`/`cst_id` ↔ `cid`) so the tables could be joined consistently and correctly in the next layer.

### 6. Built the Gold Layer (Star Schema)
Created views (no physical load — Gold is transformation-only) that integrate, aggregate, and apply business logic:

- **`gold.dim_customers`** — joins `crm_cust_info` with `erp_cust_az12` (birthdate) and `erp_loc_a101` (country) on the customer key; generates a surrogate `customer_key` via `ROW_NUMBER()`; applies a gender fallback rule (CRM is the primary source, falls back to ERP when CRM value is `n/a`).
- **`gold.dim_products`** — joins `crm_prd_info` with `erp_px_cat_g1v2` on category id; generates a surrogate `product_key`; filters out historical product versions (`WHERE prd_end_dt IS NULL`) to keep only current products.
- **`gold.fact_sales`** — joins `crm_sales_details` with the two dimension views to resolve surrogate keys (`product_key`, `customer_key`) alongside order dates and sales measures.

### 7. Modeled with Facts & Dimensions
Finalized the Gold layer as a proper star schema — one fact table (`fact_sales`) surrounded by conformed dimensions (`dim_customers`, `dim_products`) — ready to plug into BI tools, ad-hoc SQL analysis, or ML pipelines.

---

## 📁 Repository Structure

```
sql-data-warehouse-project/
│
├── datasets/                      # Raw source CSV files
│   ├── source_crm/
│   │   ├── cust_info.csv
│   │   ├── prd_info.csv
│   │   └── sales_details.csv
│   └── source_erp/
│       ├── loc_a101.csv
│       ├── cust_az12.csv
│       └── px_cat_g1v2.csv
│
├── scripts/
│   ├── bronze/
│   │   ├── ddl_bronze.sql         # Bronze table definitions
│   │   └── bronze_bulk_load.sql   # Bulk load from CSVs
│   ├── silver/
│   │   ├── ddl_silver.sql         # Silver table definitions
│   │   └── silver_transform_and Load.sql   # Cleaning & transformation logic
│   └── gold/
│       └── ddl_gold.sql           # Gold star-schema views
│
├── docs/
│   ├── data_architecture.png
│   ├── data_flow.png
│   ├── data_integeration.png
│   └── Sales_data_model_star_schema_.png
│
└── README.md
```

---

## ▶️ How to Run

1. Run `ddl_bronze.sql` to create the Bronze tables.
2. Run `proc_load_bronze.sql` to create the `bronze.load_bronze` procedure, then execute it: `EXEC bronze.load_bronze;`
3. Run `ddl_silver.sql` to create the Silver tables.
4. Run `proc_load_silver.sql` to create the `silver.load_silver` procedure, then execute it: `EXEC silver.load_silver;`
5. Run `ddl_gold.sql` to create the Gold layer views.
6. Query `gold.fact_sales`, `gold.dim_customers`, and `gold.dim_products` directly, or connect a BI tool.

> **Note:** Update the file paths in `proc_load_bronze.sql` (currently `D:\sql-data-warehouse-project\datasets\...`) to match your local environment.

---

## 🧰 Tech Stack

- **Database:** Microsoft SQL Server
- **Architecture:** Medallion (Bronze / Silver / Gold)
- **Data Modeling:** Star Schema (Kimball-style facts & dimensions)
- **Sources:** CRM & ERP systems (flat-file CSV extracts)
