import argparse
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATABASE_DIR = ROOT / "database"


REGIONS = [
    (1, "Gauteng"),
    (2, "Western Cape"),
    (3, "KwaZulu-Natal"),
    (4, "Eastern Cape"),
]

SUPPLIERS = [
    (1, "Atlas Components", 8, "Low"),
    (2, "Harbor Packaging", 5, "Medium"),
    (3, "Northstar Textiles", 12, "High"),
    (4, "Prime Industrial", 10, "Medium"),
    (5, "FreshRoute Foods", 4, "Low"),
]

PRODUCTS = [
    (1, "EL-1001", "Smart Sensor Module", "Electronics", 1, 185.00, 180, 520),
    (2, "EL-1002", "Control Board", "Electronics", 1, 265.00, 120, 360),
    (3, "PK-2201", "Recycled Carton 10kg", "Packaging", 2, 18.50, 500, 1600),
    (4, "PK-2202", "Tamper Seal Roll", "Packaging", 2, 9.80, 650, 1900),
    (5, "AP-3101", "Workwear Jacket", "Apparel", 3, 145.00, 160, 450),
    (6, "AP-3102", "Safety Glove Pair", "Apparel", 3, 34.00, 420, 1300),
    (7, "IN-4401", "Hydraulic Valve", "Industrial", 4, 390.00, 90, 260),
    (8, "IN-4402", "Bearing Kit", "Industrial", 4, 118.00, 170, 520),
    (9, "FR-5501", "Cold Chain Meal Kit", "Perishables", 5, 62.00, 300, 900),
    (10, "FR-5502", "Fresh Produce Crate", "Perishables", 5, 41.00, 360, 1100),
]


def sql_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(round(value, 2))
    return "'" + str(value).replace("'", "''") + "'"


def insert_sql(table, columns, rows):
    values = ",\n".join(
        "(" + ", ".join(sql_value(row[column] if isinstance(row, dict) else row[i]) for i, column in enumerate(columns)) + ")"
        for row in rows
    )
    return f"INSERT INTO {table} ({', '.join(columns)}) VALUES\n{values};\n"


def generate(months, orders, seed):
    random.seed(seed)
    start = date.today().replace(day=1) - timedelta(days=months * 30)
    start = start.replace(day=1)

    purchase_orders = []
    order_lines = []
    shipments = []
    inventory = []

    product_by_id = {product[0]: product for product in PRODUCTS}
    supplier_by_id = {supplier[0]: supplier for supplier in SUPPLIERS}
    po_id = 1
    line_id = 1
    shipment_id = 1

    for _ in range(orders):
        supplier_id, _, contracted_days, risk = random.choice(SUPPLIERS)
        region_id, _ = random.choice(REGIONS)
        product_candidates = [p for p in PRODUCTS if p[4] == supplier_id]
        order_date = start + timedelta(days=random.randint(0, months * 30))
        delay_bias = {"Low": 0.12, "Medium": 0.22, "High": 0.36}[risk]
        delayed = random.random() < delay_bias
        delay_days = random.randint(1, 8) if delayed else -random.randint(0, 2)
        expected_date = order_date + timedelta(days=contracted_days)
        actual_date = expected_date + timedelta(days=delay_days)
        freight_cost = random.uniform(700, 8500)
        quality_issue_units = random.randint(0, 18) if random.random() < delay_bias else random.randint(0, 4)

        purchase_orders.append({
            "purchase_order_id": po_id,
            "supplier_id": supplier_id,
            "region_id": region_id,
            "order_date": order_date.isoformat(),
            "expected_delivery_date": expected_date.isoformat(),
            "actual_delivery_date": actual_date.isoformat(),
            "freight_cost": freight_cost,
            "quality_issue_units": quality_issue_units,
        })

        total_transport = freight_cost * random.uniform(0.45, 0.9)
        shipments.append({
            "shipment_id": shipment_id,
            "purchase_order_id": po_id,
            "carrier": random.choice(["Imperial Logistics", "DSV", "Value Express", "ColdLink"]),
            "service_level": random.choice(["Standard", "Priority", "Economy"]),
            "shipped_date": (order_date + timedelta(days=random.randint(1, 3))).isoformat(),
            "delivered_date": actual_date.isoformat(),
            "transport_cost": total_transport,
        })
        shipment_id += 1

        for product in random.sample(product_candidates, random.randint(1, min(2, len(product_candidates)))):
            product_id, _, _, category, _, unit_cost, reorder_point, target_stock = product
            ordered = random.randint(max(80, reorder_point // 2), target_stock)
            shortage_probability = 0.28 if delayed else 0.09
            if random.random() < shortage_probability:
                fill_pressure = 0.82 if delayed else 0.92
                fulfilled = min(ordered, int(ordered * random.uniform(fill_pressure, 0.99)))
            else:
                fulfilled = ordered
            backordered = ordered - fulfilled
            stockout = backordered > 0 or random.random() < 0.03
            reason = "Supplier delay" if delayed else ("Demand spike" if stockout else "None")
            order_lines.append({
                "order_line_id": line_id,
                "purchase_order_id": po_id,
                "product_id": product_id,
                "ordered_units": ordered,
                "fulfilled_units": fulfilled,
                "backordered_units": backordered,
                "stockout_flag": stockout,
                "delay_reason": reason,
            })
            line_id += 1
        po_id += 1

    movement_id = 1
    for product in PRODUCTS:
        product_id, _, _, _, _, unit_cost, reorder_point, target_stock = product
        for region_id, _ in REGIONS:
            opening = random.randint(reorder_point, target_stock)
            for week in range(months * 4):
                issued = random.randint(max(20, reorder_point // 5), max(40, target_stock // 3))
                received = random.randint(0, target_stock // 2) if random.random() < 0.45 else 0
                closing = max(0, opening + received - issued)
                holding_cost = ((opening + closing) / 2) * unit_cost * 0.018
                inventory.append({
                    "movement_id": movement_id,
                    "product_id": product_id,
                    "region_id": region_id,
                    "movement_date": (start + timedelta(days=week * 7)).isoformat(),
                    "opening_units": opening,
                    "received_units": received,
                    "issued_units": issued,
                    "closing_units": closing,
                    "holding_cost": holding_cost,
                })
                opening = max(closing, random.randint(0, reorder_point)) if closing < reorder_point else closing
                movement_id += 1

    return purchase_orders, order_lines, shipments, inventory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--orders", type=int, default=650)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)
    purchase_orders, order_lines, shipments, inventory = generate(args.months, args.orders, args.seed)

    datasets = {
        "purchase_orders": purchase_orders,
        "order_lines": order_lines,
        "shipments": shipments,
        "inventory_movements": inventory,
    }
    for name, rows in datasets.items():
        pd.DataFrame(rows).to_csv(DATA_DIR / f"{name}.csv", index=False)

    sql = ["TRUNCATE inventory_movements, shipments, order_lines, purchase_orders RESTART IDENTITY CASCADE;\n"]
    sql.append(insert_sql("purchase_orders", list(purchase_orders[0].keys()), purchase_orders))
    sql.append(insert_sql("order_lines", list(order_lines[0].keys()), order_lines))
    sql.append(insert_sql("shipments", list(shipments[0].keys()), shipments))
    sql.append(insert_sql("inventory_movements", list(inventory[0].keys()), inventory))
    (DATABASE_DIR / "04_generated_fact_seed.sql").write_text("\n".join(sql), encoding="utf-8")

    print(f"Generated {len(purchase_orders)} purchase orders, {len(order_lines)} lines, and {len(inventory)} inventory movements.")
    print("Wrote CSV files to data/ and SQL seed to database/04_generated_fact_seed.sql")


if __name__ == "__main__":
    main()
