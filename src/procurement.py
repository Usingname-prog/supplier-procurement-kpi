"""Synthetic supplier procurement KPI pipeline; Python standard library only."""
import csv
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def generate_orders(path, count=500, seed=42):
    rng = random.Random(seed)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['order_id', 'supplier', 'ordered_date', 'promised_date', 'delivered_date', 'quantity', 'unit_price_eur', 'defective_units'])
        for i in range(count):
            supplier = ['Aster Components', 'Northline Supply', 'Orion Packaging', 'Vale Industrial'][i % 4]
            ordered = date(2026, 1, 1) + timedelta(days=rng.randrange(240))
            promised = ordered + timedelta(days=rng.randrange(4, 15))
            actual = promised + timedelta(days=rng.randrange(-3, 8) + (2 if supplier == 'Vale Industrial' else 0))
            quantity = rng.randrange(10, 200)
            defective = min(quantity, int(quantity * rng.uniform(0, .09)))
            writer.writerow([f'PO-{i+1:05}', supplier, ordered, promised, actual, quantity, f'{rng.uniform(5, 90):.2f}', defective])
    return path


def load_orders(connection, path):
    connection.executescript('''CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY, supplier TEXT NOT NULL,
        ordered_date TEXT NOT NULL, promised_date TEXT NOT NULL,
        delivered_date TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity > 0),
        unit_price_eur REAL NOT NULL CHECK(unit_price_eur >= 0),
        defective_units INTEGER NOT NULL CHECK(defective_units >= 0 AND defective_units <= quantity));''')
    with Path(path).open(newline='', encoding='utf-8') as file:
        rows = list(csv.DictReader(file))
    connection.executemany('''INSERT INTO orders VALUES (:order_id,:supplier,:ordered_date,:promised_date,:delivered_date,:quantity,:unit_price_eur,:defective_units)''', rows)
    connection.commit()
    return len(rows)


def supplier_kpis(connection):
    query = (ROOT / 'sql' / 'supplier_kpis.sql').read_text(encoding='utf-8')
    connection.row_factory = sqlite3.Row
    return [dict(row) for row in connection.execute(query)]


def export_kpis(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['supplier','orders','spend_eur','on_time_pct','defect_pct','avg_delay_days'])
        writer.writeheader()
        writer.writerows(rows)
    return path


def main():
    source = generate_orders(ROOT / 'data' / 'synthetic_orders.csv')
    connection = sqlite3.connect(':memory:')
    load_orders(connection, source)
    results = supplier_kpis(connection)
    output = export_kpis(results, ROOT / 'outputs' / 'supplier_kpis.csv')
    print(f'Processed 500 synthetic orders across {len(results)} suppliers; exported {output}')
    for row in results:
        print(f"{row['supplier']}: {row['on_time_pct']:.1f}% on time; €{row['spend_eur']:.2f} spend")


if __name__ == '__main__':
    main()
