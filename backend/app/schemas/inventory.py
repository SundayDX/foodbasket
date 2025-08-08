from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class InventoryBase(BaseModel):
    product_id: int = Field(..., description="商品ID")
    quantity: float = Field(..., description="当前库存量")
    min_quantity: Optional[float] = Field(None, description="最小库存警戒线")
    max_quantity: Optional[float] = Field(None, description="最大库存警戒线")
    location: Optional[str] = Field(None, description="库存位置")
    batch_number: Optional[str] = Field(None, description="批次号")
    notes: Optional[str] = Field(None, description="备注")

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[float] = None
    min_quantity: Optional[float] = None
    max_quantity: Optional[float] = None
    location: Optional[str] = None
    batch_number: Optional[str] = None
    notes: Optional[str] = None

class InventoryInDBBase(InventoryBase):
    id: int
    last_check_time: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Inventory(InventoryInDBBase):
    pass

class InventoryInfo(BaseModel):
    quantity: float
    min_quantity: Optional[float] = None
    max_quantity: Optional[float] = None
    location: Optional[str] = None
    batch_number: Optional[str] = None

    class Config:
        orm_mode = True

# 库存交易相关Schema
class InventoryTransactionBase(BaseModel):
    inventory_id: int = Field(..., description="库存ID")
    transaction_type: str = Field(..., description="交易类型")
    quantity: float = Field(..., description="交易数量")
    batch_number: Optional[str] = Field(None, description="批次号")
    notes: Optional[str] = Field(None, description="备注")

class InventoryTransactionCreate(InventoryTransactionBase):
    pass

class InventoryTransactionUpdate(BaseModel):
    transaction_type: Optional[str] = None
    quantity: Optional[float] = None
    batch_number: Optional[str] = None
    notes: Optional[str] = None

class InventoryTransactionInDBBase(InventoryTransactionBase):
    id: int
    operator_id: int
    transaction_time: datetime

    class Config:
        orm_mode = True

class InventoryTransaction(InventoryTransactionInDBBase):
    pass