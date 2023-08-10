from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy import desc
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List, Optional
from ..models import project_schedule_model, project_model, organization_model, schedule_model
from ..schemas import common_schema, user_schema, project_schedule_schema
from ..database.connection import get_db
from app.services.tower.schedule_service import add_crontab_schedule_project, check_job_id, get_job_schedule_info, remove_job_schedules
from app.utils.check_value_exists import check_if_schedules_ids_in_list_of_response, check_if_in_list_of_dict
from app.utils.get_ids import get_schedules_ids_list_from_response, get_ids_list
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/projects-schedules",
    tags=['Projects | Schedules assigns']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/login')


@router.get("", response_model=List[project_schedule_schema.ProjectScheduleResponse])
async def get_projects_schedules(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    projects_schedules_query = db.query(
        project_schedule_model.ProjectSchedule
    ).join(
        schedule_model.Schedule, schedule_model.Schedule.id == project_schedule_model.ProjectSchedule.schedule_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        schedule_model.Schedule.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        projects_schedules_query = projects_schedules_query.offset(skip)

    if limit:
        projects_schedules_query = projects_schedules_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            projects_schedules_query = projects_schedules_query.order_by(
                desc(sort))
        else:
            projects_schedules_query = projects_schedules_query.order_by(sort)
    else:
        projects_schedules_query = projects_schedules_query.order_by(
            project_schedule_model.ProjectSchedule.project_schedule_id)

    if limit == 1:
        projects_schedules = projects_schedules_query.first()
    else:
        projects_schedules = projects_schedules_query.all()

    if not projects_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return projects_schedules


@router.post("", status_code=status.HTTP_201_CREATED, response_model=List[project_schedule_schema.ProjectSchedulesResponse])
async def create_projects_schedules(
    payload: project_schedule_schema.ProjectSchedulePostRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.schedules_id or not payload.project_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign schedules to project! Provide a valid request")

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
                            detail="Can't assign schedules to project! Provide a valid schedules")

    project_query = db.query(
        project_model.Project
    ).join(
        organization_model.Organization, organization_model.Organization.id == project_model.Project.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        project_model.Project.id == payload.project_id
    )
    project = project_query.first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign schedules to project! Provide a valid project")

    if not check_if_in_list_of_dict(current_user['organizations'], project.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    projects_schedules_query = db.query(
        project_schedule_model.ProjectSchedule
    ).join(
        schedule_model.Schedule, schedule_model.Schedule.id == project_schedule_model.ProjectSchedule.schedule_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        project_schedule_model.ProjectSchedule.schedule_id.in_(
            payload.schedules_id),
        project_schedule_model.ProjectSchedule.project_id == payload.project_id
    )
    projects_schedules = projects_schedules_query.all()

    if set(payload.schedules_id) == set(get_schedules_ids_list_from_response(projects_schedules)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign schedules to project! Assign already exists!")

    for schedule in schedules:
        if not check_if_schedules_ids_in_list_of_response(projects_schedules, schedule.id):
            cron_job_id: str = str(uuid4())
            while check_job_id(cron_job_id):
                cron_job_id = str(uuid4())

            added_schedule = add_crontab_schedule_project(
                token,
                schedule.start_date_time,
                schedule.repeat_frequency,
                schedule.every if schedule.every else None,
                schedule.week_days if schedule.week_days else None,
                cron_job_id,
                project.id
            )
            if not added_schedule:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't add schedule to service! Something went wrong")

            project_schedule_payload = dict(
                schedule_id=schedule.id,
                project_id=payload.project_id,
                cron_job_id=cron_job_id
            )
            new_project_schedule = project_schedule_model.ProjectSchedule(
                **project_schedule_payload)

            db.add(new_project_schedule)
            db.commit()
            db.refresh(new_project_schedule)

            if not new_project_schedule:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign schedules to project! Something went wrong")

            response.append(new_project_schedule)

    return response


@router.get("/{id}/projects", response_model=List[project_schedule_schema.ProjectsScheduleResponse])
async def get_projects_schedule(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
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

    if skip:
        projects_schedule_query = projects_schedule_query.offset(skip)

    if limit:
        projects_schedule_query = projects_schedule_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            projects_schedule_query = projects_schedule_query.order_by(
                desc(sort))
        else:
            projects_schedule_query = projects_schedule_query.order_by(sort)
    else:
        projects_schedule_query = projects_schedule_query.order_by(
            project_schedule_model.ProjectSchedule.project_schedule_id)

    if limit == 1:
        projects_schedule = projects_schedule_query.first()
    else:
        projects_schedule = projects_schedule_query.all()

    if not projects_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return projects_schedule


@router.get("/{id}/schedules", response_model=List[project_schedule_schema.ProjectSchedulesResponse])
async def get_project_schedules(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    project_schedules_query = db.query(
        project_schedule_model.ProjectSchedule
    ).join(
        project_model.Project, project_model.Project.id == project_schedule_model.ProjectSchedule.project_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == project_model.Project.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        project_schedule_model.ProjectSchedule.project_id == id
    )

    if skip:
        project_schedules_query = project_schedules_query.offset(skip)

    if limit:
        project_schedules_query = project_schedules_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            project_schedules_query = project_schedules_query.order_by(
                desc(sort))
        else:
            project_schedules_query = project_schedules_query.order_by(sort)
    else:
        project_schedules_query = project_schedules_query.order_by(
            project_schedule_model.ProjectSchedule.project_schedule_id)

    if limit == 1:
        project_schedules = project_schedules_query.first()
    else:
        project_schedules = project_schedules_query.all()

    if not project_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return project_schedules


@router.get("/{id}/schedules/info", response_model=List[common_schema.JobsScheduleInfoBase])
async def get_project_schedules_info(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    project_schedules_query = db.query(
        project_schedule_model.ProjectSchedule
    ).join(
        project_model.Project, project_model.Project.id == project_schedule_model.ProjectSchedule.project_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == project_model.Project.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        project_schedule_model.ProjectSchedule.project_id == id
    )
    project_schedules = project_schedules_query.all()

    if not project_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any information")

    schedule_info = get_job_schedule_info(project_schedules)

    if not schedule_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any information")

    return schedule_info


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_projects_schedules(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    projects_schedules_query = db.query(
        project_schedule_model.ProjectSchedule
    ).filter(
        project_schedule_model.ProjectSchedule.project_schedule_id.in_(
            selected)
    )
    projects_schedules = projects_schedules_query.all()

    if not projects_schedules or len(projects_schedules) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for project_schedule in projects_schedules:
        if not check_if_in_list_of_dict(current_user['organizations'], project_schedule.project.organization.id) or project_schedule.project.organization.tower_id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    schedules_deleted = remove_job_schedules(projects_schedules)
    if not schedules_deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't delete schedule in service! Something went wrong")

    projects_schedules_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
