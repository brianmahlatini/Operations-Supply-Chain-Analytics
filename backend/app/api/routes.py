from fastapi import APIRouter

from app.models.schemas import OperationalKpis, ProductRegionPerformance, Recommendation, SupplierPerformance
from app.services import analytics


router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/kpis", response_model=OperationalKpis)
def kpis():
    return analytics.get_kpis()


@router.get("/suppliers", response_model=list[SupplierPerformance])
def suppliers():
    return analytics.get_supplier_performance()


@router.get("/product-region", response_model=list[ProductRegionPerformance])
def product_region():
    return analytics.get_product_region_performance()


@router.get("/inventory-turnover")
def inventory_turnover():
    return analytics.get_inventory_turnover()


@router.get("/recommendations", response_model=list[Recommendation])
def recommendations():
    return analytics.get_recommendations()
