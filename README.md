# Supplier & Procurement KPI Dashboard

**AI-assisted educational portfolio project** for junior procurement, business operations and data analyst roles. No real supplier or commercial records are used.

## Business question
Which suppliers have the weakest delivery reliability and quality, and how does their spend compare? A purchasing team can use these metrics to prioritize supplier reviews rather than choosing solely on price.

## Data and provenance
All 500 purchase orders are **synthetically generated** with Python's seeded random generator. Names, quantities, prices and performance are fictitious. No external dataset, private company data or licence restrictions. Simulated supplier performance must not be interpreted as a real market benchmark.

## Run
Requires Python 3.11+ and SQLite (included with Python).

```bash
python -m src.procurement
python -m pip install -r requirements.txt
python -m pytest -q
```

The pipeline creates `data/synthetic_orders.csv` and `outputs/supplier_kpis.csv` locally. The latter imports into Power BI or Excel. Both generated CSVs are excluded from git; regenerate them using the command above.

## Architecture
Seeded synthetic CSV generator → SQLite orders table with integrity checks → grouped SQL metrics → flat KPI CSV for Power BI/Excel.

## Definitions
- **On-time delivery %** = orders delivered on or before promised date / all orders × 100; each order counts equally.
- **Defect %** = defective units / all units received × 100; weighted by quantity.
- **Spend (€)** = sum of order quantity × unit price; excludes tax, shipping, refunds and discounts.
- **Average delay (days)** = average actual delivery date minus promised date; early delivery yields a negative value.

## Interpretation and limitations
Low on-time delivery combined with high spend suggests a supplier-management priority. This is an exploratory teaching example, not a predictive model. The dataset lacks partial deliveries, returns, currency conversion, payment terms, seasonal demand and real-world procurement constraints. Generated suppliers intentionally differ slightly in delay patterns. The export is Power BI-ready, **not** a claim that a Power BI dashboard has already been published.

## Interview explanation
See [docs/interview_guide.md](docs/interview_guide.md). Tests include a hand-calculated two-order example to validate SQL denominators and rounding.
