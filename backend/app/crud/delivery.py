from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.crud.base import CRUDBase
from app.models.delivery import Delivery, DeliveryPoint, DeliveryItem
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate

class CRUDDelivery(CRUDBase[Delivery, DeliveryCreate, DeliveryUpdate]):
    def create_with_points_and_items(
        self, db: Session, *, obj_in: DeliveryCreate
    ) -> Delivery:
        # 创建配送单主记录
        delivery_data = obj_in.dict(exclude={"delivery_points", "delivery_items"})
        db_obj = Delivery(**delivery_data)
        db.add(db_obj)
        db.flush()  # 获取delivery_id

        # 创建配送点记录
        for point in obj_in.delivery_points:
            point_data = jsonable_encoder(point)
            db_point = DeliveryPoint(**point_data, delivery_id=db_obj.id)
            db.add(db_point)

        # 创建配送商品记录
        for item in obj_in.delivery_items:
            item_data = jsonable_encoder(item)
            db_item = DeliveryItem(**item_data, delivery_id=db_obj.id)
            db.add(db_item)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_number(self, db: Session, *, delivery_number: str) -> Optional[Delivery]:
        return db.query(Delivery).filter(Delivery.delivery_number == delivery_number).first()

    def get_by_driver(
        self, db: Session, *, driver_id: int, skip: int = 0, limit: int = 100
    ) -> List[Delivery]:
        return (
            db.query(Delivery)
            .filter(Delivery.driver_id == driver_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Delivery]:
        return (
            db.query(Delivery)
            .filter(Delivery.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_deliveries(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Delivery]:
        return (
            db.query(Delivery)
            .filter(Delivery.status.in_(["待发货", "配送中"]))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_delivery_point(
        self,
        db: Session,
        *,
        delivery_point_id: int,
        status: str,
        actual_arrival_time: Optional[str] = None,
        signature_image: Optional[str] = None
    ) -> DeliveryPoint:
        delivery_point = db.query(DeliveryPoint).filter(
            DeliveryPoint.id == delivery_point_id
        ).first()
        
        if delivery_point:
            update_data = {"status": status}
            if actual_arrival_time:
                update_data["actual_arrival_time"] = actual_arrival_time
            if signature_image:
                update_data["signature_image"] = signature_image
            
            for field, value in update_data.items():
                setattr(delivery_point, field, value)
            
            # 检查是否所有配送点都已完成
            delivery = db.query(Delivery).filter(
                Delivery.id == delivery_point.delivery_id
            ).first()
            
            all_points = db.query(DeliveryPoint).filter(
                DeliveryPoint.delivery_id == delivery.id
            ).all()
            
            if all(point.status == "已完成" for point in all_points):
                delivery.status = "已完成"
                db.add(delivery)
            
            db.add(delivery_point)
            db.commit()
            db.refresh(delivery_point)
            return delivery_point
        return None

    def complete_delivery(
        self,
        db: Session,
        *,
        delivery_id: int,
        total_distance: float,
        fuel_consumption: float
    ) -> Delivery:
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
        if delivery:
            delivery.status = "已完成"
            delivery.total_distance = total_distance
            delivery.fuel_consumption = fuel_consumption
            db.add(delivery)
            db.commit()
            db.refresh(delivery)
        return delivery

class CRUDDeliveryPoint(CRUDBase[DeliveryPoint, Any, Any]):
    def get_by_delivery(
        self, db: Session, *, delivery_id: int
    ) -> List[DeliveryPoint]:
        return (
            db.query(DeliveryPoint)
            .filter(DeliveryPoint.delivery_id == delivery_id)
            .order_by(DeliveryPoint.sequence)
            .all()
        )

class CRUDDeliveryItem(CRUDBase[DeliveryItem, Any, Any]):
    def get_by_delivery(
        self, db: Session, *, delivery_id: int
    ) -> List[DeliveryItem]:
        return (
            db.query(DeliveryItem)
            .filter(DeliveryItem.delivery_id == delivery_id)
            .all()
        )

delivery = CRUDDelivery(Delivery)
delivery_point = CRUDDeliveryPoint(DeliveryPoint)
delivery_item = CRUDDeliveryItem(DeliveryItem)