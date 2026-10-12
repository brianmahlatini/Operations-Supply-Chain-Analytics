# Power BI DAX Measures

Use these measures after importing the PostgreSQL tables or views.

```DAX
Total Ordered Units = SUM(order_lines[ordered_units])

Fulfilled Units = SUM(order_lines[fulfilled_units])

Backordered Units = SUM(order_lines[backordered_units])

Service Level = DIVIDE([Fulfilled Units], [Total Ordered Units])

Stockout Rate =
DIVIDE(
    CALCULATE(COUNTROWS(order_lines), order_lines[stockout_flag] = TRUE()),
    COUNTROWS(order_lines)
)

Delayed Orders =
CALCULATE(
    DISTINCTCOUNT(purchase_orders[purchase_order_id]),
    purchase_orders[actual_delivery_date] > purchase_orders[expected_delivery_date]
)

On-Time Delivery Rate =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(purchase_orders[purchase_order_id]),
        purchase_orders[actual_delivery_date] <= purchase_orders[expected_delivery_date]
    ),
    DISTINCTCOUNT(purchase_orders[purchase_order_id])
)

Average Lead Time Days =
AVERAGEX(
    purchase_orders,
    DATEDIFF(purchase_orders[order_date], purchase_orders[actual_delivery_date], DAY)
)

Inventory Turnover =
DIVIDE(
    SUM(inventory_movements[issued_units]),
    AVERAGEX(
        inventory_movements,
        DIVIDE(inventory_movements[opening_units] + inventory_movements[closing_units], 2)
    )
)

Operational Cost =
SUM(purchase_orders[freight_cost])
    + SUM(shipments[transport_cost])
    + SUM(inventory_movements[holding_cost])
```
