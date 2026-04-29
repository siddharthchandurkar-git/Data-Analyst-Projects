# 📊 Loan Data Analysis & Risk Insights Dashboard

An end-to-end data analytics project focused on analyzing loan behavior, default patterns, and financial risk using a large-scale dataset.

---

## 🚀 Project Overview

This project analyzes **250,000+ loan records** to uncover patterns in:

- Loan defaults  
- Customer demographics  
- Financial risk indicators  
- Credit behavior  

The goal was to answer:

👉 *What factors contribute to loan default risk, and how can they be identified early?*

---

## 🛠️ Tech Stack

- SQL (MS SQL Server)  
- Power BI  
- DAX  
- Power BI Service + Gateway  

---

## 📂 Dataset

- Source: Kaggle  
- Size: 250,000+ records  

Key fields include:
- Income, Loan Amount, Credit Score  
- Employment Type, Education, Marital Status  
- Interest Rate, DTI Ratio  
- Default  

---

## ⚙️ Data Preparation

- Loaded data into SQL Server  
- Handled null values using **group-based mean imputation**  
- Built ETL pipeline using Dataflows  
- Connected SQL → Power BI via Gateway  

---

## 🔄 Data Transformation

- Created calculated fields:
  - Age Group  
  - Credit Score Bins  
  - Income Brackets  

---

## 📊 Dashboard

### 1. Loan Default & Overview

![Loan Overview](loan_default_and_overview.png)

- Loan distribution by purpose  
- Default rate by employment type  
- Income vs employment trends  
- Default trend over time  

---

### 2. Applicant Demographics & Financial Profile

![Demographics](Applicant_demographics_and_financial_profile.png)

- Loan distribution by credit score  
- Demographic segmentation  
- Loan behavior by income & marital status  

---

### 3. Financial Risk Metrics

![Financial Metrics](financial_metrics.png)

- Year-over-Year loan change  
- Default trend analysis  
- YTD loan amount  
- Risk flow visualization  

---

## 📐 DAX Measures

Advanced calculations implemented using DAX.

Key examples:
- Default Rate by Employment Type  
- YoY Loan Change  
- YoY Default Change  
- YTD Loan Amount  

---

## 📈 Key Insights

- Unemployed individuals show highest default rates  
- Full-time employees have lowest risk  
- Low credit score segments show higher defaults  
- Loan purpose and income strongly influence risk  

---

## 🎯 Business Impact

- Identifies high-risk borrowers early  
- Supports credit decision-making  
- Enables risk-based segmentation  
- Improves loan strategy  

---

## 💡 Key Learnings

- Context-aware data cleaning  
- End-to-end analytics pipeline  
- Business-focused dashboard design  
- Financial risk interpretation  

---

## 🤝 Connect

Open to opportunities in Data Analytics / Business Analytics / Data Engineering
