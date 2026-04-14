# Project 3 — dbt Data Quality Framework for Fintech

## What This Does
A production-style dbt data quality framework that standardises raw fintech 
transaction data, runs automated schema and business rule tests, and uses the 
Claude API to generate plain-English AI-powered reports for engineers and 
business stakeholders.

## Why This Matters
Data quality failures in fintech cause reconciliation errors, regulatory 
breaches, and customer trust issues. This framework catches problems at the 
transformation layer — before bad data reaches dashboards or downstream systems.

## Pipeline Architecture
Raw CSV Data → dbt Staging Model → dbt Tests → AI Report Generator → Markdown Report

## Data Quality Tests Implemented
- **Uniqueness** — transaction_id must be unique
- **Not Null** — critical fields cannot be missing
- **Accepted Values** — status and payment_method must match expected values
- **Range Validation** — amount must be greater than zero (dbt_utils)

## Tech Stack
- dbt Core
- DuckDB (local development)
- Claude API (Anthropic) — AI-powered report narrative
- Python 3
- dbt_utils package

## Project Structure
project3_fintech_dq/
├── models/
│   └── staging/
│       ├── stg_fintech__transactions.sql
│       └── _staging__models.yml
├── seeds/
│   └── transactions_raw.csv
├── dq_ai_reporter.py
├── dbt_project.yml
└── packages.yml

## How To Run

1. Clone the repository
2. Create a `.env` file with your `ANTHROPIC_API_KEY`
3. Install dbt dependencies:

dbt deps
4. Load seed data:

dbt seed
5. Run models:

dbt run
6. Run tests:

dbt test
7. Generate AI report:

python dq_ai_reporter.py
## Output
Timestamped markdown reports with executive summary, business impact analysis, 
and risk level (LOW/MEDIUM/HIGH) for each data quality issue found.

## Domain Context
Built with fintech transaction data including payment method validation, 
transaction status checks, and amount range enforcement aligned with 
financial data governance standards.

## Author
Kavya — AI-Augmented Data Quality Engineer
15 years experience in Fintech, Banking, Cybersecurity & Insurance