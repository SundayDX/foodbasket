from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Product])
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取商品列表
    """
    products = crud.product.get_multi(db, skip=skip, limit=limit)
    return products

@router.get("/with-inventory", response_model=List[schemas.ProductWithInventory])
def read_products_with_inventory(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取商品列表（包含库存信息）
    """
    products = crud.product.get_multi_with_inventory(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    创建新商品（仅限超级管理员）
    """
    product = crud.product.get_by_code(db, code=product_in.code)
    if product:
        raise HTTPException(
            status_code=400,
            detail="该商品编码已存在",
        )
    product = crud.product.create(db, obj_in=product_in)
    return product

@router.put("/{id}", response_model=schemas.Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    product_in: schemas.ProductUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    更新商品信息（仅限超级管理员）
    """
    product = crud.product.get(db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    product = crud.product.update(db, db_obj=product, obj_in=product_in)
    return product

@router.get("/{id}", response_model=schemas.Product)
def read_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    根据ID获取商品信息
    """
    product = crud.product.get(db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

@router.delete("/{id}", response_model=schemas.Product)
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除商品（仅限超级管理员）
    """
    product = crud.product.get(db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    product = crud.product.remove(db, id=id)
    return product

@router.get("/category/{category}", response_model=List[schemas.Product])
def read_products_by_category(
    *,
    db: Session = Depends(deps.get_db),
    category: str,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    根据类别获取商品列表
    """
    products = crud.product.get_by_category(
        db, category=category, skip=skip, limit=limit
    )
    return products

@router.get("/supplier/{supplier}", response_model=List[schemas.Product])
def read_products_by_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier: str,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    根据供应商获取商品列表
    """
    products = crud.product.get_by_supplier(
        db, supplier=supplier, skip=skip, limit=limit
    )
    return products