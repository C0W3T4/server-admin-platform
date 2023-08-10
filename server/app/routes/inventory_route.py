from fastapi import Request, Response, status, HTTPException, Depends, APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import inventory_model, organization_model, user_model, user_inventory_model, group_model, inventory_group_model, host_model, group_host_model
from ..schemas import inventory_schema, user_schema, common_schema, tower_schema
from app.utils.check_value_exists import check_if_in_list_of_dict
from app.utils.get_ids import get_groups_ids_list_from_response, get_hosts_by_group, get_ids_list
from app.services.tower.inventory_service import create_inventory_file, delete_inventory_file, update_inventory_file, write_inventory_file
from ..database.connection import get_db
from ..auth import oauth2

router = APIRouter(
    prefix="/api/inventories",
    tags=['Inventories']
)

templates = Jinja2Templates(directory="app/templates")


@router.get("", response_model=List[inventory_schema.InventoryResponse])
async def get_inventories(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    inventories_query = db.query(
        inventory_model.Inventory
    ).join(
        organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if search_by_name:
        inventories_query = inventories_query.filter(
            inventory_model.Inventory.name.contains(search_by_name)
        )

    if skip:
        inventories_query = inventories_query.offset(skip)

    if limit:
        inventories_query = inventories_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            inventories_query = inventories_query.order_by(desc(sort))
        else:
            inventories_query = inventories_query.order_by(sort)
    else:
        inventories_query = inventories_query.order_by(
            inventory_model.Inventory.id)

    if limit == 1:
        inventories = inventories_query.first()
    else:
        inventories = inventories_query.all()

    if not inventories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any inventories")

    return inventories


@router.get("/owner", response_model=List[inventory_schema.InventoryResponse])
async def get_my_inventories(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_inventories_query = db.query(
        inventory_model.Inventory
    ).join(
        organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.created_by == current_user['user'].username
    ).distinct(
        inventory_model.Inventory.id
    )

    if search_by_name:
        my_inventories_query = my_inventories_query.filter(
            inventory_model.Inventory.name.contains(search_by_name)
        )

    if skip:
        my_inventories_query = my_inventories_query.offset(skip)

    if limit:
        my_inventories_query = my_inventories_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            my_inventories_query = my_inventories_query.order_by(desc(sort))
        else:
            my_inventories_query = my_inventories_query.order_by(sort)
    else:
        my_inventories_query = my_inventories_query.order_by(
            inventory_model.Inventory.id)

    if limit == 1:
        my_inventories = my_inventories_query.first()
    else:
        my_inventories = my_inventories_query.all()

    if not my_inventories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any inventories")

    return my_inventories


@router.post("", status_code=status.HTTP_201_CREATED, response_model=inventory_schema.InventoryResponse)
async def create_inventories(
    payload: inventory_schema.InventoryRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    if not payload.name or not payload.inventory_file or not payload.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create inventory")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't create inventory! Provide a valid Organization")

    if not check_if_in_list_of_dict(current_user['organizations'], payload.organization_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    inventory_query = db.query(
        inventory_model.Inventory
    ).join(
        organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id == payload.organization_id
    ).filter(
        or_(
            inventory_model.Inventory.name == payload.name,
            inventory_model.Inventory.inventory_file == payload.inventory_file
        )
    )
    inventory = inventory_query.first()
    if inventory:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create inventory! Inventory already exists!")

    updated_payload = dict(
        **payload.dict(),
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    new_inventory = inventory_model.Inventory(**updated_payload)

    created_inventory_file = create_inventory_file(
        organization.name,
        payload.inventory_file,
        my_tower.company,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        20
    )
    if not created_inventory_file:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create inventory file! Something went wrong")

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    if not new_inventory:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create inventory! Something went wrong")
    else:
        if current_user["user"].user_type != user_schema.UserType.admin:
            user_query = db.query(
                user_model.User
            ).filter(
                user_model.User.tower_id == current_user["user"].tower.id,
                user_model.User.user_type == user_schema.UserType.admin
            )
            user = user_query.first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Can't assign user to inventory! Provide a valid user")

            admin_inventory_payload = dict(
                user_id=user.id,
                inventory_id=new_inventory.id
            )
            new_admin_inventory = user_inventory_model.UserInventory(
                **admin_inventory_payload)

            db.add(new_admin_inventory)
            db.commit()
            db.refresh(new_admin_inventory)

            if not new_admin_inventory:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign user to inventory! Something went wrong")

        user_inventory_payload = dict(
            user_id=current_user["user"].id,
            inventory_id=new_inventory.id
        )
        new_user_inventory = user_inventory_model.UserInventory(
            **user_inventory_payload)

        db.add(new_user_inventory)
        db.commit()
        db.refresh(new_user_inventory)

        if not new_user_inventory:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't assign user to inventory! Something went wrong")

    return new_inventory


@router.get("/{id}", response_model=inventory_schema.InventoryResponse)
async def get_inventory(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    inventory_query = db.query(
        inventory_model.Inventory
    ).join(
        organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.id == id
    )
    inventory = inventory_query.first()
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")

    if not check_if_in_list_of_dict(current_user['organizations'], inventory.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return inventory


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    inventories_query = db.query(
        inventory_model.Inventory
    ).filter(
        inventory_model.Inventory.id.in_(selected)
    )
    inventories = inventories_query.all()

    if not inventories or len(inventories) != len(selected):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")

    for inventory in inventories:
        if not check_if_in_list_of_dict(current_user['organizations'], inventory.organization.id) or inventory.organization.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    deleted_inventory_file = delete_inventory_file(
        inventories,
        my_tower.company,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not deleted_inventory_file:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't delete inventory file! Something went wrong")

    inventories_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=inventory_schema.InventoryResponse)
async def update_inventory(
    id: int,
    payload: inventory_schema.InventoryRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    if not payload.name or not payload.inventory_file or not payload.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create inventory")

    if not check_if_in_list_of_dict(current_user['organizations'], payload.organization_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't update inventory file! Provide a valid organization")

    inventory_query = db.query(
        inventory_model.Inventory
    ).filter(
        inventory_model.Inventory.id == id
    )
    inventory = inventory_query.first()
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")

    if not check_if_in_list_of_dict(current_user['organizations'], inventory.organization.id) or inventory.organization.tower.id != current_user["user"].tower.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if payload.name != inventory.name or payload.inventory_file != inventory.inventory_file:
        new_inventory_query = db.query(
            inventory_model.Inventory
        ).join(
            organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
        ).filter(
            organization_model.Organization.tower_id == current_user["user"].tower.id,
            inventory_model.Inventory.organization_id == payload.organization_id
        )
        if payload.name == inventory.name:
            new_inventory_query = new_inventory_query.filter(
                inventory_model.Inventory.inventory_file == payload.inventory_file
            )
        elif payload.inventory_file == inventory.inventory_file:
            new_inventory_query = new_inventory_query.filter(
                inventory_model.Inventory.name == payload.name
            )
        new_inventory = new_inventory_query.first()
        if new_inventory:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update inventory! Inventory already exists!")

    updated_payload = dict(
        **payload.dict(),
        last_modified_by=current_user["user"].username
    )

    if payload.organization_id != inventory.organization.id or payload.inventory_file != inventory.inventory_file:
        updated_inventory_file = update_inventory_file(
            organization.name,
            inventory.organization.name,
            inventory.inventory_file,
            updated_payload['inventory_file'],
            my_tower.company,
            my_tower.ipv4,
            my_tower.port,
            my_tower.username,
            my_tower.password,
            10
        )
        if not updated_inventory_file:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't update inventory file! Something went wrong")

    inventory_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_inventory = inventory_query.first()

    return updated_inventory


@router.put("/{id}/sync", response_model=inventory_schema.InventoryResponse)
async def sync_inventory(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    inventory_query = db.query(
        inventory_model.Inventory
    ).filter(
        inventory_model.Inventory.id == id
    )
    inventory = inventory_query.first()
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")

    if not check_if_in_list_of_dict(current_user['organizations'], inventory.organization.id) or inventory.organization.tower.id != current_user["user"].tower.id:
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
        inventory_group_model.InventoryGroup.inventory_id == id
    )
    inventories_groups = inventories_groups_query.all()

    groups_hosts_query = db.query(
        group_host_model.GroupHost
    ).join(
        host_model.Host, host_model.Host.id == group_host_model.GroupHost.host_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        group_host_model.GroupHost.group_id.in_(
            get_groups_ids_list_from_response(inventories_groups))
    )
    groups_hosts = groups_hosts_query.all()

    hosts_by_group = get_hosts_by_group(groups_hosts)

    template = templates.TemplateResponse(
        'inventory', context={"request": request, "hosts_by_group": hosts_by_group})

    write_file = write_inventory_file(
        inventory.organization.name,
        inventory.inventory_file,
        template.body.decode("utf-8"),
        my_tower.company,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not write_file:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't sync inventory! Something went wrong")

    updated_payload = dict(
        name=inventory.name,
        inventory_file=inventory.inventory_file,
        inventory_status=write_file if write_file else inventory.inventory_status,
        organization_id=inventory.organization_id,
        last_modified_by=current_user["user"].username
    )

    inventory_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_inventory = inventory_query.first()

    return updated_inventory
