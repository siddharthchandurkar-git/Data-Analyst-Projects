# 📊 Loan Data Analysis & Risk Insights Dashboard

An end-to-end data analytics project focused on analyzing loan behavior, default patterns, and financial risk using a large-scale dataset.

---

## 🚀 Project Overview

This project analyzes **250,000+ loan records** to uncover patterns in:

- Loan defaults  
- Customer demographics  
- Financial risk indicators  
- Credit behavior  

The goal was to move beyond reporting and answer:

👉 *What factors contribute to loan default risk, and how can they be identified early?*

---

## 🛠️ Tech Stack

- **SQL (MS SQL Server)** – Data storage, cleaning, transformation  
- **Power BI** – Interactive dashboards and business insights  
- **DAX** – Advanced calculations and metrics  
- **Power BI Service + Gateway** – Dataflow pipeline integration  

---

## 📂 Dataset

- Source: Kaggle (Loan Dataset)  
- Size: 250,000+ records  
- Key fields:
  - Loan Amount, Income, Credit Score  
  - Employment Type, Education, Marital Status  
  - Loan Purpose, Interest Rate, DTI Ratio  
  - Default Status  

---

## ⚙️ Data Engineering & Preparation

### 1. Data Loading (SQL)
- Imported raw dataset into SQL Server  
- Structured data into analyzable format  

### 2. Data Cleaning & Transformation
- Identified missing values  
- Replaced nulls using **group-based mean imputation**  
  *(e.g., different averages for different credit score segments)*  

👉 This ensured more realistic and context-aware data cleaning  

### 3. Data Pipeline
- Connected SQL Server to Power BI using:
  - **On-Premises Data Gateway**
  - **Dataflow Pipeline**
- Loaded processed data into Power BI  

---

## 🔄 Data Transformation (Power BI)

- Performed transformations using Power Query  
- Created derived columns:
  - Age Groups  
  - Credit Score Categories  
  - Income Brackets  

---

## 📊 Dashboard Overview

The dashboard is divided into **3 analytical layers**:

---

### 1️⃣ Loan Default & Overview


::contentReference[oaicite:0]{index=0}


- Loan distribution by purpose  
- Default rate by employment type  
- Income trends across employment categories  
- Default trends over time  
- Loan amount analysis by age group  

---

### 2️⃣ Applicant Demographics & Financial Profile


::contentReference[oaicite:1]{index=1}


- Loan patterns across credit score categories  
- Demographic segmentation (age, marital status, education)  
- Loan distribution by income and employment  
- Credit behavior insights  

---

### 3️⃣ Financial Risk Metrics


::contentReference[oaicite:2]{index=2}


- Year-over-Year (YoY) loan amount change  
- YoY default trends  
- YTD loan metrics  
- Risk flow visualization across income and employment  

---

## 📐 Key DAX Measures

Implemented advanced DAX calculations for analytical insights.

📄 Full list of measures: :contentReference[oaicite:3]{index=3}  

Key examples:

- Default Rate by Employment Type  
- YoY Loan Amount Change  
- YoY Default Change  
- YTD Loan Amount  
- Median Loan by Credit Category  

---

## 📈 Key Insights

- **Unemployed individuals show highest default rates**  
- Default risk decreases significantly for **full-time employees**  
- Lower credit score groups show **higher financial risk concentration**  
- Loan distribution varies strongly by **purpose and income levels**  
- YoY trends reveal **cyclical changes in default behavior**  

---

## 🎯 Business Impact

- Enables early identification of **high-risk borrowers**  
- Supports **credit risk assessment and decision-making**  
- Helps financial institutions optimize **loan approval strategies**  
- Provides a foundation for **risk modeling and policy design**  

---

## 📁 Project Structure
├── SQL/
│ └── data_cleaning.sql
├── dashboards/
│ ├── Loan_Overview.png
│ ├── Demographics.png
│ └── Financial_Metrics.png
├── dax/
│ └── measures.docx
├── data/
│ └── dataset.csv
└── README.md


---

## ⚡ How to Run

1. Load dataset into SQL Server  
2. Perform cleaning and transformation  
3. Connect Power BI via Dataflow  
4. Open Power BI dashboard file  
5. Explore insights  

---

## 💡 Key Learnings

- Importance of **context-aware data cleaning (group-based imputation)**  
- Translating raw financial data into **risk insights**  
- Building layered dashboards for **exploration → explanation → decision**  
- Applying DAX for advanced analytical logic  

---

## 🤝 Connect

If you're working in analytics, finance, or strategy — happy to connect and discuss!

