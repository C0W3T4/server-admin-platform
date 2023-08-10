from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timezone
from ..models import job_model, template_model, organization_model, user_template_model, user_model
from ..schemas import job_schema, user_schema, common_schema, tower_schema
from ..database.connection import get_db
from app.utils.get_ids import get_ids_list, get_templates_ids_list_from_response
from app.utils.check_value_exists import check_if_in_list_of_dict
from ..services.tower.tower_service import launch_jobs
from ..auth import oauth2

router = APIRouter(
    prefix="/api/jobs",
    tags=['Jobs']
)


@router.get("", response_model=List[job_schema.JobResponse])
async def get_all_jobs(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    user_templates_query = db.query(
        user_template_model.UserTemplate
    ).join(
        user_model.User, user_model.User.id == user_template_model.UserTemplate.user_id
    ).join(
        template_model.Template, template_model.Template.id == user_template_model.UserTemplate.template_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_template_model.UserTemplate.user_id == current_user["user"].id
    )
    user_templates = user_templates_query.all()
    if not user_templates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    jobs_query = db.query(
        job_model.Job
    ).join(
        template_model.Template, template_model.Template.id == job_model.Job.template_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == job_model.Job.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        job_model.Job.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        job_model.Job.template_id.in_(
            get_templates_ids_list_from_response(user_templates))
    )

    if search_by_name:
        jobs_query = jobs_query.filter(
            template_model.Template.name.contains(search_by_name)
        )

    if skip:
        jobs_query = jobs_query.offset(skip)

    if limit:
        jobs_query = jobs_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            jobs_query = jobs_query.order_by(desc(sort))
        else:
            jobs_query = jobs_query.order_by(sort)
    else:
        jobs_query = jobs_query.order_by(job_model.Job.id)

    if limit == 1:
        jobs = jobs_query.first()
    else:
        jobs = jobs_query.all()

    if not jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find any jobs")

    return jobs


@router.get("/owner", response_model=List[job_schema.JobResponse])
async def get_my_jobs(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_jobs_query = db.query(
        job_model.Job
    ).join(
        template_model.Template, template_model.Template.id == job_model.Job.template_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == job_model.Job.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        job_model.Job.launched_by == current_user['user'].username
    ).distinct(
        job_model.Job.id
    )

    if search_by_name:
        my_jobs_query = my_jobs_query.filter(
            template_model.Template.name.contains(search_by_name)
        )

    if skip:
        my_jobs_query = my_jobs_query.offset(skip)

    if limit:
        my_jobs_query = my_jobs_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            my_jobs_query = my_jobs_query.order_by(desc(sort))
        else:
            my_jobs_query = my_jobs_query.order_by(sort)
    else:
        my_jobs_query = my_jobs_query.order_by(job_model.Job.id)

    if limit == 1:
        my_jobs = my_jobs_query.first()
    else:
        my_jobs = my_jobs_query.all()

    if not my_jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find any jobs")

    return my_jobs


@router.post("/launch", status_code=status.HTTP_201_CREATED, response_model=job_schema.JobResponse)
async def launch_new_job(
    payload: job_schema.JobRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    if not payload.template_id or not payload.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot create a job! Provide a valid request")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot create a job! Provide a valid Organization")

    if not check_if_in_list_of_dict(current_user['organizations'], payload.organization_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    template_query = db.query(
        template_model.Template
    ).join(
        organization_model.Organization, organization_model.Organization.id == template_model.Template.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        template_model.Template.id == payload.template_id
    )
    template = template_query.first()
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot create a job! Provide a valid Template")

    started_at = datetime.now(timezone.utc)

    result_output = launch_jobs(
        template.organization.name,
        template.project.source_control_url,
        template.playbook_name,
        template.inventory.inventory_file,
        template.privilege_escalation,
        template.forks,
        template.verbosity,
        template.launch_type,
        template.extra_vars,
        template.credential.username,
        template.credential.password,
        my_tower.company,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not result_output:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't launch job! Something went wrong")

    finished_at = datetime.now(timezone.utc)

    updated_payload = dict(
        **payload.dict(),
        started_at=started_at,
        finished_at=finished_at,
        output=result_output,
        job_status=job_schema.JobStatus.successful if result_output else job_schema.JobStatus.pending,
        launched_by=current_user["user"].username
    )

    new_job = job_model.Job(**updated_payload)

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    if not new_job:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create job! Something went wrong")

    return new_job


@router.get("/{id}", response_model=job_schema.JobResponse)
async def get_job(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    job_query = db.query(
        job_model.Job
    ).join(
        organization_model.Organization, organization_model.Organization.id == job_model.Job.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        job_model.Job.id == id
    )
    job = job_query.first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    if not check_if_in_list_of_dict(current_user['organizations'], job.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return job


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    jobs_query = db.query(
        job_model.Job
    ).filter(
        job_model.Job.id.in_(selected)
    )
    jobs = jobs_query.all()

    if not jobs or len(jobs) != len(selected):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    for job in jobs:
        if not check_if_in_list_of_dict(current_user['organizations'], job.organization.id) or job.organization.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    jobs_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}/launch", response_model=job_schema.JobResponse)
async def launch_job(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    job_query = db.query(
        job_model.Job
    ).filter(
        job_model.Job.id == id
    )
    job = job_query.first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    if not check_if_in_list_of_dict(current_user['organizations'], job.organization.id) or job.organization.tower.id != current_user["user"].tower.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    started_at = datetime.now(timezone.utc)

    result_output = launch_jobs(
        job.template.organization.name,
        job.template.project.source_control_url,
        job.template.playbook_name,
        job.template.inventory.inventory_file,
        job.template.privilege_escalation,
        job.template.forks,
        job.template.verbosity,
        job.template.launch_type,
        job.template.extra_vars,
        job.template.credential.username,
        job.template.credential.password,
        my_tower.company,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not result_output:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't launch job! Something went wrong")

    finished_at = datetime.now(timezone.utc)

    updated_payload = dict(
        template_id=job.template.id,
        organization_id=job.organization.id,
        started_at=started_at,
        finished_at=finished_at,
        output=result_output,
        job_status=job_schema.JobStatus.successful if result_output else job.job_status,
        launched_by=current_user["user"].username
    )

    job_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_job = job_query.first()

    return updated_job
