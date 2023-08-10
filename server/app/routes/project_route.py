from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models import project_model, organization_model, user_credential_model, user_model, credential_model, user_project_model
from ..schemas import project_schema, user_schema, common_schema, tower_schema, credential_schema
from ..database.connection import get_db
from app.utils.get_ids import get_ids_list
from app.utils.check_value_exists import check_if_in_list_of_dict
from app.services.tower.project_service import clone_repo, delete_projects, update_project_name, update_repo
from ..auth import oauth2

router = APIRouter(
    prefix="/api/projects",
    tags=['Projects']
)


@router.get("", response_model=List[project_schema.ProjectResponse])
async def get_projects(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    projects_query = db.query(
        project_model.Project
    ).join(
        organization_model.Organization, organization_model.Organization.id == project_model.Project.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if search_by_name:
        projects_query = projects_query.filter(
            project_model.Project.name.contains(search_by_name)
        )

    if skip:
        projects_query = projects_query.offset(skip)

    if limit:
        projects_query = projects_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            projects_query = projects_query.order_by(desc(sort))
        else:
            projects_query = projects_query.order_by(sort)
    else:
        projects_query = projects_query.order_by(project_model.Project.id)

    if limit == 1:
        projects = projects_query.first()
    else:
        projects = projects_query.all()

    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any projects")

    return projects


@router.get("/owner", response_model=List[project_schema.ProjectResponse])
async def get_my_projects(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_projects_query = db.query(
        project_model.Project
    ).join(
        organization_model.Organization, organization_model.Organization.id == project_model.Project.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        project_model.Project.created_by == current_user['user'].username
    ).distinct(
        project_model.Project.id
    )

    if search_by_name:
        my_projects_query = my_projects_query.filter(
            project_model.Project.name.contains(search_by_name)
        )

    if skip:
        my_projects_query = my_projects_query.offset(skip)

    if limit:
        my_projects_query = my_projects_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            my_projects_query = my_projects_query.order_by(desc(sort))
        else:
            my_projects_query = my_projects_query.order_by(sort)
    else:
        my_projects_query = my_projects_query.order_by(
            project_model.Project.id)

    if limit == 1:
        my_projects = my_projects_query.first()
    else:
        my_projects = my_projects_query.all()

    if not my_projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any projects")

    return my_projects


@router.post("", status_code=status.HTTP_201_CREATED, response_model=project_schema.ProjectResponse)
async def create_project(
    payload: project_schema.ProjectRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    if not payload.name or not payload.source_control_credential_type or not payload.tool or not payload.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create project")

    if payload.source_control_credential_type == project_schema.SourceControlCredentialType.manual:
        if not payload.base_path or not payload.playbook_directory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create project")
    elif payload.source_control_credential_type == project_schema.SourceControlCredentialType.git:
        if not payload.source_control_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create project")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot create a project! Provide a valid Organization")

    if not check_if_in_list_of_dict(current_user['organizations'], payload.organization_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    project_query = db.query(
        project_model.Project
    ).join(
        organization_model.Organization, organization_model.Organization.id == project_model.Project.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id == payload.organization_id
    ).filter(
        or_(
            project_model.Project.name == payload.name,
            project_model.Project.source_control_url == payload.source_control_url
        )
    )
    project = project_query.first()
    if project:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create project! Project already exists")

    user_credential_query = db.query(
        user_credential_model.UserCredential
    ).join(
        user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
    ).join(
        credential_model.Credential, credential_model.Credential.id == user_credential_model.UserCredential.credential_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_credential_model.UserCredential.user_id == current_user["user"].id,
        credential_model.Credential.credential_type == credential_schema.CredentialType.source_control
    )
    user_credential = user_credential_query.first()
    if not user_credential:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't create a project! Need to create a credential first!")

    cloned_repository = clone_repo(
        payload.source_control_url,
        organization.name,
        user_credential.credential.password,
        user_credential.credential.username,
        my_tower.company,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not cloned_repository:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't clone repository! Something went wrong")

    updated_payload = dict(
        **payload.dict(),
        project_status=cloned_repository if cloned_repository else project_schema.ProjectStatus.pending,
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    new_project = project_model.Project(**updated_payload)

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    if not new_project:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create project! Something went wrong")
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
                                    detail="Can't assign user to project! Provide a valid user")

            admin_project_payload = dict(
                user_id=user.id,
                project_id=new_project.id
            )
            new_admin_project = user_project_model.UserProject(
                **admin_project_payload)

            db.add(new_admin_project)
            db.commit()
            db.refresh(new_admin_project)

            if not new_admin_project:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign user to project! Something went wrong")

        user_project_payload = dict(
            user_id=current_user["user"].id,
            project_id=new_project.id
        )
        new_user_project = user_project_model.UserProject(
            **user_project_payload)

        db.add(new_user_project)
        db.commit()
        db.refresh(new_user_project)

        if not new_user_project:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't assign user to project! Something went wrong")

    return new_project


@router.get("/{id}", response_model=project_schema.ProjectResponse)
async def get_project(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    project_query = db.query(
        project_model.Project
    ).join(
        organization_model.Organization, organization_model.Organization.id == project_model.Project.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        project_model.Project.id == id
    )
    project = project_query.first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if not check_if_in_list_of_dict(current_user['organizations'], project.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return project


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    projects_query = db.query(
        project_model.Project
    ).filter(
        project_model.Project.id.in_(selected)
    )
    projects = projects_query.all()

    if not projects or len(projects) != len(selected):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    for project in projects:
        if not check_if_in_list_of_dict(current_user['organizations'], project.organization.id) or project.organization.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    deleted_projects = delete_projects(
        projects,
        my_tower.company,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not deleted_projects:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't delete projects! Something went wrong")

    projects_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=project_schema.ProjectResponse)
async def update_project(
    id: int,
    payload: project_schema.ProjectRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    updated_repo = None

    if not payload.name or not payload.source_control_credential_type or not payload.tool or not payload.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create project")

    if payload.source_control_credential_type == project_schema.SourceControlCredentialType.manual:
        if not payload.base_path or not payload.playbook_directory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create project")
    elif payload.source_control_credential_type == project_schema.SourceControlCredentialType.git:
        if not payload.source_control_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create project")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot create a project! Provide a valid Organization")

    project_query = db.query(
        project_model.Project
    ).filter(
        project_model.Project.id == id
    )
    project = project_query.first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if not check_if_in_list_of_dict(current_user['organizations'], project.organization.id) or project.organization.tower.id != current_user["user"].tower.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if payload.name != project.name or payload.source_control_url != project.source_control_url:
        new_project_query = db.query(
            project_model.Project
        ).join(
            organization_model.Organization, organization_model.Organization.id == project_model.Project.organization_id
        ).filter(
            organization_model.Organization.tower_id == current_user["user"].tower.id,
            project_model.Project.organization_id == payload.organization_id
        )
        if payload.name == project.name:
            new_project_query = new_project_query.filter(
                project_model.Project.source_control_url == payload.source_control_url
            )
        elif payload.source_control_url == project.source_control_url:
            new_project_query = new_project_query.filter(
                project_model.Project.name == payload.name
            )
        new_project = new_project_query.first()
        if new_project:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update project! Already exists!")

    if payload.organization_id != project.organization.id or payload.source_control_url != project.source_control_url:
        updated_project_name = update_project_name(
            organization.name,
            project.organization.name,
            project.source_control_url,
            payload.source_control_url,
            my_tower.company,
            my_tower.ipv4,
            my_tower.port,
            my_tower.username,
            my_tower.password,
            10
        )
        if not updated_project_name:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't update project! Something went wrong")

        if payload.source_control_url != project.source_control_url:
            user_credential_query = db.query(
                user_credential_model.UserCredential
            ).join(
                user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
            ).join(
                credential_model.Credential, credential_model.Credential.id == user_credential_model.UserCredential.credential_id
            ).filter(
                user_model.User.tower_id == current_user["user"].tower.id,
                user_credential_model.UserCredential.user_id == current_user["user"].id,
                credential_model.Credential.credential_type == credential_schema.CredentialType.source_control
            )
            user_credential = user_credential_query.first()
            if not user_credential:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Cannot update project! Need to create a credential first!")

            updated_repo = update_repo(
                payload.source_control_url,
                organization.name,
                user_credential.credential.password,
                user_credential.credential.username,
                my_tower.company,
                my_tower.ipv4,
                my_tower.port,
                my_tower.username,
                my_tower.password,
                10
            )
            if not updated_repo:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't update project! Something went wrong")

    if updated_repo:
        updated_payload = dict(
            **payload.dict(),
            project_status=updated_repo if updated_repo else project.project_status,
            last_modified_by=current_user["user"].username
        )
    else:
        updated_payload = dict(
            **payload.dict(),
            last_modified_by=current_user["user"].username
        )

    project_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_project = project_query.first()

    return updated_project


@router.put("/{id}/repo", response_model=project_schema.ProjectResponse)
async def update_repo_project(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    project_query = db.query(
        project_model.Project
    ).filter(
        project_model.Project.id == id
    )
    project = project_query.first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if not check_if_in_list_of_dict(current_user['organizations'], project.organization.id) or project.organization.tower.id != current_user["user"].tower.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    user_credential_query = db.query(
        user_credential_model.UserCredential
    ).join(
        user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
    ).join(
        credential_model.Credential, credential_model.Credential.id == user_credential_model.UserCredential.credential_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_credential_model.UserCredential.user_id == current_user["user"].id,
        credential_model.Credential.credential_type == credential_schema.CredentialType.source_control
    )
    user_credential = user_credential_query.first()
    if not user_credential:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot update project! Need to create a credential first!")

    updated_repo = update_repo(
        project.source_control_url,
        project.organization.name,
        user_credential.credential.password,
        user_credential.credential.username,
        my_tower.company,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not updated_repo:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't update project! Something went wrong")

    updated_payload = dict(
        name=project.name,
        source_control_credential_type=project.source_control_credential_type,
        tool=project.tool,
        source_control_url=project.source_control_url,
        project_status=updated_repo if updated_repo else project.project_status,
        organization_id=project.organization_id,
        last_modified_by=current_user["user"].username
    )

    project_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_project = project_query.first()

    return updated_project
