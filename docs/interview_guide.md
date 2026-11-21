# Explain it in an interview

**30-second pitch:** I reviewed an AI-assisted educational procurement analytics pipeline that generates transparent synthetic purchase orders, loads them into SQLite and calculates delivery, defect and spend KPIs. I can explain and reproduce each calculation and use the CSV output in Excel or Power BI.

**Why SQL?** Grouping by supplier makes aggregation reproducible. `CASE WHEN` counts on-time orders; `SUM(defective_units) / SUM(quantity)` correctly weights quality by units rather than averaging percentages.

**Why a seed?** It produces identical synthetic inputs for debugging, testing and fair comparisons.

**What can go wrong?** Missing dates, partial deliveries, duplicates, mixed currencies, late-arriving corrections and survivorship bias can invalidate supplier rankings. In a real system I would validate incoming data and add a reporting cut-off.

**What should I learn next?** SQL GROUP BY, CASE WHEN, joins, weighted averages, CSV encoding, basic data-quality checks, and building a Power BI bar chart of on-time % by supplier with spend as a secondary metric.

**Integrity:** This project was AI-assisted. Do not claim independent authorship, professional procurement experience, or real-world business impact.
