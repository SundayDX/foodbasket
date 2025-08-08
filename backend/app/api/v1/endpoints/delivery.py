from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Delivery])
def read_deliveries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取配送单列表
    """
    deliveries = crud.delivery.get_multi(db, skip=skip, limit=limit)
    return deliveries

@router.post("/", response_model=schemas.Delivery)
def create_delivery(
    *,
    db: Session = Depends(deps.get_db),
    delivery_in: schemas.DeliveryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建新配送单
    """
    # 检查配送单号是否已存在
    delivery = crud.delivery.get_by_number(db, delivery_number=delivery_in.delivery_number)
    if delivery:
        raise HTTPException(
            status_code=400,
            detail="配送单号已存在",
        )
    delivery = crud.delivery.create_with_points_and_items(db, obj_in=delivery_in)
    return delivery

@router.get("/active", response_model=List[schemas.Delivery])
def read_active_deliveries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取进行中的配送单列表
    """
    deliveries = crud.delivery.get_active_deliveries(db, skip=skip, limit=limit)
    return deliveries

@router.get("/driver/{driver_id}", response_model=List[schemas.Delivery])
def read_driver_deliveries(
    *,
    db: Session = Depends(deps.get_db),
    driver_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取指定司机的配送单列表
    """
    deliveries = crud.delivery.get_by_driver(
        db, driver_id=driver_id, skip=skip, limit=limit
    )
    return deliveries

@router.get("/{id}", response_model=schemas.DeliveryWithDetails)
def read_delivery(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    根据ID获取配送单详情
    """
    delivery = crud.delivery.get(db, id=id)
    if not delivery:
        raise HTTPException(status_code=404, detail="配送单不存在")
    
    # 获取司机信息
    driver = crud.user.get(db, id=delivery.driver_id)
    if driver:
        driver_info = {
            "id": driver.id,
            "full_name": driver.full_name,
            "email": driver.email
        }
    else:
        driver_info = None
    
    # 构建返回数据
    delivery_data = schemas.Delivery.from_orm(delivery)
    return schemas.DeliveryWithDetails(
        **delivery_data.dict(),
        driver=driver_info
    )

@router.put("/{id}", response_model=schemas.Delivery)
def update_delivery(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    delivery_in: schemas.DeliveryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新配送单信息
    """
    delivery = crud.delivery.get(db, id=id)
    if not delivery:
        raise HTTPException(status_code=404, detail="配送单不存在")
    delivery = crud.delivery.update(db, db_obj=delivery, obj_in=delivery_in)
    return delivery

@router.post("/{id}/complete", response_model=schemas.Delivery)
def complete_delivery(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    total_distance: float,
    fuel_consumption: float,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    完成配送单
    """
    delivery = crud.delivery.complete_delivery(
        db,
        delivery_id=id,
        total_distance=total_distance,
        fuel_consumption=fuel_consumption
    )
    if not delivery:
        raise HTTPException(status_code=404, detail="配送单不存在")
    return delivery

@router.post("/points/{point_id}/update", response_model=schemas.DeliveryPoint)
def update_delivery_point(
    *,
    db: Session = Depends(deps.get_db),
    point_id: int,
    status: str,
    actual_arrival_time: str = None,
    signature_image: str = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新配送点状态
    """
    delivery_point = crud.delivery.update_delivery_point(
        db,
        delivery_point_id=point_id,
        status=status,
        actual_arrival_time=actual_arrival_time,
        signature_image=signature_image
    )
    if not delivery_point:
        raise HTTPException(status_code=404, detail="配送点不存在")
    return delivery_point

@router.get("/points/{delivery_id}", response_model=List[schemas.DeliveryPoint])
def read_delivery_points(
    *,
    db: Session = Depends(deps.get_db),
    delivery_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取配送单的所有配送点
    """
    points = crud.delivery_point.get_by_delivery(db, delivery_id=delivery_id)
    return points

@router.get("/items/{delivery_id}", response_model=List[schemas.DeliveryItem])
def read_delivery_items(
    *,
    db: Session = Depends(deps.get_db),
    delivery_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取配送单的所有商品
    """
    items = crud.delivery_item.get_by_delivery(db, delivery_id=delivery_id)
    return items