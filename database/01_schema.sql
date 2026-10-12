DROP VIEW IF EXISTS vw_supplier_performance;
DROP VIEW IF EXISTS vw_inventory_turnover;
DROP VIEW IF EXISTS vw_order_fulfillment;
DROP VIEW IF EXISTS vw_product_region_performance;
DROP VIEW IF EXISTS vw_operational_kpis;

DROP TABLE IF EXISTS inventory_movements;
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS order_lines;
DROP TABLE IF EXISTS purchase_orders;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS regions;

CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(80) NOT NULL UNIQUE,
    country VARCHAR(80) NOT NULL,
    warehouse_name VARCHAR(120) NOT NULL
);

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(120) NOT NULL,
    category VARCHAR(80) NOT NULL,
    contracted_lead_time_days INTEGER NOT NULL CHECK (contracted_lead_time_days > 0),
    risk_tier VARCHAR(20) NOT NULL CHECK (risk_tier IN ('Low', 'Medium', 'High'))
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(40) NOT NULL UNIQUE,
    product_name VARCHAR(140) NOT NULL,
    category VARCHAR(80) NOT NULL,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(supplier_id),
    unit_cost NUMERIC(12, 2) NOT NULL CHECK (unit_cost >= 0),
    reorder_point INTEGER NOT NULL CHECK (reorder_point >= 0),
    target_stock INTEGER NOT NULL CHECK (target_stock >= reorder_point)
);

CREATE TABLE purchase_orders (
    purchase_order_id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(supplier_id),
    region_id INTEGER NOT NULL REFERENCES regions(region_id),
    order_date DATE NOT NULL,
    expected_delivery_date DATE NOT NULL,
    actual_delivery_date DATE,
    freight_cost NUMERIC(12, 2) NOT NULL DEFAULT 0,
    quality_issue_units INTEGER NOT NULL DEFAULT 0 CHECK (quality_issue_units >= 0)
);

CREATE TABLE order_lines (
    order_line_id SERIAL PRIMARY KEY,
    purchase_order_id INTEGER NOT NULL REFERENCES purchase_orders(purchase_order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    ordered_units INTEGER NOT NULL CHECK (ordered_units > 0),
    fulfilled_units INTEGER NOT NULL CHECK (fulfilled_units >= 0),
    backordered_units INTEGER NOT NULL CHECK (backordered_units >= 0),
    stockout_flag BOOLEAN NOT NULL DEFAULT FALSE,
    delay_reason VARCHAR(80) NOT NULL DEFAULT 'None'
);

CREATE TABLE shipments (
    shipment_id SERIAL PRIMARY KEY,
    purchase_order_id INTEGER NOT NULL REFERENCES purchase_orders(purchase_order_id),
    carrier VARCHAR(80) NOT NULL,
    service_level VARCHAR(40) NOT NULL,
    shipped_date DATE NOT NULL,
    delivered_date DATE NOT NULL,
    transport_cost NUMERIC(12, 2) NOT NULL CHECK (transport_cost >= 0)
);

CREATE TABLE inventory_movements (
    movement_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    region_id INTEGER NOT NULL REFERENCES regions(region_id),
    movement_date DATE NOT NULL,
    opening_units INTEGER NOT NULL CHECK (opening_units >= 0),
    received_units INTEGER NOT NULL DEFAULT 0 CHECK (received_units >= 0),
    issued_units INTEGER NOT NULL DEFAULT 0 CHECK (issued_units >= 0),
    closing_units INTEGER NOT NULL CHECK (closing_units >= 0),
    holding_cost NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (holding_cost >= 0)
);

CREATE INDEX idx_purchase_orders_supplier_region ON purchase_orders(supplier_id, region_id);
CREATE INDEX idx_purchase_orders_dates ON purchase_orders(order_date, actual_delivery_date);
CREATE INDEX idx_order_lines_product ON order_lines(product_id);
CREATE INDEX idx_inventory_product_region_date ON inventory_movements(product_id, region_id, movement_date);
