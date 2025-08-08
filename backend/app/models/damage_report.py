from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class DamageReport(Base):
    id = Column(Integer, primary_key=True, index=True)
    report_number = Column(String(50), unique=True, index=True)  # 报损单号
    product_id = Column(Integer, ForeignKey("product.id"))
    reporter_id = Column(Integer, ForeignKey("user.id"))  # 报损人
    approver_id = Column(Integer, ForeignKey("user.id"))  # 审批人
    quantity = Column(Float)  # 报损数量
    damage_type = Column(String(50))  # 报损类型：自然损耗/运输损坏/质量问题等
    batch_number = Column(String(50))  # 批次号
    status = Column(String(20))  # 状态：待审核/已审核/已拒绝
    damage_images = Column(JSON)  # 报损图片路径列表
    reason = Column(Text)  # 报损原因
    handling_method = Column(String(50))  # 处理方式：销毁/降价销售/其他
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    approved_at = Column(DateTime(timezone=True))  # 审批时间

    # 关联关系
    product = relationship("Product", back_populates="damage_reports")
    reporter = relationship("User", foreign_keys=[reporter_id])
    approver = relationship("User", foreign_keys=[approver_id])