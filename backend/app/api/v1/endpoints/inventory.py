from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Inventory])
def read_inventories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取库存列表
    """
    inventories = crud.inventory.get_multi(db, skip=skip, limit=limit)
    return inventories

@router.post("/", response_model=schemas.Inventory)
def create_inventory(
    *,
    db: Session = Depends(deps.get_db),
    inventory_in: schemas.InventoryCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    创建新库存记录（仅限超级管理员）
    """
    # 检查商品是否存在
    product = crud.product.get(db, id=inventory_in.product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="商品不存在",
        )
    # 检查是否已存在该商品的库存记录
    inventory = crud.inventory.get_by_product(db, product_id=inventory_in.product_id)
    if inventory:
        raise HTTPException(
            status_code=400,
            detail="该商品的库存记录已存在",
        )
    inventory = crud.inventory.create(db, obj_in=inventory_in)
    return inventory

@router.get("/low-stock", response_model=List[schemas.Inventory])
def read_low_stock_inventories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取库存不足的商品列表
    """
    inventories = crud.inventory.get_low_stock(db, skip=skip, limit=limit)
    return inventories

@router.get("/high-stock", response_model=List[schemas.Inventory])
def read_high_stock_inventories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取库存过高的商品列表
    """
    inventories = crud.inventory.get_high_stock(db, skip=skip, limit=limit)
    return inventories

@router.get("/{id}", response_model=schemas.Inventory)
def read_inventory(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    根据ID获取库存信息
    """
    inventory = crud.inventory.get(db, id=id)
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    return inventory

@router.put("/{id}", response_model=schemas.Inventory)
def update_inventory(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    inventory_in: schemas.InventoryUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    更新库存信息（仅限超级管理员）
    """
    inventory = crud.inventory.get(db, id=id)
    if not inventory:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    inventory = crud.inventory.update(db, db_obj=inventory, obj_in=inventory_in)
    return inventory

@router.post("/transactions/", response_model=schemas.InventoryTransaction)
def create_inventory_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: schemas.InventoryTransactionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建库存交易记录
    """
    try:
        transaction = crud.inventory_transaction.create_with_inventory_update(
            db=db,
            obj_in=transaction_in,
            operator_id=current_user.id
        )
        return transaction
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.get("/transactions/{inventory_id}", response_model=List[schemas.InventoryTransaction])
def read_inventory_transactions(
    *,
    db: Session = Depends(deps.get_db),
    inventory_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取指定库存的交易记录
    """
    transactions = crud.inventory_transaction.get_by_inventory(
        db=db, inventory_id=inventory_id, skip=skip, limit=limit
    )
    return transactions

@router.get("/product/{product_id}", response_model=schemas.Inventory)
def read_inventory_by_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    根据商品ID获取库存信息
    """
    inventory = crud.inventory.get_by_product(db, product_id=product_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="该商品的库存记录不存在")
    return inventory

@router.get("/batch/{batch_number}", response_model=List[schemas.Inventory])
def read_inventory_by_batch(
    *,
    db: Session = Depends(deps.get_db),
    batch_number: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    根据批次号获取库存信息
    """
    inventories = crud.inventory.get_by_batch(db, batch_number=batch_number)
    return inventories