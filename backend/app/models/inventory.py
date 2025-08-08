from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Inventory(Base):
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), unique=True)
    quantity = Column(Float, default=0)  # 当前库存量
    min_quantity = Column(Float)  # 最小库存警戒线
    max_quantity = Column(Float)  # 最大库存警戒线
    location = Column(String(100))  # 库存位置
    batch_number = Column(String(50))  # 批次号
    notes = Column(Text)
    last_check_time = Column(DateTime(timezone=True))  # 最后盘点时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    product = relationship("Product", back_populates="inventory")

class InventoryTransaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    transaction_type = Column(String(20))  # 入库/出库/调整
    quantity = Column(Float)  # 变动数量（正数为入库，负数为出库）
    batch_number = Column(String(50))  # 批次号
    operator_id = Column(Integer, ForeignKey("user.id"))
    transaction_time = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    
    # 关联关系
    operator = relationship("User")
    inventory = relationship("Inventory")