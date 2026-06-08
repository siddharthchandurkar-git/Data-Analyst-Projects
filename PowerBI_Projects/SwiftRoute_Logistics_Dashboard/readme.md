# 🚚 SwiftRoute Logistics Dashboard

## 📌 Project Overview

This project focuses on analyzing logistics operations for a fictional logistics company, **SwiftRoute Logistics**, using Power BI.

The objective was to transform raw operational data into actionable insights by monitoring delivery performance, hub efficiency, driver productivity, and fleet utilization. The dashboard was developed based on detailed business requirements and follows a dimensional modeling approach using a Star Schema.

---

## 🎯 Business Problem

Logistics companies manage large volumes of orders, drivers, hubs, and vehicles every day. Management required a centralized dashboard to answer key operational questions:

- How many orders were processed this month?
- Are deliveries being completed on time?
- Which hubs are performing efficiently?
- Which drivers contribute most to delivery delays?
- Which vehicles experience the highest breakdown rates?
- How does customer satisfaction change over time?

The goal was to provide operational visibility and support data-driven decision-making.

---

## 🏗️ Project Approach

### 1. Requirement Gathering & Domain Understanding

Before building the dashboard, the dataset and business requirements were thoroughly studied to understand:

- Order lifecycle and delivery process
- Hub operations and processing workflows
- Driver performance metrics
- Fleet management concepts
- Customer satisfaction measurement

Domain knowledge was documented to understand the business meaning behind each field and KPI.

---

### 2. Data Preparation

The data was imported into Power BI and reviewed for quality.

Tasks performed:

- Validated column data types
- Standardized date fields
- Reviewed data quality
- Verified relationships between datasets

---

### 3. Data Modeling

A Star Schema model was created.

#### Fact Table
- Orders

#### Dimension Tables
- Drivers
- Hubs
- Vehicles
- Date Table

A dedicated Date Table was created to support:

- Time intelligence calculations
- Month-over-Month analysis
- Trend reporting

Relationships were established between fact and dimension tables to optimize reporting performance.

---

### 4. DAX Development

Custom DAX measures were developed to support KPI calculations and dynamic reporting.

Examples include:

- Total Orders
- On-Time Delivery Rate
- Customer Satisfaction (CSAT %)
- Average Delivery Time
- Previous Month KPIs
- Month-over-Month Growth %
- Driver Performance KPIs
- Dynamic Titles
- Vehicle Utilization Metrics

All KPI calculations were validated using Excel Pivot Tables to ensure accuracy.

---

## 📊 Dashboard Pages

---

## Dashboard 1: Executive Overview

![Executive Dashboard](Swiftroute%20Logistics%20Dashboard.png)

### KPIs

- Total Orders
- On-Time Delivery Rate
- Customer Satisfaction Score (CSAT)
- Average Delivery Time
- Previous Month Comparison
- Month-over-Month Performance

### Operational Insights

#### Hubs
- Total Hubs
- Orders Processed vs Hub Capacity
- Hub Performance Ranking

#### Drivers
- Number of Drivers
- Experience vs Rating Analysis
- Drivers with Highest Delays

#### Vehicles
- Fleet Size
- Active vs Maintenance Vehicles
- Orders by Vehicle Model

---

## Dashboard 2: Hubs Overview

![Hubs Overview](Hubs%20overview.png)

### Insights

- Orders Processed vs Hub Capacity
- Hub Performance Ranking
- Daily Processing Time Analysis
- Hub Utilization Monitoring

### Business Value

- Identify overloaded hubs
- Detect underutilized hubs
- Improve workload distribution
- Support capacity planning

---

## Dashboard 3: Drivers Overview

![Drivers Overview](Drivers%20Overview.png)

### Insights

- Driver Performance Analysis
- Experience vs Rating Correlation
- Drivers with Highest Delays
- Driver Profile Summary
- Monthly Delivery Trends

### Business Value

- Monitor driver productivity
- Identify training opportunities
- Analyze workload distribution
- Improve delivery performance

---

## Dashboard 4: Vehicles Overview

![Vehicles Overview](Vehicles%20Overview.png)

### Insights

- Fleet Availability
- Vehicle Reliability
- Breakdown Analysis
- Orders by Vehicle Type
- Orders by Vehicle Model
- Vehicle Age vs Breakdown Correlation

### Business Value

- Reduce maintenance risks
- Improve fleet utilization
- Identify unreliable vehicles
- Support replacement planning

---

## 📈 KPIs Implemented

### Operational KPIs

- Total Orders
- Delivered Orders
- Delayed Orders
- On-Time Delivery Rate
- Average Delivery Time
- Customer Satisfaction Score (CSAT)

### Trend KPIs

- Previous Month Orders
- Previous Month CSAT
- Previous Month Delivery Rate
- Previous Month Average Delivery Time

### Growth KPIs

- Month-over-Month Orders Growth %
- Month-over-Month CSAT Change %
- Month-over-Month Delivery Rate Change %
- Month-over-Month Delivery Time Change %

---

## 🧮 DAX Functions Used

- CALCULATE()
- DATEADD()
- DIVIDE()
- COUNT()
- AVERAGE()
- SELECTEDVALUE()
- DATEDIFF()
- FORMAT()
- WEEKDAY()
- REPT()

---

## 🛠️ Tools & Technologies

- Power BI Desktop
- Power Query
- DAX
- Data Modeling
- Star Schema Design
- Excel (Validation)

---

## 📚 Key Learnings

Through this project, I gained hands-on experience in:

- Translating business requirements into dashboard solutions
- Understanding logistics and supply chain operations
- Building dimensional data models
- Creating time-intelligence calculations using DAX
- KPI validation and reporting best practices
- Designing executive-level operational dashboards
- Delivering actionable insights through data visualization

---

## 📂 Project Structure

```text
SwiftRoute Logistics Dashboard
│
├── Dataset
├── Power BI Report (.pbix)
├── Dashboard Screenshots
├── README.md
└── Documentation
```

---

## ⭐ Conclusion

This project demonstrates how Power BI can be used to monitor logistics operations across hubs, drivers, vehicles, and orders. By combining business requirements, domain knowledge, data modeling, DAX calculations, and interactive visualizations, the dashboard provides decision-makers with a comprehensive view of operational performance and areas for improvement.
