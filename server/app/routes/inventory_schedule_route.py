from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy import desc
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List, Optional
from ..models import inventory_schedule_model, inventory_model, organization_model, schedule_model
from ..schemas import common_schema, user_schema, inventory_schedule_schema
from ..database.connection import get_db
from app.services.tower.schedule_service import add_crontab_schedule_inventory, check_job_id, get_job_schedule_info, remove_job_schedules
from app.utils.check_value_exists import check_if_schedules_ids_in_list_of_response, check_if_in_list_of_dict
from app.utils.get_ids import get_schedules_ids_list_from_response, get_ids_list
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/inventories-schedules",
    tags=['Inventories | Schedules assigns']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/login')


@router.get("", response_model=List[inventory_schedule_schema.InventoryScheduleResponse])
async def get_inventories_schedules(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    inventories_schedules_query = db.query(
        inventory_schedule_model.InventorySchedule
    ).join(
        schedule_model.Schedule, schedule_model.Schedule.id == inventory_schedule_model.InventorySchedule.schedule_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        schedule_model.Schedule.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        inventories_schedules_query = inventories_schedules_query.offset(skip)

    if limit:
        inventories_schedules_query = inventories_schedules_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            inventories_schedules_query = inventories_schedules_query.order_by(
                desc(sort))
        else:
            inventories_schedules_query = inventories_schedules_query.order_by(
                sort)
    else:
        inventories_schedules_query = inventories_schedules_query.order_by(
            inventory_schedule_model.InventorySchedule.inventory_schedule_id)

    if limit == 1:
        inventories_schedules = inventories_schedules_query.first()
    else:
        inventories_schedules = inventories_schedules_query.all()

    if not inventories_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return inventories_schedules


@router.post("", status_code=status.HTTP_201_CREATED, response_model=List[inventory_schedule_schema.InventorySchedulesResponse])
async def create_inventories_schedules(
    payload: inventory_schedule_schema.InventorySchedulePostRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.schedules_id or not payload.inventory_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign schedules to inventory! Provide a valid request")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not get credential token", headers={"WWW-Authenticate": "Bearer"})

    response: list = []

    schedules_query = db.query(
        schedule_model.Schedule
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        schedule_model.Schedule.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        schedule_model.Schedule.id.in_(payload.schedules_id)
    )
    schedules = schedules_query.all()
    if not schedules or len(schedules) != len(payload.schedules_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign schedules to inventory! Provide a valid schedules")

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
                            detail="Can't assign schedules to inventory! Provide a valid inventory")

    if not check_if_in_list_of_dict(current_user['organizations'], inventory.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    inventories_schedules_query = db.query(
        inventory_schedule_model.InventorySchedule
    ).join(
        schedule_model.Schedule, schedule_model.Schedule.id == inventory_schedule_model.InventorySchedule.schedule_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_schedule_model.InventorySchedule.schedule_id.in_(
            payload.schedules_id),
        inventory_schedule_model.InventorySchedule.inventory_id == payload.inventory_id
    )
    inventories_schedules = inventories_schedules_query.all()

    if set(payload.schedules_id) == set(get_schedules_ids_list_from_response(inventories_schedules)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign schedules to inventory! Assign already exists!")

    for schedule in schedules:
        if not check_if_schedules_ids_in_list_of_response(inventories_schedules, schedule.id):
            cron_job_id: str = str(uuid4())
            while check_job_id(cron_job_id):
                cron_job_id = str(uuid4())

            added_schedule = add_crontab_schedule_inventory(
                token,
                schedule.start_date_time,
                schedule.repeat_frequency,
                schedule.every if schedule.every else None,
                schedule.week_days if schedule.week_days else None,
                cron_job_id,
                inventory.id
            )
            if not added_schedule:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't add schedule to service! Something went wrong")

            inventory_schedule_payload = dict(
                schedule_id=schedule.id,
                inventory_id=payload.inventory_id,
                cron_job_id=cron_job_id
            )
            new_inventory_schedule = inventory_schedule_model.InventorySchedule(
                **inventory_schedule_payload)

            db.add(new_inventory_schedule)
            db.commit()
            db.refresh(new_inventory_schedule)

            if not new_inventory_schedule:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign schedules to inventory! Something went wrong")

            response.append(new_inventory_schedule)

    return response


@router.get("/{id}/inventories", response_model=List[inventory_schedule_schema.InventoriesScheduleResponse])
async def get_inventories_schedule(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    inventories_schedule_query = db.query(
        inventory_schedule_model.InventorySchedule
    ).join(
        schedule_model.Schedule, schedule_model.Schedule.id == inventory_schedule_model.InventorySchedule.schedule_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        schedule_model.Schedule.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        inventory_schedule_model.InventorySchedule.schedule_id == id
    )

    if skip:
        inventories_schedule_query = inventories_schedule_query.offset(skip)

    if limit:
        inventories_schedule_query = inventories_schedule_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            inventories_schedule_query = inventories_schedule_query.order_by(
                desc(sort))
        else:
            inventories_schedule_query = inventories_schedule_query.order_by(
                sort)
    else:
        inventories_schedule_query = inventories_schedule_query.order_by(
            inventory_schedule_model.InventorySchedule.inventory_schedule_id)

    if limit == 1:
        inventories_schedule = inventories_schedule_query.first()
    else:
        inventories_schedule = inventories_schedule_query.all()

    if not inventories_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return inventories_schedule


@router.get("/{id}/schedules", response_model=List[inventory_schedule_schema.InventorySchedulesResponse])
async def get_inventory_schedules(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    inventory_schedules_query = db.query(
        inventory_schedule_model.InventorySchedule
    ).join(
        inventory_model.Inventory, inventory_model.Inventory.id == inventory_schedule_model.InventorySchedule.inventory_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        inventory_schedule_model.InventorySchedule.inventory_id == id
    )

    if skip:
        inventory_schedules_query = inventory_schedules_query.offset(skip)

    if limit:
        inventory_schedules_query = inventory_schedules_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            inventory_schedules_query = inventory_schedules_query.order_by(
                desc(sort))
        else:
            inventory_schedules_query = inventory_schedules_query.order_by(
                sort)
    else:
        inventory_schedules_query = inventory_schedules_query.order_by(
            inventory_schedule_model.InventorySchedule.inventory_schedule_id)

    if limit == 1:
        inventory_schedules = inventory_schedules_query.first()
    else:
        inventory_schedules = inventory_schedules_query.all()

    if not inventory_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return inventory_schedules


@router.get("/{id}/schedules/info", response_model=List[common_schema.JobsScheduleInfoBase])
async def get_inventory_schedules_info(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    inventory_schedules_query = db.query(
        inventory_schedule_model.InventorySchedule
    ).join(
        inventory_model.Inventory, inventory_model.Inventory.id == inventory_schedule_model.InventorySchedule.inventory_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        inventory_schedule_model.InventorySchedule.inventory_id == id
    )
    inventory_schedules = inventory_schedules_query.all()

    if not inventory_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any information")

    schedule_info = get_job_schedule_info(inventory_schedules)

    if not schedule_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any information")

    return schedule_info


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventories_schedules(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    inventories_schedules_query = db.query(
        inventory_schedule_model.InventorySchedule
    ).filter(
        inventory_schedule_model.InventorySchedule.inventory_schedule_id.in_(
            selected)
    )
    inventories_schedules = inventories_schedules_query.all()

    if not inventories_schedules or len(inventories_schedules) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for inventory_schedule in inventories_schedules:
        if not check_if_in_list_of_dict(current_user['organizations'], inventory_schedule.inventory.organization.id) or inventory_schedule.inventory.organization.tower_id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    schedules_deleted = remove_job_schedules(inventories_schedules)
    if not schedules_deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't delete schedule in service! Something went wrong")

    inventories_schedules_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
