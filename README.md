# 🚕 Taxi Data Engineering Pipeline (2026 Standards)

An end-to-end high-performance data engineering pipeline built to process, clean, and analyze taxi sales data efficiently using **Polars (Lazy Evaluation API)** and **PostgreSQL**.

---

## 🏗️ Architecture & Features

- **High-Performance Ingestion:** Utilized **Polars Lazy API (`scan_csv`)** leveraging *Predicate Pushdown* and *Projection Pushdown* to minimize I/O operations and memory usage (RAM footprint minimization).
- **Streaming Pipeline:** Processed and validated raw data efficiently before transferring into the data warehouse layer.
- **Relational Storage:** Database loading into **PostgreSQL** using optimized batching techniques with `SQLAlchemy` and `psycopg2`.
- **Advanced Analytical Layer:** Developed complex analytical SQL queries using **Window Functions**, **Framing Specifications**, and `LAG()`/`LEAD()` for customer behavior and pattern tracking.
- **Version Control:** Managed and documented with standard Git practices.

---

## 🛠️ Tech Stack & Dependencies

- **Language:** Python 3.11+
- **Data Processing:** Polars, PyArrow
- **Database Layer:** PostgreSQL, SQLAlchemy, psycopg2-binary
- **Analytics:** Advanced SQL (PostgreSQL Window Functions)
- **Tooling:** VS Code, Git/GitHub

---

## 📁 Repository Structure

```text
taxi-data-engineering/
├── data/
│   └── raw/                   # Raw input datasets (CSV)
├── analytics_queries.sql      # Advanced Analytical SQL queries
├── pipeline_processor.py      # Core ET/ELT pipeline built with Polars Lazy API
├── requirements.txt           # Project environment dependencies
└── README.md                  # Project documentation