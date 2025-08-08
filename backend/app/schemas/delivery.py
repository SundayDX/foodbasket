from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class DeliveryPointBase(BaseModel):
    sequence: int = Field(..., description="配送顺序")
    customer_name: str = Field(..., description="客户名称")
    address: str = Field(..., description="配送地址")
    contact_phone: str = Field(..., description="联系电话")
    planned_arrival_time: datetime = Field(..., description="计划到达时间")
    notes: Optional[str] = Field(None, description="备注")

class DeliveryPointCreate(DeliveryPointBase):
    pass

class DeliveryPointUpdate(BaseModel):
    sequence: Optional[int] = None
    customer_name: Optional[str] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    planned_arrival_time: Optional[datetime] = None
    actual_arrival_time: Optional[datetime] = None
    status: Optional[str] = None
    signature_image: Optional[str] = None
    notes: Optional[str] = None

class DeliveryPointInDBBase(DeliveryPointBase):
    id: int
    delivery_id: int
    status: str
    actual_arrival_time: Optional[datetime] = None
    signature_image: Optional[str] = None

    class Config:
        orm_mode = True

class DeliveryPoint(DeliveryPointInDBBase):
    pass

class DeliveryItemBase(BaseModel):
    product_id: int = Field(..., description="商品ID")
    quantity: float = Field(..., description="数量")
    unit_price: float = Field(..., description="单价")
    total_price: float = Field(..., description="总价")
    notes: Optional[str] = Field(None, description="备注")

class DeliveryItemCreate(DeliveryItemBase):
    pass

class DeliveryItemUpdate(BaseModel):
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    notes: Optional[str] = None

class DeliveryItemInDBBase(DeliveryItemBase):
    id: int
    delivery_id: int

    class Config:
        orm_mode = True

class DeliveryItem(DeliveryItemInDBBase):
    pass

class DeliveryBase(BaseModel):
    delivery_number: str = Field(..., description="配送单号")
    driver_id: int = Field(..., description="司机ID")
    vehicle_number: str = Field(..., description="车牌号")
    start_time: datetime = Field(..., description="出发时间")
    route_info: Dict[str, Any] = Field(..., description="路线信息")
    notes: Optional[str] = Field(None, description="备注")

class DeliveryCreate(DeliveryBase):
    delivery_points: List[DeliveryPointCreate]
    delivery_items: List[DeliveryItemCreate]

class DeliveryUpdate(BaseModel):
    vehicle_number: Optional[str] = None
    status: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_distance: Optional[float] = None
    fuel_consumption: Optional[float] = None
    route_info: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class DeliveryInDBBase(DeliveryBase):
    id: int
    status: str
    end_time: Optional[datetime] = None
    total_distance: Optional[float] = None
    fuel_consumption: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Delivery(DeliveryInDBBase):
    delivery_points: List[DeliveryPoint]
    delivery_items: List[DeliveryItem]

class DeliveryWithDetails(Delivery):
    driver: Dict[str, Any]  # 包含司机信息