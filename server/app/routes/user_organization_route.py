from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import user_organization_model, user_model, organization_model
from ..schemas import common_schema, user_schema, user_organization_schema, organization_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/users-organizations",
    tags=['Users | Organizations assigns']
)


@router.get("", response_model=List[organization_schema.OrganizationResponse])
async def get_users_organizations(
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_organizations: list = []

    users_organizations_query = db.query(
        user_organization_model.UserOrganization
    ).join(
        user_model.User, user_model.User.id == user_organization_model.UserOrganization.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_organization_model.UserOrganization.user_id == current_user["user"].id
    )

    if skip:
        users_organizations_query = users_organizations_query.offset(skip)

    if limit:
        users_organizations_query = users_organizations_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_organizations_query = users_organizations_query.order_by(
                desc(sort))
        else:
            users_organizations_query = users_organizations_query.order_by(
                sort)
    else:
        users_organizations_query = users_organizations_query.order_by(
            user_organization_model.UserOrganization.user_organization_id)

    if limit == 1:
        users_organizations = users_organizations_query.first()
    else:
        users_organizations = users_organizations_query.all()

    if not users_organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")
    else:
        for user_organization in users_organizations:
            my_organizations.append(user_organization.organization)

    return my_organizations


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_organization_schema.UserOrganizationResponse)
async def create_users_organizations(
    payload: user_organization_schema.UserOrganizationPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.users_id or not payload.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign users to organization! Provide a valid request")

    users_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id.in_(payload.users_id)
    )
    users = users_query.all()
    if not users or len(users) != len(payload.users_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to organization! Provide a valid user")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to organization! Provide a valid organization")

    users_organizations_query = db.query(
        user_organization_model.UserOrganization
    ).join(
        user_model.User, user_model.User.id == user_organization_model.UserOrganization.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_organization_model.UserOrganization.user_id.in_(payload.users_id),
        user_organization_model.UserOrganization.organization_id == payload.organization_id
    )
    users_organizations = users_organizations_query.all()

    if set(payload.users_id) == set(get_users_ids_list_from_response(users_organizations)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign users to organization! Assign already exists!")

    for user_id in payload.users_id:
        if not check_if_users_ids_in_list_of_response(users_organizations, user_id):
            user_organization_payload = dict(
                user_id=user_id,
                organization_id=payload.organization_id
            )
            new_user_organization = user_organization_model.UserOrganization(
                **user_organization_payload)

            db.add(new_user_organization)
            db.commit()
            db.refresh(new_user_organization)

            if not new_user_organization:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign users to organization! Something went wrong")

    return new_user_organization


@router.get("/{id}/users", response_model=List[user_organization_schema.UsersOrganizationResponse])
async def get_users_organization(
    id: int,
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_organization_query = db.query(
        user_organization_model.UserOrganization
    ).join(
        user_model.User, user_model.User.id == user_organization_model.UserOrganization.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_organization_model.UserOrganization.organization_id == id
    )

    if skip:
        users_organization_query = users_organization_query.offset(skip)

    if limit:
        users_organization_query = users_organization_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_organization_query = users_organization_query.order_by(
                desc(sort))
        else:
            users_organization_query = users_organization_query.order_by(sort)
    else:
        users_organization_query = users_organization_query.order_by(
            user_organization_model.UserOrganization.user_organization_id)

    if limit == 1:
        users_organization = users_organization_query.first()
    else:
        users_organization = users_organization_query.all()

    if not users_organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_organization


@router.get("/{id}/organizations", response_model=List[user_organization_schema.UserOrganizationsResponse])
async def get_user_organizations(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    user_organizations_query = db.query(
        user_organization_model.UserOrganization
    ).join(
        user_model.User, user_model.User.id == user_organization_model.UserOrganization.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_organization_model.UserOrganization.user_id == id
    )

    if skip:
        user_organizations_query = user_organizations_query.offset(skip)

    if limit:
        user_organizations_query = user_organizations_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            user_organizations_query = user_organizations_query.order_by(
                desc(sort))
        else:
            user_organizations_query = user_organizations_query.order_by(sort)
    else:
        user_organizations_query = user_organizations_query.order_by(
            user_organization_model.UserOrganization.user_organization_id)

    if limit == 1:
        user_organizations = user_organizations_query.first()
    else:
        user_organizations = user_organizations_query.all()

    if not user_organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return user_organizations


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_organizations(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    user_organization_query = db.query(
        user_organization_model.UserOrganization
    ).filter(
        user_organization_model.UserOrganization.user_organization_id.in_(
            selected)
    )
    users_organizations = user_organization_query.all()

    if not users_organizations or len(users_organizations) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for user_organization in users_organizations:
        if user_organization.user.tower.id != current_user["user"].tower.id or user_organization.organization.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    user_organization_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
