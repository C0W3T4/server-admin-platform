from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import inventory_group_model, group_model, organization_model, inventory_model
from ..schemas import common_schema, user_schema, inventory_group_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_groups_ids_in_list_of_response, check_if_in_list_of_dict
from app.utils.get_ids import get_groups_ids_list_from_response, get_ids_list
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/inventories-groups",
    tags=['Inventories | Groups assigns']
)


@router.get("", response_model=List[inventory_group_schema.InventoryGroupResponse])
async def get_inventories_groups(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    inventories_groups_query = db.query(
        inventory_group_model.InventoryGroup
    ).join(
        group_model.Group, group_model.Group.id == inventory_group_model.InventoryGroup.group_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        inventories_groups_query = inventories_groups_query.offset(skip)

    if limit:
        inventories_groups_query = inventories_groups_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            inventories_groups_query = inventories_groups_query.order_by(
                desc(sort))
        else:
            inventories_groups_query = inventories_groups_query.order_by(sort)
    else:
        inventories_groups_query = inventories_groups_query.order_by(
            inventory_group_model.InventoryGroup.inventory_group_id)

    if limit == 1:
        inventories_groups = inventories_groups_query.first()
    else:
        inventories_groups = inventories_groups_query.all()

    if not inventories_groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return inventories_groups


@router.post("", status_code=status.HTTP_201_CREATED, response_model=inventory_group_schema.InventoryGroupResponse)
async def create_inventories_groups(
    payload: inventory_group_schema.InventoryGroupPostRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.groups_id or not payload.inventory_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign groups to inventory! Provide a valid request")

    groups_query = db.query(
        group_model.Group
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        group_model.Group.id.in_(payload.groups_id)
    )
    groups = groups_query.all()
    if not groups or len(groups) != len(payload.groups_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign groups to inventory! Provide a valid group")

    inventory_query = db.query(
        inventory_model.Inventory
    ).join(
        organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        inventory_model.Inventory.id == payload.inventory_id
    )
    inventory = inventory_query.first()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign groups to inventory! Provide a valid group")

    if not check_if_in_list_of_dict(current_user['organizations'], inventory.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    inventories_groups_query = db.query(
        inventory_group_model.InventoryGroup
    ).join(
        group_model.Group, group_model.Group.id == inventory_group_model.InventoryGroup.group_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        inventory_group_model.InventoryGroup.group_id.in_(payload.groups_id),
        inventory_group_model.InventoryGroup.inventory_id == payload.inventory_id
    )
    inventories_groups = inventories_groups_query.all()

    if set(payload.groups_id) == set(get_groups_ids_list_from_response(inventories_groups)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign groups to inventory! Assign already exists!")

    for group_id in payload.groups_id:
        if not check_if_groups_ids_in_list_of_response(inventories_groups, group_id):
            inventory_group_payload = dict(
                group_id=group_id,
                inventory_id=payload.inventory_id
            )
            new_inventory_group = inventory_group_model.InventoryGroup(
                **inventory_group_payload)

            db.add(new_inventory_group)
            db.commit()
            db.refresh(new_inventory_group)

            if not new_inventory_group:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign groups to inventory! Something went wrong")

    return new_inventory_group


@router.get("/{id}/inventories", response_model=List[inventory_group_schema.InventoriesGroupResponse])
async def get_inventories_group(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    inventories_group_query = db.query(
        inventory_group_model.InventoryGroup
    ).join(
        group_model.Group, group_model.Group.id == inventory_group_model.InventoryGroup.group_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        inventory_group_model.InventoryGroup.group_id == id
    )

    if skip:
        inventories_group_query = inventories_group_query.offset(skip)

    if limit:
        inventories_group_query = inventories_group_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            inventories_group_query = inventories_group_query.order_by(
                desc(sort))
        else:
            inventories_group_query = inventories_group_query.order_by(sort)
    else:
        inventories_group_query = inventories_group_query.order_by(
            inventory_group_model.InventoryGroup.inventory_group_id)

    if limit == 1:
        inventories_group = inventories_group_query.first()
    else:
        inventories_group = inventories_group_query.all()

    if not inventories_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return inventories_group


@router.get("/{id}/groups", response_model=List[inventory_group_schema.InventoryGroupsResponse])
async def get_inventory_groups(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    inventory_groups_query = db.query(
        inventory_group_model.InventoryGroup
    ).join(
        inventory_model.Inventory, inventory_model.Inventory.id == inventory_group_model.InventoryGroup.inventory_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        inventory_group_model.InventoryGroup.inventory_id == id
    )

    if skip:
        inventory_groups_query = inventory_groups_query.offset(skip)

    if limit:
        inventory_groups_query = inventory_groups_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            inventory_groups_query = inventory_groups_query.order_by(
                desc(sort))
        else:
            inventory_groups_query = inventory_groups_query.order_by(sort)
    else:
        inventory_groups_query = inventory_groups_query.order_by(
            inventory_group_model.InventoryGroup.inventory_group_id)

    if limit == 1:
        inventory_groups = inventory_groups_query.first()
    else:
        inventory_groups = inventory_groups_query.all()

    if not inventory_groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return inventory_groups


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventories_groups(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    inventories_groups_query = db.query(
        inventory_group_model.InventoryGroup
    ).filter(
        inventory_group_model.InventoryGroup.inventory_group_id.in_(selected)
    )
    inventories_groups = inventories_groups_query.all()

    if not inventories_groups or len(inventories_groups) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for inventory_group in inventories_groups:
        if not check_if_in_list_of_dict(current_user['organizations'], inventory_group.inventory.organization.id) or inventory_group.inventory.organization.tower_id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    inventories_groups_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
