from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models import schedule_model, organization_model, template_schedule_model, project_schedule_model, inventory_schedule_model
from ..schemas import schedule_schema, user_schema, common_schema
from ..database.connection import get_db
from app.services.tower.schedule_service import update_job_schedule
from app.utils.get_ids import get_ids_list
from app.utils.check_value_exists import check_if_in_list_of_dict
from ..auth import oauth2

router = APIRouter(
    prefix="/api/schedules",
    tags=['Schedules']
)


@router.get("", response_model=List[schedule_schema.ScheduleResponse])
async def get_schedules(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    schedules_query = db.query(
        schedule_model.Schedule
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        schedule_model.Schedule.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if search_by_name:
        schedules_query = schedules_query.filter(
            schedule_model.Schedule.name.contains(search_by_name)
        )

    if skip:
        schedules_query = schedules_query.offset(skip)

    if limit:
        schedules_query = schedules_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            schedules_query = schedules_query.order_by(desc(sort))
        else:
            schedules_query = schedules_query.order_by(sort)
    else:
        schedules_query = schedules_query.order_by(schedule_model.Schedule.id)

    if limit == 1:
        schedules = schedules_query.first()
    else:
        schedules = schedules_query.all()

    if not schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any schedules")

    return schedules


@router.get("/owner", response_model=List[schedule_schema.ScheduleResponse])
async def get_my_schedules(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_schedules_query = db.query(
        schedule_model.Schedule
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        schedule_model.Schedule.created_by == current_user['user'].username
    ).distinct(
        schedule_model.Schedule.id
    )

    if search_by_name:
        my_schedules_query = my_schedules_query.filter(
            schedule_model.Schedule.name.contains(search_by_name)
        )

    if skip:
        my_schedules_query = my_schedules_query.offset(skip)

    if limit:
        my_schedules_query = my_schedules_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            my_schedules_query = my_schedules_query.order_by(desc(sort))
        else:
            my_schedules_query = my_schedules_query.order_by(sort)
    else:
        my_schedules_query = my_schedules_query.order_by(
            schedule_model.Schedule.id)

    if limit == 1:
        my_schedules = my_schedules_query.first()
    else:
        my_schedules = my_schedules_query.all()

    if not my_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any schedules")

    return my_schedules


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schedule_schema.ScheduleResponse)
async def create_schedule(
    payload: schedule_schema.ScheduleRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.name or not payload.schedule_type or not payload.start_date_time or not payload.repeat_frequency or not payload.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't create schedule! Provide a valid request")

    if payload.week_days:
        for week_day in payload.week_days:
            if week_day not in range(0, 7):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Can't create schedule! Provide a valid time")

    if payload.start_date_time.minute not in range(0, 60) or payload.start_date_time.hour not in range(0, 24) or payload.start_date_time.day not in range(1, 32) or payload.start_date_time.month not in range(1, 13):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't create schedule! Provide a valid time")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot create a schedule! Provide a valid Organization")

    if not check_if_in_list_of_dict(current_user['organizations'], payload.organization_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    schedule_query = db.query(
        schedule_model.Schedule
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        schedule_model.Schedule.organization_id == payload.organization_id,
        schedule_model.Schedule.name == payload.name
    )
    schedule = schedule_query.first()
    if schedule:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create schedule! Schedule already exists")

    updated_payload = dict(
        **payload.dict(),
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    new_schedule = schedule_model.Schedule(**updated_payload)

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    if not new_schedule:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create schedule! Something went wrong")

    return new_schedule


@router.get("/{id}", response_model=schedule_schema.ScheduleResponse)
async def get_schedule(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    schedule_query = db.query(
        schedule_model.Schedule
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        schedule_model.Schedule.id == id
    )
    schedule = schedule_query.first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")

    if not check_if_in_list_of_dict(current_user['organizations'], schedule.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return schedule


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    schedules_query = db.query(
        schedule_model.Schedule
    ).filter(
        schedule_model.Schedule.id.in_(selected)
    )
    schedules = schedules_query.all()

    if not schedules or len(schedules) != len(selected):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")

    for schedule in schedules:
        if not check_if_in_list_of_dict(current_user['organizations'], schedule.organization.id) or schedule.organization.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    schedules_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schedule_schema.ScheduleResponse)
async def update_schedule(
    id: int,
    payload: schedule_schema.ScheduleUpdateRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.name or not payload.start_date_time or not payload.repeat_frequency or not payload.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't update schedule! Provide a valid request")

    if payload.week_days:
        for week_day in payload.week_days:
            if week_day not in range(0, 7):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Can't update schedule! Provide a valid time")

    if payload.start_date_time.minute not in range(0, 60) or payload.start_date_time.hour not in range(0, 24) or payload.start_date_time.day not in range(1, 32) or payload.start_date_time.month not in range(1, 13):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't update schedule! Provide a valid time")

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
                            detail="Can't update a schedule! Provide a valid Organization")

    schedule_query = db.query(
        schedule_model.Schedule
    ).filter(
        schedule_model.Schedule.id == id
    )
    schedule = schedule_query.first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="schedule not found")

    if not check_if_in_list_of_dict(current_user['organizations'], schedule.organization.id) or schedule.organization.tower.id != current_user["user"].tower.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if payload.name != schedule.name:
        new_schedule_query = db.query(
            schedule_model.Schedule
        ).join(
            organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
        ).filter(
            organization_model.Organization.tower_id == current_user["user"].tower.id,
            schedule_model.Schedule.organization_id == payload.organization_id,
            schedule_model.Schedule.name == payload.name
        )
        new_schedule = new_schedule_query.first()
        if new_schedule:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update schedule! Schedule already exists")

    if schedule.schedule_type == schedule_schema.ScheduleType.inventory:
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
        inventories_schedule = inventories_schedule_query.all()

        if inventories_schedule:
            for inventory_schedule in inventories_schedule:
                schedules_updated = update_job_schedule(
                    inventory_schedule.cron_job_id,
                    payload.start_date_time,
                    payload.repeat_frequency,
                    payload.every if payload.every else None,
                    payload.week_days if payload.week_days else None
                )
                if not schedules_updated:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail="Can't update schedule in service! Something went wrong")

    if schedule.schedule_type == schedule_schema.ScheduleType.project:
        projects_schedule_query = db.query(
            project_schedule_model.ProjectSchedule
        ).join(
            schedule_model.Schedule, schedule_model.Schedule.id == project_schedule_model.ProjectSchedule.schedule_id
        ).join(
            organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
        ).filter(
            organization_model.Organization.tower_id == current_user["user"].tower.id,
            schedule_model.Schedule.organization_id.in_(
                get_ids_list(current_user['organizations'])),
            project_schedule_model.ProjectSchedule.schedule_id == id
        )
        projects_schedule = projects_schedule_query.all()

        if projects_schedule:
            for project_schedule in projects_schedule:
                schedules_updated = update_job_schedule(
                    project_schedule.cron_job_id,
                    payload.start_date_time,
                    payload.repeat_frequency,
                    payload.every if payload.every else None,
                    payload.week_days if payload.week_days else None
                )
                if not schedules_updated:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail="Can't update schedule in service! Something went wrong")

    if schedule.schedule_type == schedule_schema.ScheduleType.template:
        templates_schedule_query = db.query(
            template_schedule_model.TemplateSchedule
        ).join(
            schedule_model.Schedule, schedule_model.Schedule.id == template_schedule_model.TemplateSchedule.schedule_id
        ).join(
            organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
        ).filter(
            organization_model.Organization.tower_id == current_user["user"].tower.id,
            schedule_model.Schedule.organization_id.in_(
                get_ids_list(current_user['organizations'])),
            template_schedule_model.TemplateSchedule.schedule_id == id
        )
        templates_schedule = templates_schedule_query.all()

        if templates_schedule:
            for template_schedule in templates_schedule:
                schedules_updated = update_job_schedule(
                    template_schedule.cron_job_id,
                    payload.start_date_time,
                    payload.repeat_frequency,
                    payload.every if payload.every else None,
                    payload.week_days if payload.week_days else None
                )
                if not schedules_updated:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail="Can't update schedule in service! Something went wrong")

    updated_payload = dict(
        **payload.dict(),
        last_modified_by=current_user["user"].username
    )

    schedule_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_schedule = schedule_query.first()

    return updated_schedule
