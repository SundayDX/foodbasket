from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Product]:
        return db.query(Product).filter(Product.code == code).first()
    
    def get_by_category(self, db: Session, *, category: str, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(Product).filter(Product.category == category).offset(skip).limit(limit).all()
    
    def get_by_supplier(self, db: Session, *, supplier: str, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(Product).filter(Product.supplier == supplier).offset(skip).limit(limit).all()
    
    def get_multi_with_inventory(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(Product)
            .outerjoin(Product.inventory)
            .offset(skip)
            .limit(limit)
            .all()
        )

product = CRUDProduct(Product)