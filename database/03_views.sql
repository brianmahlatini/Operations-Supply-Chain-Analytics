CREATE OR REPLACE VIEW vw_inventory_turnover AS
SELECT
    p.product_id,
    p.sku,
    p.product_name,
    p.category,
    r.region_name,
    SUM(im.issued_units) AS issued_units,
    ROUND(AVG((im.opening_units + im.closing_units) / 2.0), 2) AS average_inventory_units,
    ROUND(SUM(im.issued_units)::NUMERIC / NULLIF(AVG((im.opening_units + im.closing_units) / 2.0), 0), 2) AS inventory_turnover,
    SUM(CASE WHEN im.closing_units <= p.reorder_point THEN 1 ELSE 0 END) AS days_below_reorder_point,
    ROUND(SUM(im.holding_cost), 2) AS holding_cost
FROM inventory_movements im
JOIN products p ON p.product_id = im.product_id
JOIN regions r ON r.region_id = im.region_id
GROUP BY p.product_id, p.sku, p.product_name, p.category, r.region_name;

CREATE OR REPLACE VIEW vw_order_fulfillment AS
SELECT
    p.product_id,
    p.sku,
    p.product_name,
    p.category,
    s.supplier_name,
    r.region_name,
    COUNT(DISTINCT po.purchase_order_id) AS purchase_orders,
    SUM(ol.ordered_units) AS ordered_units,
    SUM(ol.fulfilled_units) AS fulfilled_units,
    SUM(ol.backordered_units) AS backordered_units,
    ROUND(SUM(ol.fulfilled_units)::NUMERIC / NULLIF(SUM(ol.ordered_units), 0), 4) AS fulfillment_rate,
    ROUND(SUM(CASE WHEN ol.stockout_flag THEN 1 ELSE 0 END)::NUMERIC / NULLIF(COUNT(*), 0), 4) AS stockout_rate,
    SUM(CASE WHEN po.actual_delivery_date > po.expected_delivery_date THEN 1 ELSE 0 END) AS delayed_orders
FROM order_lines ol
JOIN purchase_orders po ON po.purchase_order_id = ol.purchase_order_id
JOIN products p ON p.product_id = ol.product_id
JOIN suppliers s ON s.supplier_id = po.supplier_id
JOIN regions r ON r.region_id = po.region_id
GROUP BY p.product_id, p.sku, p.product_name, p.category, s.supplier_name, r.region_name;

CREATE OR REPLACE VIEW vw_supplier_performance AS
SELECT
    s.supplier_id,
    s.supplier_name,
    s.category,
    s.risk_tier,
    COUNT(po.purchase_order_id) AS purchase_orders,
    ROUND(AVG((COALESCE(po.actual_delivery_date, po.expected_delivery_date) - po.order_date)::NUMERIC), 2) AS average_lead_time_days,
    ROUND(AVG((po.expected_delivery_date - po.order_date)::NUMERIC), 2) AS contracted_expected_days,
    ROUND(SUM(CASE WHEN po.actual_delivery_date <= po.expected_delivery_date THEN 1 ELSE 0 END)::NUMERIC / NULLIF(COUNT(*), 0), 4) AS on_time_delivery_rate,
    SUM(CASE WHEN po.actual_delivery_date > po.expected_delivery_date THEN 1 ELSE 0 END) AS delayed_orders,
    SUM(po.quality_issue_units) AS quality_issue_units,
    ROUND(SUM(po.freight_cost), 2) AS freight_cost
FROM suppliers s
JOIN purchase_orders po ON po.supplier_id = s.supplier_id
GROUP BY s.supplier_id, s.supplier_name, s.category, s.risk_tier;

CREATE OR REPLACE VIEW vw_product_region_performance AS
SELECT
    ofv.product_name,
    ofv.category,
    ofv.region_name,
    ofv.supplier_name,
    ofv.fulfillment_rate,
    ofv.stockout_rate,
    it.inventory_turnover,
    it.days_below_reorder_point,
    it.holding_cost
FROM vw_order_fulfillment ofv
LEFT JOIN vw_inventory_turnover it
    ON it.product_id = ofv.product_id
    AND it.region_name = ofv.region_name;

CREATE OR REPLACE VIEW vw_operational_kpis AS
WITH line_metrics AS (
    SELECT
        SUM(fulfilled_units) AS fulfilled_units,
        SUM(ordered_units) AS ordered_units,
        SUM(CASE WHEN stockout_flag THEN 1 ELSE 0 END) AS stockout_lines,
        COUNT(*) AS order_lines
    FROM order_lines
),
po_metrics AS (
    SELECT
        COUNT(*) AS purchase_orders,
        SUM(CASE WHEN actual_delivery_date <= expected_delivery_date THEN 1 ELSE 0 END) AS on_time_orders,
        SUM(CASE WHEN actual_delivery_date > expected_delivery_date THEN 1 ELSE 0 END) AS delayed_orders,
        AVG((actual_delivery_date - order_date)::NUMERIC) AS average_lead_time_days,
        SUM(freight_cost) AS freight_cost
    FROM purchase_orders
),
shipment_costs AS (
    SELECT SUM(transport_cost) AS transport_cost
    FROM shipments
),
inventory_costs AS (
    SELECT SUM(holding_cost) AS holding_cost
    FROM inventory_movements
)
SELECT
    ROUND(line_metrics.fulfilled_units::NUMERIC / NULLIF(line_metrics.ordered_units, 0), 4) AS service_level,
    ROUND(line_metrics.stockout_lines::NUMERIC / NULLIF(line_metrics.order_lines, 0), 4) AS stockout_rate,
    ROUND(po_metrics.on_time_orders::NUMERIC / NULLIF(po_metrics.purchase_orders, 0), 4) AS on_time_delivery_rate,
    ROUND(po_metrics.average_lead_time_days, 2) AS average_lead_time_days,
    ROUND(po_metrics.freight_cost + shipment_costs.transport_cost + inventory_costs.holding_cost, 2) AS operational_cost,
    po_metrics.delayed_orders
FROM line_metrics
CROSS JOIN po_metrics
CROSS JOIN shipment_costs
CROSS JOIN inventory_costs;
