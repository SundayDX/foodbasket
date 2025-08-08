from fastapi import APIRouter
from app.api.v1.endpoints import auth, products, inventory, delivery, damage_reports, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(products.router, prefix="/products", tags=["商品管理"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["库存管理"])
api_router.include_router(delivery.router, prefix="/delivery", tags=["配送管理"])
api_router.include_router(damage_reports.router, prefix="/damage-reports", tags=["报损管理"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["数据分析"])