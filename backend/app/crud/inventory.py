from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.inventory import Inventory, InventoryTransaction
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryTransactionCreate

class CRUDInventory(CRUDBase[Inventory, InventoryCreate, InventoryUpdate]):
    def get_by_product(self, db: Session, *, product_id: int) -> Optional[Inventory]:
        return db.query(Inventory).filter(Inventory.product_id == product_id).first()

    def get_by_batch(self, db: Session, *, batch_number: str) -> List[Inventory]:
        return db.query(Inventory).filter(Inventory.batch_number == batch_number).all()

    def get_low_stock(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Inventory]:
        return (
            db.query(Inventory)
            .filter(Inventory.quantity <= Inventory.min_quantity)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_high_stock(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Inventory]:
        return (
            db.query(Inventory)
            .filter(Inventory.quantity >= Inventory.max_quantity)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_quantity(
        self, db: Session, *, db_obj: Inventory, quantity_change: float
    ) -> Inventory:
        db_obj.quantity += quantity_change
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDInventoryTransaction(CRUDBase[InventoryTransaction, InventoryTransactionCreate, Dict[str, Any]]):
    def create_with_inventory_update(
        self,
        db: Session,
        *,
        obj_in: InventoryTransactionCreate,
        operator_id: int
    ) -> InventoryTransaction:
        # 创建交易记录
        obj_in_data = obj_in.dict()
        db_obj = InventoryTransaction(**obj_in_data, operator_id=operator_id)
        db.add(db_obj)
        
        # 更新库存
        inventory = db.query(Inventory).filter(Inventory.id == obj_in.inventory_id).first()
        if not inventory:
            raise ValueError("库存记录不存在")
        
        # 根据交易类型更新库存数量
        if obj_in.transaction_type in ["入库", "调整增加"]:
            inventory.quantity += obj_in.quantity
        elif obj_in.transaction_type in ["出库", "调整减少"]:
            if inventory.quantity < abs(obj_in.quantity):
                raise ValueError("库存不足")
            inventory.quantity -= abs(obj_in.quantity)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_inventory(
        self, db: Session, *, inventory_id: int, skip: int = 0, limit: int = 100
    ) -> List[InventoryTransaction]:
        return (
            db.query(InventoryTransaction)
            .filter(InventoryTransaction.inventory_id == inventory_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

inventory = CRUDInventory(Inventory)
inventory_transaction = CRUDInventoryTransaction(InventoryTransaction)