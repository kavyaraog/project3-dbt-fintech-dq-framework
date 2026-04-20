# Project 3 — dbt Data Quality Framework for Fintech

## What This Does

A production-style dbt data quality framework that standardises raw fintech
transaction data, runs automated schema and business rule tests on Snowflake,
and uses the Claude API to generate plain-English AI-powered reports for
engineers and business stakeholders.

## Why This Matters

Data quality failures in fintech cause reconciliation errors, regulatory
breaches, and customer trust issues. This framework catches problems at the
transformation layer — before bad data reaches dashboards or downstream systems.

## Results from First Run

The framework identified 3 real data quality issues automatically:

- **Duplicate transaction_id (TXN008)** — would cause potential double-charge exposure in payments
- **Missing customer_id on TXN005** — creates a BSA/AML reporting gap
- **Invalid amounts on 2 transactions** — negative and zero values, invalid in a payments context

6 of 9 automated tests passed. 3 meaningful failures detected, classified by business
impact, and summarised by Claude API into a compliance-ready narrative report.

## Pipeline Architecture

Raw CSV Data → Snowflake → dbt Staging Model → dbt Tests → Claude API Report Generator → Markdown Audit Report

## Data Quality Tests Implemented

- **Uniqueness** — transaction_id must be unique (catches duplicate charges)
- **Not Null** — critical fields cannot be missing (catches BSA/AML gaps)
- **Accepted Values** — status and payment_method must match expected values
- **Range Validation** — amount must be greater than zero (catches invalid payments)

## Tech Stack

- dbt Core
- Snowflake (cloud data warehouse)
- DuckDB (local development option)
- Claude API (Anthropic) — AI-powered narrative reporting
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
3. Configure your Snowflake connection in `~/.dbt/profiles.yml`
4. Install dbt dependencies: `dbt deps`
5. Load seed data: `dbt seed`
6. Run models: `dbt run`
7. Run tests: `dbt test`
8. Generate AI report: `python dq_ai_reporter.py`

## Output

Timestamped markdown reports with executive summary, business impact analysis,
and risk level (LOW/MEDIUM/HIGH) for each data quality issue found. Reports
are structured for review by both engineering teams and compliance stakeholders.

## Domain Context

Built with fintech transaction data including payment method validation,
transaction status checks, and amount range enforcement aligned with
financial data governance standards.

## Author

Kavya Gangadhara — Data Quality Engineer | Fintech & Banking Domain | AI-Augmented DQ Frameworks
