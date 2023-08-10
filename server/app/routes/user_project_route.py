from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import user_project_model, user_model, project_model, organization_model
from ..schemas import common_schema, user_schema, user_project_schema, project_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/users-projects",
    tags=['Users | Projects assigns']
)


@router.get("", response_model=List[user_project_schema.UserProjectResponse])
async def get_users_projects(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_projects_query = db.query(
        user_project_model.UserProject
    ).join(
        user_model.User, user_model.User.id == user_project_model.UserProject.user_id
    ).join(
        project_model.Project, project_model.Project.id == user_project_model.UserProject.project_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        users_projects_query = users_projects_query.offset(skip)

    if limit:
        users_projects_query = users_projects_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_projects_query = users_projects_query.order_by(desc(sort))
        else:
            users_projects_query = users_projects_query.order_by(sort)
    else:
        users_projects_query = users_projects_query.order_by(
            user_project_model.UserProject.user_project_id)

    if limit == 1:
        users_projects = users_projects_query.first()
    else:
        users_projects = users_projects_query.all()

    if not users_projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_projects


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_project_schema.UserProjectResponse)
async def create_users_projects(
    payload: user_project_schema.UserProjectPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.users_id or not payload.project_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign users to project! Provide a valid request")

    users_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id.in_(payload.users_id)
    )
    users = users_query.all()
    if not users or len(users) != len(payload.users_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to project! Provide a valid user")

    project_query = db.query(
        project_model.Project
    ).join(
        organization_model.Organization, organization_model.Organization.id == project_model.Project.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        project_model.Project.id == payload.project_id
    )
    project = project_query.first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to project! Provide a valid project")

    if not check_if_in_list_of_dict(current_user['organizations'], project.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    users_projects_query = db.query(
        user_project_model.UserProject
    ).join(
        user_model.User, user_model.User.id == user_project_model.UserProject.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_project_model.UserProject.user_id.in_(payload.users_id),
        user_project_model.UserProject.project_id == payload.project_id
    )
    users_projects = users_projects_query.all()

    if set(payload.users_id) == set(get_users_ids_list_from_response(users_projects)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign users to project! Assign already exists!")

    for user_id in payload.users_id:
        if not check_if_users_ids_in_list_of_response(users_projects, user_id):
            user_project_payload = dict(
                user_id=user_id,
                project_id=payload.project_id
            )
            new_user_project = user_project_model.UserProject(
                **user_project_payload)

            db.add(new_user_project)
            db.commit()
            db.refresh(new_user_project)

            if not new_user_project:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign users to project! Something went wrong")

    return new_user_project


@router.get("/{id}/users", response_model=List[user_project_schema.UsersProjectResponse])
async def get_users_project(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_project_query = db.query(
        user_project_model.UserProject
    ).join(
        user_model.User, user_model.User.id == user_project_model.UserProject.user_id
    ).join(
        project_model.Project, project_model.Project.id == user_project_model.UserProject.project_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_project_model.UserProject.project_id == id
    )

    if skip:
        users_project_query = users_project_query.offset(skip)

    if limit:
        users_project_query = users_project_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_project_query = users_project_query.order_by(desc(sort))
        else:
            users_project_query = users_project_query.order_by(sort)
    else:
        users_project_query = users_project_query.order_by(
            user_project_model.UserProject.user_project_id)

    if limit == 1:
        users_project = users_project_query.first()
    else:
        users_project = users_project_query.all()

    if not users_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_project


@router.get("/{id}/projects", response_model=List[project_schema.ProjectResponse])
async def get_user_projects(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_projects: list = []

    user_projects_query = db.query(
        user_project_model.UserProject
    ).join(
        user_model.User, user_model.User.id == user_project_model.UserProject.user_id
    ).join(
        project_model.Project, project_model.Project.id == user_project_model.UserProject.project_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_project_model.UserProject.user_id == id
    )

    if skip:
        user_projects_query = user_projects_query.offset(skip)

    if limit:
        user_projects_query = user_projects_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            user_projects_query = user_projects_query.order_by(desc(sort))
        else:
            user_projects_query = user_projects_query.order_by(sort)
    else:
        user_projects_query = user_projects_query.order_by(
            user_project_model.UserProject.user_project_id)

    if limit == 1:
        user_projects = user_projects_query.first()
    else:
        user_projects = user_projects_query.all()

    if not user_projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")
    else:
        for user_project in user_projects:
            my_projects.append(user_project.project)

    return my_projects


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_projects(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    users_projects_query = db.query(
        user_project_model.UserProject
    ).filter(
        user_project_model.UserProject.user_project_id.in_(selected)
    )
    users_projects = users_projects_query.all()

    if not users_projects or len(users_projects) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for user_project in users_projects:
        if not check_if_in_list_of_dict(current_user['organizations'], user_project.project.organization.id) or user_project.user.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    users_projects_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
