from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class QualityCheck(Base):
    id = Column(Integer, primary_key=True, index=True)
    check_number = Column(String(50), unique=True, index=True)  # 检查单号
    product_id = Column(Integer, ForeignKey("product.id"))
    inspector_id = Column(Integer, ForeignKey("user.id"))  # 检查人
    batch_number = Column(String(50))  # 批次号
    check_type = Column(String(50))  # 检查类型：入库检查/在库检查/出库检查
    check_time = Column(DateTime(timezone=True), server_default=func.now())
    quality_level = Column(String(20))  # 质量等级：优/良/合格/不合格
    temperature = Column(Float)  # 温度记录（如果需要）
    humidity = Column(Float)  # 湿度记录（如果需要）
    appearance_check = Column(Boolean)  # 外观检查
    freshness_check = Column(Boolean)  # 新鲜度检查
    packaging_check = Column(Boolean)  # 包装检查
    check_images = Column(JSON)  # 检查图片路径列表
    check_result = Column(String(20))  # 检查结果：通过/不通过
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    product = relationship("Product", back_populates="quality_checks")
    inspector = relationship("User", foreign_keys=[inspector_id])

class QualityStandard(Base):
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    category = Column(String(50))  # 适用品类
    standard_name = Column(String(100))  # 标准名称
    standard_content = Column(JSON)  # 标准内容（JSON格式存储具体检查项）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    product = relationship("Product")