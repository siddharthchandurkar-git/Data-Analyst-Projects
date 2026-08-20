
# Mobility Services Data Engineering Pipeline

An end-to-end **data engineering pipeline for the Mobility Services / Ride-Hailing domain**, built using **Databricks, PySpark, Delta Lake, dbt, Jinja, and dimensional modeling**.

The project demonstrates how raw operational data from multiple CSV sources can be ingested, processed through a **Bronze → Silver → Gold medallion architecture**, and transformed into analytics-ready fact and dimension tables with **incremental processing, Delta upserts, reusable PySpark transformations, dbt incremental models, and SCD Type 2 history tracking**.

---

## 📌 Project Overview

The project simulates a mobility services platform containing information about:

* Customers
* Drivers
* Trips
* Locations
* Vehicles
* Payments

The raw datasets were initially provided as CSV files. These datasets were loaded into Databricks and organized into a layered architecture:

```text
Raw CSV Files
      │
      ▼
┌─────────────────────┐
│     Source Layer    │
│  pysparkdbt.source  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Bronze Layer     │
│   Raw/Ingested Data │
└──────────┬──────────┘
           │
           ▼
┌───────────────────────────────┐
│          Silver Layer         │
│                               │
│ PySpark Transformations       │
│ + Delta Upserts               │
│ + Deduplication               │
│ + Incremental dbt Model       │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│           Gold Layer          │
│                               │
│       dbt Dimensional Model   │
│                               │
│ FactTrips                     │
│ DimCustomers                  │
│ DimDrivers                    │
│ DimLocations                  │
│ DimPayments                   │
│ DimVehicles                   │
└───────────────────────────────┘
```

The final Gold layer is available in the Databricks catalog and provides an analytical model consisting of fact and dimension tables.

---

# 🏗️ Architecture

The project follows the **Medallion Architecture** pattern.

```text
                    RAW DATA
                       │
          ┌────────────┴────────────┐
          │                         │
     customers.csv             drivers.csv
     trips.csv                 locations.csv
     vehicles.csv              payments.csv
          │                         │
          └────────────┬────────────┘
                       ▼
              ┌─────────────────┐
              │ SOURCE SCHEMA   │
              │ pysparkdbt      │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ BRONZE SCHEMA   │
              │ Raw Ingestion   │
              └────────┬────────┘
                       ▼
        ┌──────────────────────────────┐
        │        SILVER LAYER          │
        │                              │
        │ PySpark Transformations      │
        │ Deduplication                │
        │ CDC-based processing         │
        │ Delta MERGE / Upsert         │
        │                              │
        │ +                            │
        │                              │
        │ dbt Incremental Trips Model  │
        └──────────────┬───────────────┘
                       ▼
              ┌─────────────────┐
              │   GOLD / dbt    │
              │                 │
              │ SCD Type 2      │
              │ Fact + Dims     │
              └────────┬────────┘
                       ▼
              ANALYTICS-READY DATA
```

---

# 📂 Source Data

The project contains six source datasets.

## 1. Customers

| Column                   | Description                |
| ------------------------ | -------------------------- |
| `customer_id`            | Unique customer identifier |
| `first_name`             | Customer first name        |
| `last_name`              | Customer last name         |
| `email`                  | Customer email             |
| `phone_number`           | Customer phone number      |
| `city`                   | Customer city              |
| `signup_date`            | Customer signup date       |
| `last_updated_timestamp` | CDC/update timestamp       |

---

## 2. Drivers

| Column                   | Description              |
| ------------------------ | ------------------------ |
| `driver_id`              | Unique driver identifier |
| `first_name`             | Driver first name        |
| `last_name`              | Driver last name         |
| `phone_number`           | Driver phone number      |
| `vehicle_id`             | Associated vehicle       |
| `driver_rating`          | Driver rating            |
| `city`                   | Driver city              |
| `last_updated_timestamp` | CDC/update timestamp     |

---

## 3. Trips

| Column                   | Description                   |
| ------------------------ | ----------------------------- |
| `trip_id`                | Unique trip identifier        |
| `driver_id`              | Driver associated with trip   |
| `customer_id`            | Customer associated with trip |
| `vehicle_id`             | Vehicle used                  |
| `trip_start_time`        | Trip start timestamp          |
| `trip_end_time`          | Trip end timestamp            |
| `start_location`         | Starting location             |
| `end_location`           | Destination                   |
| `distance_km`            | Trip distance                 |
| `fare_amount`            | Trip fare                     |
| `payment_method`         | Payment method                |
| `trip_status`            | Trip status                   |
| `last_updated_timestamp` | CDC/update timestamp          |

---

## 4. Locations

| Column                   | Description                |
| ------------------------ | -------------------------- |
| `location_id`            | Unique location identifier |
| `city`                   | City                       |
| `state`                  | State                      |
| `country`                | Country                    |
| `latitude`               | Latitude                   |
| `longitude`              | Longitude                  |
| `last_updated_timestamp` | CDC/update timestamp       |

---

## 5. Vehicles

| Column                   | Description               |
| ------------------------ | ------------------------- |
| `vehicle_id`             | Unique vehicle identifier |
| `license_plate`          | Vehicle registration      |
| `model`                  | Vehicle model             |
| `make`                   | Vehicle manufacturer      |
| `year`                   | Manufacturing year        |
| `vehicle_type`           | Vehicle category          |
| `last_updated_timestamp` | CDC/update timestamp      |

---

## 6. Payments

| Column                   | Description               |
| ------------------------ | ------------------------- |
| `payment_id`             | Unique payment identifier |
| `trip_id`                | Associated trip           |
| `customer_id`            | Associated customer       |
| `payment_method`         | Payment method            |
| `payment_status`         | Payment status            |
| `amount`                 | Transaction amount        |
| `transaction_time`       | Transaction timestamp     |
| `last_updated_timestamp` | CDC/update timestamp      |

---

# 🛠️ Technology Stack

| Technology             | Purpose                                             |
| ---------------------- | --------------------------------------------------- |
| **Databricks**         | Data engineering platform and execution environment |
| **PySpark**            | Distributed data transformation                     |
| **Delta Lake**         | ACID storage and MERGE/upsert operations            |
| **Python**             | Reusable and modular transformation logic           |
| **dbt**                | SQL-based transformation and dimensional modeling   |
| **Jinja**              | Dynamic SQL generation and dbt templating           |
| **dbt Snapshots**      | Historical change tracking / SCD Type 2             |
| **Databricks Catalog** | Organization and management of data layers          |

---

# 🥉 Bronze Layer

The first stage of the pipeline is the Bronze layer.

The six CSV datasets were loaded into Databricks and organized under the project catalog:

```text
pysparkdbt
└── source
```

Schemas were then created for the medallion architecture:

```text
pysparkdbt
├── source
├── bronze
├── silver
└── gold
```

The Bronze ingestion notebook is responsible for bringing the source data into the Bronze layer.

The objective of the Bronze layer is to maintain a representation of the ingested source data before applying business transformations.

---

# 🥈 Silver Layer

The Silver layer is where the main data processing takes place.

The project uses **PySpark** for reusable transformations and also demonstrates a **dbt incremental model** for the Trips dataset.

## PySpark Transformations

Instead of creating six independent transformation implementations, reusable functionality was placed inside a Python class.

```python
class transformations:

    def dedup(self, df, dedup_cols, cdc):
        ...

    def process_timestamp(self, df):
        ...

    def upsert(self, df, key_cols, table, cdc):
        ...
```

This provides a more modular approach to data processing.

---

# 🧩 Modularity and Object-Oriented Python

The `custom_utils.py` module contains a reusable `transformations` class.

The class encapsulates common data engineering operations:

### `dedup()`

Performs CDC-based deduplication using a Spark window function.

Conceptually:

```text
Partition by business key
        ↓
Order by CDC timestamp DESC
        ↓
Assign row number
        ↓
Keep row_number = 1
```

The implementation uses:

```python
row_number().over(
    Window
    .partitionBy(*dedup_cols)
    .orderBy(col(cdc).desc())
)
```

This allows the pipeline to retain the latest version of a record.

---

## `process_timestamp()`

Adds a processing timestamp to the dataset:

```python
df = df.withColumn(
    "process_timestamp",
    current_timestamp()
)
```

This provides metadata indicating when the pipeline processed a record.

---

# 🔄 Delta MERGE / Upsert

The reusable `upsert()` function implements Delta Lake MERGE logic.

The merge condition is dynamically generated from the supplied key columns:

```python
merge_condition = " AND ".join(
    [f"src.{i} = trg.{i}" for i in key_cols]
)
```

The pipeline then performs:

```text
                 Incoming Data
                      │
                      ▼
                 Delta MERGE
                 /         \
          Match             No Match
            │                   │
            ▼                   ▼
         UPDATE              INSERT
```

The implementation uses the CDC timestamp to determine whether a matched record should be updated:

```python
.whenMatchedUpdateAll(
    condition=f"src.{cdc} >= trg.{cdc}"
)
.whenNotMatchedInsertAll()
```

This demonstrates an important data engineering pattern:

> **Use a business key to identify records and a CDC/update timestamp to determine the most recent version.**

---

# ⚡ Incremental Processing

The project also implements incremental processing using dbt.

The Trips transformation is configured as:

```jinja
{{ 
    config(
        materialized='incremental',
        unique_key='trip_id'
    )
}}
```

Instead of processing the entire Trips dataset every time, the model checks whether it is running incrementally:

```jinja
{% if is_incremental() %}
```

It then filters records using the latest timestamp already present in the target:

```sql
WHERE last_updated_timestamp >
(
    SELECT COALESCE(
        MAX(last_updated_timestamp),
        '1900-01-01'
    )
    FROM {{ this }}
)
```

Conceptually:

```text
                 Bronze Trips
                      │
                      ▼
              Check target table
                      │
                      ▼
        Find MAX(last_updated_timestamp)
                      │
                      ▼
      Keep only newer source records
                      │
                      ▼
              Incremental Model
```

This reduces unnecessary processing when only a subset of source data has changed.

---

# 🧮 Dynamic SQL with Jinja

The dbt Trips model also uses Jinja to dynamically generate the selected columns.

The columns are defined as a Python/Jinja list:

```jinja
{% set cols = [
    'trip_id',
    'vehicle_id',
    'customer_id',
    'driver_id',
    'trip_start_time',
    'trip_end_time',
    'distance_km',
    'fare_amount',
    'last_updated_timestamp'
] %}
```

The columns are then generated using a Jinja loop:

```jinja
{% for col in cols %}
    {{ col }}
{% endfor %}
```

This demonstrates how **Jinja templating can reduce repetitive SQL and make dbt models more dynamic and maintainable.**

---

# 🧱 dbt Layer

After the Silver transformations, dbt was connected to the Databricks environment.

The dbt project contains:

```text
models/
snapshots/
macros/
tests/
seeds/
analyses/
```

The dbt configuration defines separate behavior for the Silver and Gold models.

Gold models are configured as tables:

```yaml
gold:
  +materialized: table
```

Silver models are also configured as tables, with the Silver schema explicitly assigned:

```yaml
silver:
  +materialized: table
  +schema: silver
```

---

# 🧩 Custom dbt Macro

A custom `generate_schema_name` macro was created to control how dbt resolves schema names.

```jinja
{% macro generate_schema_name(custom_schema_name, node) %}

    {% set default_schema = target.schema %}

    {% if custom_schema_name is none %}

        {{ default_schema }}

    {% else %}

        {{ custom_schema_name | trim }}

    {% endif %}

{% endmacro %}
```

This demonstrates the use of **dbt macros and Jinja-based customization**.

---

# 🥇 Gold Layer

The Gold layer represents the analytics-ready dimensional model.

The final Gold schema contains:

### Fact

* `FactTrips`

### Dimensions

* `DimCustomers`
* `DimDrivers`
* `DimLocations`
* `DimPayments`
* `DimVehicles`

Conceptually:

```text
                         DimCustomers
                              │
                              │
                              ▼
DimDrivers ───────────► FactTrips ◄────────── DimVehicles
                              │
                              │
                              ▼
                        DimLocations

                              │
                              ▼
                        DimPayments
```

The Gold layer is designed for analytical consumption rather than raw operational processing.

---

# 📚 Dimensional Modeling

The project applies a **fact-and-dimension modeling approach**.

## FactTrips

The trip entity represents the central business event.

It contains measures and identifiers associated with a trip, such as:

* Distance
* Fare
* Trip timestamps
* Customer
* Driver
* Vehicle
* Trip status

## Dimension Tables

The dimensions provide descriptive attributes surrounding the trip event.

```text
DimCustomers
    ↓
Customer attributes

DimDrivers
    ↓
Driver attributes

DimVehicles
    ↓
Vehicle attributes

DimLocations
    ↓
Geographical attributes

DimPayments
    ↓
Payment information
```

This creates an analytical model that can support queries such as:

* Trip analysis
* Customer analysis
* Driver performance
* Vehicle utilization
* Payment analysis
* Location-based analysis

---

# 🕒 SCD Type 2 with dbt Snapshots

One of the key features of the Gold layer is **Slowly Changing Dimension Type 2 (SCD Type 2)** implementation through dbt snapshots.

Snapshots were configured for:

```text
DimCustomers
DimLocations
DimDrivers
DimPayments
DimVehicles
```

Each snapshot uses:

```yaml
unique_key: customer_id
strategy: timestamp
updated_at: last_updated_timestamp
```

The corresponding unique key changes according to the entity.

For example:

```yaml
unique_key: customer_id
```

for customers and:

```yaml
unique_key: driver_id
```

for drivers.

---

## SCD Type 2 Concept

Instead of simply overwriting an existing dimension record:

```text
Old Record
    ↓
UPDATE
    ↓
New Record
```

SCD Type 2 preserves the historical version:

```text
Customer 101

Version 1
──────────────
City = Mumbai
Valid From = ...
Valid To   = ...

        ↓ Customer changes

Version 2
──────────────
City = Pune
Valid From = ...
Valid To   = ...
```

This allows historical analysis based on the state of an entity at a particular point in time.

The snapshots use:

```yaml
strategy: timestamp
updated_at: last_updated_timestamp
```

to determine when a source record has changed.

The project also configures:

```yaml
dbt_valid_to_current: "to_date('9999-12-31')"
```

for current records.

---

# 📸 FactTrips Snapshot

The Trips model is also configured as a dbt snapshot:

```yaml
name: FactTrips
relation: ref('trips')
unique_key: trip_id
strategy: timestamp
updated_at: last_updated_timestamp
```

This allows historical changes to Trips to be tracked using the same timestamp-based snapshot strategy.

---

# 🔁 dbt Execution

After the models and snapshots were configured, the project was executed using dbt commands including:

```bash
dbt build
dbt run
dbt snapshot
```

The resulting objects were materialized in Databricks.

The Databricks catalog was subsequently updated with the Gold schema containing the generated fact and dimension tables.

---

# 🗂️ Data Catalog Structure

The resulting Databricks catalog is organized around the project:

```text
pysparkdbt
│
├── source
│   ├── customers
│   ├── drivers
│   ├── trips
│   ├── locations
│   ├── vehicles
│   └── payments
│
├── bronze
│
├── silver
│
└── gold
    ├── FactTrips
    ├── DimCustomers
    ├── DimDrivers
    ├── DimLocations
    ├── DimPayments
    └── DimVehicles
```

The exact physical objects are managed by the Databricks/dbt configuration and execution.

---

# 🧠 Key Data Engineering Concepts Demonstrated

This project combines several important data engineering concepts.

### 1. Medallion Architecture

```text
Bronze → Silver → Gold
```

Separates ingestion, transformation, and analytical consumption.

### 2. PySpark

Used for distributed data transformations and processing.

### 3. Python Classes

A reusable `transformations` class encapsulates common transformation logic.

### 4. Modularity

Common operations are implemented once and reused rather than duplicated across notebooks.

### 5. Dynamic Processing

Functions accept parameters such as:

```text
dedup_cols
cdc
key_cols
table
```

allowing the same logic to operate on different datasets.

### 6. Window Functions

Used for CDC-based deduplication.

### 7. Delta Lake MERGE

Used to implement update/insert behavior through an upsert pattern.

### 8. Incremental Processing

dbt's `is_incremental()` functionality processes only newly updated data.

### 9. Jinja Templating

Used to dynamically generate SQL and customize dbt behavior.

### 10. dbt Macros

A custom schema-generation macro was implemented.

### 11. Dimensional Modeling

The Gold layer uses fact and dimension tables.

### 12. SCD Type 2

dbt snapshots preserve historical changes to dimension entities.

### 13. CDC-Based Processing

`last_updated_timestamp` is used throughout the pipeline to identify changed records.

---

# 🔍 Design Approach

A key design decision in this project was avoiding a purely table-by-table static transformation approach.

Instead of writing:

```text
customers transformation
drivers transformation
vehicles transformation
payments transformation
...
```

as completely independent implementations, common processing logic was abstracted into reusable functions.

```text
                    Transformation Class
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       dedup()       process_timestamp()   upsert()
          │                │                │
          └────────────────┴────────────────┘
                           │
                           ▼
                     Multiple Tables
```

This improves maintainability and makes the pipeline easier to extend.

---

# 🚀 What This Project Demonstrates

The project demonstrates an end-to-end workflow from raw source data to analytics-ready data:

```text
CSV
 ↓
Databricks Source
 ↓
Bronze
 ↓
PySpark / dbt Silver
 ↓
Deduplication
 ↓
CDC Processing
 ↓
Delta Upsert
 ↓
Incremental Processing
 ↓
dbt
 ↓
Jinja / Macros
 ↓
SCD Type 2 Snapshots
 ↓
Fact + Dimension Models
 ↓
Gold
 ↓
Analytics
```

Rather than being limited to SQL transformations, the project combines **data ingestion, distributed processing, reusable Python code, Delta Lake operations, incremental processing, dbt transformations, historical data management, and dimensional modeling**.

---

# 📌 Project Structure

A representative project structure is:

```text
mobility-services-data-engineering/
│
├── notebooks/
│   ├── Bronze_ingestion.ipynb
│   └── Silver_transformation.ipynb
│
├── pyspark/
│   └── custom_utils.py
│
├── dbt/
│   ├── dbt_project.yml
│   │
│   ├── models/
│   │   ├── silver/
│   │   │   └── trips.sql
│   │   │
│   │   └── ...
│   │
│   ├── snapshots/
│   │   ├── scds.yml
│   │   └── fact.yml
│   │
│   ├── macros/
│   │   └── generate_schema_name.sql
│   │
│   └── ...
│
└── README.md
```

---

# 📈 Potential Future Enhancements

The current implementation provides a batch-oriented pipeline with incremental processing and CDC-based updates.

Potential future extensions include:

* Implement Spark Structured Streaming for near-real-time ingestion.
* Add automated data-quality tests in dbt.
* Add dbt documentation and lineage.
* Add orchestration using a workflow/scheduling framework.
* Add pipeline monitoring and alerting.
* Add automated data validation between Bronze, Silver, and Gold.
* Add CI/CD for dbt and PySpark code.
* Add additional analytical marts for business-specific use cases.
* Add automated testing for reusable PySpark transformation functions.

> **Note:** Spark Structured Streaming is listed here as a potential extension rather than as an implemented component of the current pipeline.

---

# 🎯 Learning Outcomes

Through this project, the following concepts were applied in a practical data engineering workflow:

* Medallion architecture
* Databricks
* PySpark
* Delta Lake
* Python classes and objects
* Modular programming
* Dynamic transformation logic
* Window functions
* CDC-based deduplication
* Delta MERGE / upsert
* Incremental processing
* dbt models
* dbt incremental materializations
* Jinja templating
* dbt macros
* dbt snapshots
* SCD Type 2
* Fact and dimension modeling
* Star-schema concepts
* Databricks data catalog organization

---

# 👨‍💻 Project Summary

**Mobility Services Data Engineering Pipeline** is an end-to-end data engineering project that transforms six raw operational datasets into a structured analytical data model.

The pipeline uses **Databricks and PySpark for ingestion and transformation**, **Delta Lake for upsert-based processing**, and **dbt for incremental modeling, Jinja-based SQL generation, snapshots, and SCD Type 2 historical tracking**.

The final Gold layer provides a dimensional model consisting of a central `FactTrips` table and supporting customer, driver, location, payment, and vehicle dimensions.

The project demonstrates how modern data engineering practices can be combined to build a reusable and scalable pipeline from raw data ingestion through analytics-ready modeling.
