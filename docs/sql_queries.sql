-- Executive KPI layer
SELECT * FROM vw_operational_kpis;

-- Supplier lead-time and delivery reliability
SELECT
    supplier_name,
    risk_tier,
    purchase_orders,
    average_lead_time_days,
    on_time_delivery_rate,
    delayed_orders,
    freight_cost
FROM vw_supplier_performance
ORDER BY on_time_delivery_rate ASC;

-- Inventory bottlenecks by product and region
SELECT
    product_name,
    category,
    region_name,
    supplier_name,
    fulfillment_rate,
    stockout_rate,
    inventory_turnover,
    days_below_reorder_point,
    holding_cost
FROM vw_product_region_performance
ORDER BY stockout_rate DESC, days_below_reorder_point DESC;

-- Slow-moving and understocked inventory
SELECT
    sku,
    product_name,
    region_name,
    issued_units,
    average_inventory_units,
    inventory_turnover,
    days_below_reorder_point
FROM vw_inventory_turnover
ORDER BY inventory_turnover ASC, days_below_reorder_point DESC;
