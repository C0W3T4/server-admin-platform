from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import organization_model, user_organization_model, user_model
from ..schemas import organization_schema, user_schema, common_schema, tower_schema
from app.services.tower.organization_service import create_organization_directories, delete_organization_remote, update_organization_name
from ..auth import oauth2
from ..database.connection import get_db

router = APIRouter(
    prefix="/api/organizations",
    tags=['Organizations']
)


@router.get("", response_model=List[organization_schema.OrganizationResponse])
async def get_organizations(
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    organizations_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id
    )

    if search_by_name:
        organizations_query = organizations_query.filter(
            organization_model.Organization.name.contains(search_by_name)
        )

    if skip:
        organizations_query = organizations_query.offset(skip)

    if limit:
        organizations_query = organizations_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            organizations_query = organizations_query.order_by(desc(sort))
        else:
            organizations_query = organizations_query.order_by(sort)
    else:
        organizations_query = organizations_query.order_by(
            organization_model.Organization.id)

    if limit == 1:
        organizations = organizations_query.first()
    else:
        organizations = organizations_query.all()

    if not organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any organizations")

    return organizations


@router.get("/owner", response_model=List[organization_schema.OrganizationResponse])
async def get_my_organizations(
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    organizations_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.created_by == current_user["user"].username
    )

    if search_by_name:
        organizations_query = organizations_query.filter(
            organization_model.Organization.name.contains(search_by_name)
        )

    if skip:
        organizations_query = organizations_query.offset(skip)

    if limit:
        organizations_query = organizations_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            organizations_query = organizations_query.order_by(desc(sort))
        else:
            organizations_query = organizations_query.order_by(sort)
    else:
        organizations_query = organizations_query.order_by(
            organization_model.Organization.id)

    if limit == 1:
        organizations = organizations_query.first()
    else:
        organizations = organizations_query.all()

    if not organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any organizations")

    return organizations


@router.post("", status_code=status.HTTP_201_CREATED, response_model=organization_schema.OrganizationResponse)
async def create_organizations(
    payload: organization_schema.OrganizationRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't create organization! Provide a valid request")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.name == payload.name
    )
    organization = organization_query.first()

    if organization:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create organization! Organization already exists!")

    updated_payload = dict(
        **payload.dict(),
        tower_id=current_user["user"].tower.id,
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    new_organization = organization_model.Organization(**updated_payload)

    organization_directories = create_organization_directories(
        my_tower.company,
        payload.name,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not organization_directories:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create directory! Something went wrong")

    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)

    if not new_organization:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create organization! Something went wrong")
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
                                    detail="Can't assign user to organization! Provide a valid user")

            admin_organization_payload = dict(
                user_id=user.id,
                organization_id=new_organization.id
            )
            new_admin_organization = user_organization_model.UserOrganization(
                **admin_organization_payload)

            db.add(new_admin_organization)
            db.commit()
            db.refresh(new_admin_organization)

            if not new_admin_organization:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign user to organization! Something went wrong")

        user_organization_payload = dict(
            user_id=current_user["user"].id,
            organization_id=new_organization.id
        )
        new_user_organization = user_organization_model.UserOrganization(
            **user_organization_payload)

        db.add(new_user_organization)
        db.commit()
        db.refresh(new_user_organization)

        if not new_user_organization:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't assign user to organization! Something went wrong")

    return new_organization


@router.get("/{id}", response_model=organization_schema.OrganizationResponse)
async def get_organization(
    id: int,
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == id
    )
    organization = organization_query.first()

    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Organization not found")

    return organization


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id.in_(selected)
    )
    organizations = organization_query.all()

    if not organizations or len(organizations) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some organizations not found")

    for organization in organizations:
        deleted_organization_remote = delete_organization_remote(
            organization.name,
            my_tower.company,
            my_tower.ipv4,
            my_tower.port,
            my_tower.username,
            my_tower.password,
            10
        )
        if not deleted_organization_remote:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't delete organizations on remote! Something went wrong")

    organization_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=organization_schema.OrganizationResponse)
async def update_organization(
    id: int,
    payload: organization_schema.OrganizationRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't update organization! Provide a valid request")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Organization not found")

    updated_payload = dict(
        **payload.dict(),
        tower_id=organization.tower.id,
        created_by=organization.created_by,
        last_modified_by=current_user["user"].username
    )

    if payload.name != organization.name:
        new_organization_query = db.query(
            organization_model.Organization
        ).filter(
            organization_model.Organization.tower_id == current_user["user"].tower.id,
            organization_model.Organization.name == payload.name
        )
        new_organization = new_organization_query.first()
        if new_organization:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update organization! Organization already exists!")

        updated_organization_name = update_organization_name(
            organization.name,
            payload.name,
            my_tower.company,
            my_tower.ipv4,
            my_tower.port,
            my_tower.username,
            my_tower.password,
            10
        )
        if not updated_organization_name:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't update organization! Something went wrong")

    organization_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_organization = organization_query.first()

    return updated_organization
