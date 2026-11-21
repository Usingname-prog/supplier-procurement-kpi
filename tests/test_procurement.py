import csv
import sqlite3
from src.procurement import generate_orders, load_orders, supplier_kpis, export_kpis


def test_deterministic_generation(tmp_path):
    a = generate_orders(tmp_path / 'a.csv', 20, seed=3)
    b = generate_orders(tmp_path / 'b.csv', 20, seed=3)
    assert a.read_bytes() == b.read_bytes()


def test_order_constraints(tmp_path):
    path = generate_orders(tmp_path / 'orders.csv', 70)
    with path.open(newline='') as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 70
    assert all(0 <= int(r['defective_units']) <= int(r['quantity']) for r in rows)


def test_sql_metrics_with_known_values(tmp_path):
    path = tmp_path / 'known.csv'
    path.write_text('order_id,supplier,ordered_date,promised_date,delivered_date,quantity,unit_price_eur,defective_units\n'
                    '1,Test,2026-01-01,2026-01-10,2026-01-09,10,5,1\n'
                    '2,Test,2026-01-01,2026-01-10,2026-01-12,30,2,3\n')
    conn = sqlite3.connect(':memory:')
    assert load_orders(conn, path) == 2
    row = supplier_kpis(conn)[0]
    assert row['orders'] == 2
    assert row['spend_eur'] == 110
    assert row['on_time_pct'] == 50
    assert row['defect_pct'] == 10
    assert row['avg_delay_days'] == .5


def test_export_roundtrip(tmp_path):
    conn = sqlite3.connect(':memory:')
    load_orders(conn, generate_orders(tmp_path / 'in.csv', 12))
    output = export_kpis(supplier_kpis(conn), tmp_path / 'out.csv')
    with output.open(newline='') as file:
        assert len(list(csv.DictReader(file))) == 4
