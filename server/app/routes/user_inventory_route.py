from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import user_inventory_model, user_model, inventory_model, organization_model
from ..schemas import common_schema, user_schema, user_inventory_schema, inventory_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/users-inventories",
    tags=['Users | Inventories assigns']
)


@router.get("", response_model=List[user_inventory_schema.UserInventoryResponse])
async def get_users_inventories(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_inventories_query = db.query(
        user_inventory_model.UserInventory
    ).join(
        user_model.User, user_model.User.id == user_inventory_model.UserInventory.user_id
    ).join(
        inventory_model.Inventory, inventory_model.Inventory.id == user_inventory_model.UserInventory.inventory_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        users_inventories_query = users_inventories_query.offset(skip)

    if limit:
        users_inventories_query = users_inventories_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_inventories_query = users_inventories_query.order_by(
                desc(sort))
        else:
            users_inventories_query = users_inventories_query.order_by(sort)
    else:
        users_inventories_query = users_inventories_query.order_by(
            user_inventory_model.UserInventory.user_inventory_id)

    if limit == 1:
        users_inventories = users_inventories_query.first()
    else:
        users_inventories = users_inventories_query.all()

    if not users_inventories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_inventories


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_inventory_schema.UserInventoryResponse)
async def create_users_inventories(
    payload: user_inventory_schema.UserInventoryPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.users_id or not payload.inventory_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign users to inventory! Provide a valid request")

    users_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id.in_(payload.users_id)
    )
    users = users_query.all()
    if not users or len(users) != len(payload.users_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to inventory! Provide a valid user")

    inventory_query = db.query(
        inventory_model.Inventory
    ).join(
        organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.id == payload.inventory_id
    )
    inventory = inventory_query.first()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to inventory! Provide a valid inventory")

    if not check_if_in_list_of_dict(current_user['organizations'], inventory.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    users_inventories_query = db.query(
        user_inventory_model.UserInventory
    ).join(
        user_model.User, user_model.User.id == user_inventory_model.UserInventory.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_inventory_model.UserInventory.user_id.in_(payload.users_id),
        user_inventory_model.UserInventory.inventory_id == payload.inventory_id
    )
    users_inventories = users_inventories_query.all()

    if set(payload.users_id) == set(get_users_ids_list_from_response(users_inventories)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign users to inventory! Assign already exists!")

    for user_id in payload.users_id:
        if not check_if_users_ids_in_list_of_response(users_inventories, user_id):
            user_inventory_payload = dict(
                user_id=user_id,
                inventory_id=payload.inventory_id
            )
            new_user_inventory = user_inventory_model.UserInventory(
                **user_inventory_payload)

            db.add(new_user_inventory)
            db.commit()
            db.refresh(new_user_inventory)

            if not new_user_inventory:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign users to inventory! Something went wrong")

    return new_user_inventory


@router.get("/{id}/users", response_model=List[user_inventory_schema.UsersInventoryResponse])
async def get_users_inventory(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_inventory_query = db.query(
        user_inventory_model.UserInventory
    ).join(
        user_model.User, user_model.User.id == user_inventory_model.UserInventory.user_id
    ).join(
        inventory_model.Inventory, inventory_model.Inventory.id == user_inventory_model.UserInventory.inventory_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_inventory_model.UserInventory.inventory_id == id
    )

    if skip:
        users_inventory_query = users_inventory_query.offset(skip)

    if limit:
        users_inventory_query = users_inventory_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_inventory_query = users_inventory_query.order_by(desc(sort))
        else:
            users_inventory_query = users_inventory_query.order_by(sort)
    else:
        users_inventory_query = users_inventory_query.order_by(
            user_inventory_model.UserInventory.user_inventory_id)

    if limit == 1:
        users_inventory = users_inventory_query.first()
    else:
        users_inventory = users_inventory_query.all()

    if not users_inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_inventory


@router.get("/{id}/inventories", response_model=List[inventory_schema.InventoryResponse])
async def get_user_inventories(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_inventories: list = []

    user_inventories_query = db.query(
        user_inventory_model.UserInventory
    ).join(
        user_model.User, user_model.User.id == user_inventory_model.UserInventory.user_id
    ).join(
        inventory_model.Inventory, inventory_model.Inventory.id == user_inventory_model.UserInventory.inventory_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_inventory_model.UserInventory.user_id == id
    )

    if skip:
        user_inventories_query = user_inventories_query.offset(skip)

    if limit:
        user_inventories_query = user_inventories_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            user_inventories_query = user_inventories_query.order_by(
                desc(sort))
        else:
            user_inventories_query = user_inventories_query.order_by(sort)
    else:
        user_inventories_query = user_inventories_query.order_by(
            user_inventory_model.UserInventory.user_inventory_id)

    if limit == 1:
        user_inventories = user_inventories_query.first()
    else:
        user_inventories = user_inventories_query.all()

    if not user_inventories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")
    else:
        for user_inventory in user_inventories:
            my_inventories.append(user_inventory.inventory)

    return my_inventories


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_inventories(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    users_inventories_query = db.query(
        user_inventory_model.UserInventory
    ).filter(
        user_inventory_model.UserInventory.user_inventory_id.in_(selected)
    )
    users_inventories = users_inventories_query.all()

    if not users_inventories or len(users_inventories) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for user_inventory in users_inventories:
        if not check_if_in_list_of_dict(current_user['organizations'], user_inventory.inventory.organization.id) or user_inventory.user.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    users_inventories_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
