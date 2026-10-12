from app.core.database import fetch_all, fetch_one


def get_kpis():
    return fetch_one("SELECT * FROM vw_operational_kpis")


def get_supplier_performance():
    return fetch_all("""
        SELECT *
        FROM vw_supplier_performance
        ORDER BY on_time_delivery_rate ASC, average_lead_time_days DESC
    """)


def get_product_region_performance():
    return fetch_all("""
        SELECT *
        FROM vw_product_region_performance
        ORDER BY stockout_rate DESC, days_below_reorder_point DESC, fulfillment_rate ASC
    """)


def get_inventory_turnover():
    return fetch_all("""
        SELECT *
        FROM vw_inventory_turnover
        ORDER BY inventory_turnover ASC, days_below_reorder_point DESC
    """)


def get_recommendations():
    supplier_risk = fetch_all("""
        SELECT supplier_name, on_time_delivery_rate, delayed_orders
        FROM vw_supplier_performance
        WHERE on_time_delivery_rate < 0.85
        ORDER BY on_time_delivery_rate ASC
        LIMIT 3
    """)
    stockout_risk = fetch_all("""
        SELECT product_name, region_name, stockout_rate, days_below_reorder_point
        FROM vw_product_region_performance
        WHERE stockout_rate > 0.12 OR days_below_reorder_point >= 8
        ORDER BY stockout_rate DESC, days_below_reorder_point DESC
        LIMIT 3
    """)

    recommendations = []
    for row in supplier_risk:
        recommendations.append({
            "priority": "High",
            "focus_area": "Supplier reliability",
            "insight": f"{row['supplier_name']} is below the 85% on-time delivery threshold with {row['delayed_orders']} delayed orders.",
            "action": "Review service-level terms, add expediting rules for critical SKUs, and qualify a secondary supplier.",
        })

    for row in stockout_risk:
        recommendations.append({
            "priority": "High",
            "focus_area": "Inventory availability",
            "insight": f"{row['product_name']} in {row['region_name']} shows elevated stockout risk.",
            "action": "Raise reorder points using demand variability and shift replenishment cadence from monthly to weekly review.",
        })

    recommendations.append({
        "priority": "Medium",
        "focus_area": "Operational cost",
        "insight": "Freight, transport, and holding cost are tracked together to expose the trade-off between expedite spend and excess stock.",
        "action": "Create a monthly cost-to-serve review by supplier, region, and product category.",
    })
    return recommendations
