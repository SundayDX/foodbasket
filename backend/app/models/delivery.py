from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Delivery(Base):
    id = Column(Integer, primary_key=True, index=True)
    delivery_number = Column(String(50), unique=True, index=True)  # 配送单号
    driver_id = Column(Integer, ForeignKey("user.id"))
    vehicle_number = Column(String(20))  # 车牌号
    status = Column(String(20))  # 配送状态：待发货/配送中/已完成/已取消
    start_time = Column(DateTime(timezone=True))  # 出发时间
    end_time = Column(DateTime(timezone=True))  # 完成时间
    total_distance = Column(Float)  # 总里程
    fuel_consumption = Column(Float)  # 油耗
    route_info = Column(JSON)  # 路线信息，包含配送点顺序等
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    driver = relationship("User", foreign_keys=[driver_id])
    delivery_items = relationship("DeliveryItem", back_populates="delivery")
    delivery_points = relationship("DeliveryPoint", back_populates="delivery")

class DeliveryItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("delivery.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Float)
    unit_price = Column(Float)
    total_price = Column(Float)
    notes = Column(Text)

    # 关联关系
    delivery = relationship("Delivery", back_populates="delivery_items")
    product = relationship("Product")

class DeliveryPoint(Base):
    id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("delivery.id"))
    sequence = Column(Integer)  # 配送顺序
    customer_name = Column(String(100))
    address = Column(String(200))
    contact_phone = Column(String(20))
    planned_arrival_time = Column(DateTime(timezone=True))
    actual_arrival_time = Column(DateTime(timezone=True))
    status = Column(String(20))  # 配送点状态：待配送/已到达/已完成/已取消
    signature_image = Column(String(200))  # 签收图片路径
    notes = Column(Text)

    # 关联关系
    delivery = relationship("Delivery", back_populates="delivery_points")