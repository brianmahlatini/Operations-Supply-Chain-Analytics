from decimal import Decimal

from pydantic import BaseModel


class OperationalKpis(BaseModel):
    service_level: Decimal | None
    stockout_rate: Decimal | None
    on_time_delivery_rate: Decimal | None
    average_lead_time_days: Decimal | None
    operational_cost: Decimal | None
    delayed_orders: int | None


class SupplierPerformance(BaseModel):
    supplier_name: str
    category: str
    risk_tier: str
    purchase_orders: int
    average_lead_time_days: Decimal | None
    contracted_expected_days: Decimal | None
    on_time_delivery_rate: Decimal | None
    delayed_orders: int
    quality_issue_units: int
    freight_cost: Decimal


class ProductRegionPerformance(BaseModel):
    product_name: str
    category: str
    region_name: str
    supplier_name: str
    fulfillment_rate: Decimal | None
    stockout_rate: Decimal | None
    inventory_turnover: Decimal | None
    days_below_reorder_point: int | None
    holding_cost: Decimal | None


class Recommendation(BaseModel):
    priority: str
    focus_area: str
    insight: str
    action: str
