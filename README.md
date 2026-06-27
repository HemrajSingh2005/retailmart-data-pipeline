# retailmart-data-pipeline
Data Engineering Assignment - RetailMart ETL Pipeline | Mandelbulb Technologies
# 🛒 RetailMart Data Pipeline

An end-to-end ETL (Extract → Transform → Load) data pipeline built 
in Python, simulating a real-world retail data engineering workflow.

---

## 📌 Problem Statement

RetailMart Pvt. Ltd. collects raw, messy daily sales data from stores 
across India. This pipeline automates the process of cleaning, 
transforming, and loading that data so the business team can use it 
for reporting and decision-making.

---

## 🏗️ Pipeline Architecture

sales_data.csv  ─┐

products.csv    ──► Ingest → Clean → Transform → SQLite DB → Reports

stores.csv      ─┘

---

## ⚙️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core pipeline language |
| Pandas | Data ingestion, cleaning, transformation |
| NumPy | Statistical calculations |
| SQLite3 | Data loading and SQL querying |
| Power BI | Interactive sales dashboard for business reporting |
| Git + GitHub | Version control |

---

## 📋 Pipeline Stages

### Stage 1 — Data Ingestion
- Load 3 CSV sources into Pandas DataFrames
- Print shape, preview, and null summary for each

### Stage 2 — Data Cleaning
- Detect and remove duplicate transactions
- Fill missing quantity with 0 (safe default)
- Drop rows with missing amount (financial integrity)
- Convert sale_date to datetime, amount to float

### Stage 3 — Data Transformation
- Three-way merge using left joins on store_id and product_id
- Compute total_revenue = quantity × price
- NumPy stats: mean, max, min revenue
- City-wise revenue aggregation (sorted descending)

### Stage 4 — Data Loading
- Load final DataFrame into SQLite (retail_sales table)
- SQL query: Top 3 best-selling products by quantity

### Stage 5 — Reporting
- SQL query: Revenue per store per day
- Python summary: total transactions, revenue, top city, top product

### Stage 6 — Error Handling
- Full pipeline wrapped in run_pipeline()
- Handles: FileNotFoundError, EmptyDataError, sqlite3.Error

---
## 📊 Sales Dashboard

Built an interactive Power BI dashboard covering:
- KPI Cards — Total Revenue, Total Transactions, Top City, Top Product
- Total Revenue by City (bar chart)
- Top Products by Quantity Sold (bar chart)
- Daily Revenue per Store (table)

[View Dashboard (PDF)](dashboard/RetailMart_Dashboard.pdf)

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/Hemraj-coder/retailmart-data-pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline
python3 retailmart_pipeline.py
```

---

## 📊 Sample Output

[Pipeline Output1](output_screenshots/output_screenshot1.png)

[Pipeline Output2](output_screenshots/output_screenshot2.png)

[Pipeline Output3](output_screenshots/output_screenshot3.png)

---

## 📁 Project Structure

retailmart-data-pipeline/

├── retailmart_pipeline.py   # Main ETL pipeline

├── requirements.txt         # Dependencies

├── output_screenshots/      # Terminal output proof

└── dashboard/               # business reporting

---

## 👤 Author

**Hemraj Singh**  
B.Tech CSE (AI & Data Science) | Poornima University  
[LinkedIn](https://www.linkedin.com/in/hemrajsingh2005) • 
[GitHub](https://github.com/HemrajSingh2005)
