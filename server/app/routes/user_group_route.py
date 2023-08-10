from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import user_group_model, user_model, group_model, organization_model
from ..schemas import common_schema, user_schema, user_group_schema, group_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/users-groups",
    tags=['Users | Groups assigns']
)


@router.get("", response_model=List[user_group_schema.UserGroupResponse])
async def get_users_groups(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_groups_query = db.query(
        user_group_model.UserGroup
    ).join(
        user_model.User, user_model.User.id == user_group_model.UserGroup.user_id
    ).join(
        group_model.Group, group_model.Group.id == user_group_model.UserGroup.group_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        users_groups_query = users_groups_query.offset(skip)

    if limit:
        users_groups_query = users_groups_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_groups_query = users_groups_query.order_by(desc(sort))
        else:
            users_groups_query = users_groups_query.order_by(sort)
    else:
        users_groups_query = users_groups_query.order_by(
            user_group_model.UserGroup.user_group_id)

    if limit == 1:
        users_groups = users_groups_query.first()
    else:
        users_groups = users_groups_query.all()

    if not users_groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_groups


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_group_schema.UserGroupResponse)
async def create_users_groups(
    payload: user_group_schema.UserGroupPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.users_id or not payload.group_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign users to group! Provide a valid request")

    users_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id.in_(payload.users_id)
    )
    users = users_query.all()
    if not users or len(users) != len(payload.users_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to group! Provide a valid user")

    group_query = db.query(
        group_model.Group
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.id == payload.group_id
    )
    group = group_query.first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to group! Provide a valid group")

    if not check_if_in_list_of_dict(current_user['organizations'], group.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    users_groups_query = db.query(
        user_group_model.UserGroup
    ).join(
        user_model.User, user_model.User.id == user_group_model.UserGroup.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_group_model.UserGroup.user_id.in_(payload.users_id),
        user_group_model.UserGroup.group_id == payload.group_id
    )
    users_groups = users_groups_query.all()

    if set(payload.users_id) == set(get_users_ids_list_from_response(users_groups)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign users to group! Assign already exists!")

    for user_id in payload.users_id:
        if not check_if_users_ids_in_list_of_response(users_groups, user_id):
            user_group_payload = dict(
                user_id=user_id,
                group_id=payload.group_id
            )
            new_user_group = user_group_model.UserGroup(**user_group_payload)

            db.add(new_user_group)
            db.commit()
            db.refresh(new_user_group)

            if not new_user_group:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign users to group! Something went wrong")

    return new_user_group


@router.get("/{id}/users", response_model=List[user_group_schema.UsersGroupResponse])
async def get_users_group(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_group_query = db.query(
        user_group_model.UserGroup
    ).join(
        user_model.User, user_model.User.id == user_group_model.UserGroup.user_id
    ).join(
        group_model.Group, group_model.Group.id == user_group_model.UserGroup.group_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_group_model.UserGroup.group_id == id
    )

    if skip:
        users_group_query = users_group_query.offset(skip)

    if limit:
        users_group_query = users_group_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_group_query = users_group_query.order_by(desc(sort))
        else:
            users_group_query = users_group_query.order_by(sort)
    else:
        users_group_query = users_group_query.order_by(
            user_group_model.UserGroup.user_group_id)

    if limit == 1:
        users_group = users_group_query.first()
    else:
        users_group = users_group_query.all()

    if not users_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_group


@router.get("/{id}/groups", response_model=List[group_schema.GroupResponse])
async def get_user_groups(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_groups: list = []

    user_groups_query = db.query(
        user_group_model.UserGroup
    ).join(
        user_model.User, user_model.User.id == user_group_model.UserGroup.user_id
    ).join(
        group_model.Group, group_model.Group.id == user_group_model.UserGroup.group_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_group_model.UserGroup.user_id == id
    )

    if skip:
        user_groups_query = user_groups_query.offset(skip)

    if limit:
        user_groups_query = user_groups_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            user_groups_query = user_groups_query.order_by(desc(sort))
        else:
            user_groups_query = user_groups_query.order_by(sort)
    else:
        user_groups_query = user_groups_query.order_by(
            user_group_model.UserGroup.user_group_id)

    if limit == 1:
        user_groups = user_groups_query.first()
    else:
        user_groups = user_groups_query.all()

    if not user_groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")
    else:
        for user_group in user_groups:
            my_groups.append(user_group.group)

    return my_groups


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_groups(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    users_groups_query = db.query(
        user_group_model.UserGroup
    ).filter(
        user_group_model.UserGroup.user_group_id.in_(selected)
    )
    users_groups = users_groups_query.all()

    if not users_groups or len(users_groups) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for user_group in users_groups:
        if not check_if_in_list_of_dict(current_user['organizations'], user_group.group.organization.id) or user_group.user.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    users_groups_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
