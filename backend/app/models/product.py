from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    code = Column(String(50), unique=True, index=True)  # 商品编码
    category = Column(String(50), index=True)  # 商品类别
    unit = Column(String(20))  # 单位（如：kg, 箱, 个）
    description = Column(Text)
    supplier = Column(String(100), index=True)  # 供应商
    purchase_price = Column(Float)  # 采购价
    selling_price = Column(Float)  # 销售价
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    quality_checks = relationship("QualityCheck", back_populates="product")
    damage_reports = relationship("DamageReport", back_populates="product")