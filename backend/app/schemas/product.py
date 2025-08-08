from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., description="商品名称")
    code: str = Field(..., description="商品编码")
    category: str = Field(..., description="商品类别")
    unit: str = Field(..., description="单位（如：kg, 箱, 个）")
    description: Optional[str] = Field(None, description="商品描述")
    supplier: str = Field(..., description="供应商")
    purchase_price: float = Field(..., description="采购价")
    selling_price: float = Field(..., description="销售价")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    description: Optional[str] = None
    supplier: Optional[str] = None
    purchase_price: Optional[float] = None
    selling_price: Optional[float] = None

class ProductInDBBase(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Product(ProductInDBBase):
    pass

class ProductWithInventory(ProductInDBBase):
    inventory: Optional["InventoryInfo"] = None

from app.schemas.inventory import InventoryInfo
ProductWithInventory.update_forward_refs()