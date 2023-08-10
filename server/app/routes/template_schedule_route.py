from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy import desc
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List, Optional
from ..models import template_schedule_model, template_model, organization_model, schedule_model
from ..schemas import common_schema, user_schema, template_schedule_schema
from ..database.connection import get_db
from app.services.tower.schedule_service import add_crontab_schedule_template, check_job_id, get_job_schedule_info, remove_job_schedules
from app.utils.check_value_exists import check_if_schedules_ids_in_list_of_response, check_if_in_list_of_dict
from app.utils.get_ids import get_schedules_ids_list_from_response, get_ids_list
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/templates-schedules",
    tags=['Templates | Schedules assigns']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/login')


@router.get("", response_model=List[template_schedule_schema.TemplateScheduleResponse])
async def get_templates_schedules(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    templates_schedules_query = db.query(
        template_schedule_model.TemplateSchedule
    ).join(
        schedule_model.Schedule, schedule_model.Schedule.id == template_schedule_model.TemplateSchedule.schedule_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        schedule_model.Schedule.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        templates_schedules_query = templates_schedules_query.offset(skip)

    if limit:
        templates_schedules_query = templates_schedules_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            templates_schedules_query = templates_schedules_query.order_by(
                desc(sort))
        else:
            templates_schedules_query = templates_schedules_query.order_by(
                sort)
    else:
        templates_schedules_query = templates_schedules_query.order_by(
            template_schedule_model.TemplateSchedule.template_schedule_id)

    if limit == 1:
        templates_schedules = templates_schedules_query.first()
    else:
        templates_schedules = templates_schedules_query.all()

    if not templates_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return templates_schedules


@router.post("", status_code=status.HTTP_201_CREATED, response_model=List[template_schedule_schema.TemplateSchedulesResponse])
async def create_templates_schedules(
    payload: template_schedule_schema.TemplateSchedulePostRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.schedules_id or not payload.template_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign schedules to template! Provide a valid request")

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
                            detail="Can't assign schedules to template! Provide a valid schedules")

    template_query = db.query(
        template_model.Template
    ).join(
        organization_model.Organization, organization_model.Organization.id == template_model.Template.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        template_model.Template.id == payload.template_id
    )
    template = template_query.first()
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign schedules to template! Provide a valid template")

    if not check_if_in_list_of_dict(current_user['organizations'], template.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    templates_schedules_query = db.query(
        template_schedule_model.TemplateSchedule
    ).join(
        schedule_model.Schedule, schedule_model.Schedule.id == template_schedule_model.TemplateSchedule.schedule_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        template_schedule_model.TemplateSchedule.schedule_id.in_(
            payload.schedules_id),
        template_schedule_model.TemplateSchedule.template_id == payload.template_id
    )
    templates_schedules = templates_schedules_query.all()

    if set(payload.schedules_id) == set(get_schedules_ids_list_from_response(templates_schedules)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign schedules to template! Assign already exists!")

    for schedule in schedules:
        if not check_if_schedules_ids_in_list_of_response(templates_schedules, schedule.id):
            cron_job_id: str = str(uuid4())
            while check_job_id(cron_job_id):
                cron_job_id = str(uuid4())

            added_schedule = add_crontab_schedule_template(
                token,
                schedule.start_date_time,
                schedule.repeat_frequency,
                schedule.every if schedule.every else None,
                schedule.week_days if schedule.week_days else None,
                cron_job_id,
                template.id,
                template.organization.id
            )
            if not added_schedule:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't add schedule to service! Something went wrong")

            template_schedule_payload = dict(
                schedule_id=schedule.id,
                template_id=payload.template_id,
                cron_job_id=cron_job_id
            )
            new_template_schedule = template_schedule_model.TemplateSchedule(
                **template_schedule_payload)

            db.add(new_template_schedule)
            db.commit()
            db.refresh(new_template_schedule)

            if not new_template_schedule:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign schedules to template! Something went wrong")

            response.append(new_template_schedule)

    return response


@router.get("/{id}/templates", response_model=List[template_schedule_schema.TemplatesScheduleResponse])
async def get_templates_schedule(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
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

    if skip:
        templates_schedule_query = templates_schedule_query.offset(skip)

    if limit:
        templates_schedule_query = templates_schedule_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            templates_schedule_query = templates_schedule_query.order_by(
                desc(sort))
        else:
            templates_schedule_query = templates_schedule_query.order_by(sort)
    else:
        templates_schedule_query = templates_schedule_query.order_by(
            template_schedule_model.TemplateSchedule.template_schedule_id)

    if limit == 1:
        templates_schedule = templates_schedule_query.first()
    else:
        templates_schedule = templates_schedule_query.all()

    if not templates_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return templates_schedule


@router.get("/{id}/schedules", response_model=List[template_schedule_schema.TemplateSchedulesResponse])
async def get_template_schedules(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    template_schedules_query = db.query(
        template_schedule_model.TemplateSchedule
    ).join(
        template_model.Template, template_model.Template.id == template_schedule_model.TemplateSchedule.template_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == template_model.Template.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        template_schedule_model.TemplateSchedule.template_id == id
    )

    if skip:
        template_schedules_query = template_schedules_query.offset(skip)

    if limit:
        template_schedules_query = template_schedules_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            template_schedules_query = template_schedules_query.order_by(
                desc(sort))
        else:
            template_schedules_query = template_schedules_query.order_by(sort)
    else:
        template_schedules_query = template_schedules_query.order_by(
            template_schedule_model.TemplateSchedule.template_schedule_id)

    if limit == 1:
        template_schedules = template_schedules_query.first()
    else:
        template_schedules = template_schedules_query.all()

    if not template_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return template_schedules


@router.get("/{id}/schedules/info", response_model=List[common_schema.JobsScheduleInfoBase])
async def get_template_schedules_info(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    template_schedules_query = db.query(
        template_schedule_model.TemplateSchedule
    ).join(
        template_model.Template, template_model.Template.id == template_schedule_model.TemplateSchedule.template_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == template_model.Template.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        template_schedule_model.TemplateSchedule.template_id == id
    )
    template_schedules = template_schedules_query.all()

    if not template_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any information")

    schedule_info = get_job_schedule_info(template_schedules)

    if not schedule_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any information")

    return schedule_info


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_templates_schedules(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    templates_schedules_query = db.query(
        template_schedule_model.TemplateSchedule
    ).filter(
        template_schedule_model.TemplateSchedule.template_schedule_id.in_(
            selected)
    )
    templates_schedules = templates_schedules_query.all()

    if not templates_schedules or len(templates_schedules) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for template_schedule in templates_schedules:
        if not check_if_in_list_of_dict(current_user['organizations'], template_schedule.template.organization.id) or template_schedule.template.organization.tower_id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    schedules_deleted = remove_job_schedules(templates_schedules)
    if not schedules_deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't delete schedule in service! Something went wrong")

    templates_schedules_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
