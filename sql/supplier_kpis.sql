-- Order-weighted on-time delivery; unit-weighted defect rate.
-- avg_delay_days includes early deliveries as negative days.
SELECT supplier,
       COUNT(*) AS orders,
       ROUND(SUM(quantity * unit_price_eur), 2) AS spend_eur,
       ROUND(100.0 * SUM(CASE WHEN delivered_date <= promised_date THEN 1 ELSE 0 END) / COUNT(*), 2) AS on_time_pct,
       ROUND(100.0 * SUM(defective_units) / SUM(quantity), 2) AS defect_pct,
       ROUND(AVG(julianday(delivered_date) - julianday(promised_date)), 2) AS avg_delay_days
FROM orders
GROUP BY supplier
ORDER BY on_time_pct DESC, supplier;
