from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models import group_model, organization_model, user_model, user_group_model
from ..schemas import group_schema, user_schema, common_schema
from app.utils.check_value_exists import check_if_in_list_of_dict
from app.utils.get_ids import get_ids_list
from ..database.connection import get_db
from ..auth import oauth2

router = APIRouter(
    prefix="/api/groups",
    tags=['Groups']
)


@router.get("", response_model=List[group_schema.GroupResponse])
async def get_groups(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    groups_query = db.query(
        group_model.Group
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if search_by_name:
        groups_query = groups_query.filter(
            group_model.Group.name.contains(search_by_name)
        )

    if skip:
        groups_query = groups_query.offset(skip)

    if limit:
        groups_query = groups_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            groups_query = groups_query.order_by(desc(sort))
        else:
            groups_query = groups_query.order_by(sort)
    else:
        groups_query = groups_query.order_by(group_model.Group.id)

    if limit == 1:
        groups = groups_query.first()
    else:
        groups = groups_query.all()

    if not groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any groups")

    return groups


@router.get("/owner", response_model=List[group_schema.GroupResponse])
async def get_my_groups(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_groups_query = db.query(
        group_model.Group
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.created_by == current_user['user'].username
    ).distinct(
        group_model.Group.id
    )

    if search_by_name:
        my_groups_query = my_groups_query.filter(
            group_model.Group.name.contains(search_by_name)
        )

    if skip:
        my_groups_query = my_groups_query.offset(skip)

    if limit:
        my_groups_query = my_groups_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            my_groups_query = my_groups_query.order_by(desc(sort))
        else:
            my_groups_query = my_groups_query.order_by(sort)
    else:
        my_groups_query = my_groups_query.order_by(group_model.Group.id)

    if limit == 1:
        my_groups = my_groups_query.first()
    else:
        my_groups = my_groups_query.all()

    if not my_groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any groups")

    return my_groups


@router.post("", status_code=status.HTTP_201_CREATED, response_model=group_schema.GroupResponse)
async def create_groups(
    payload: group_schema.GroupRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.name or not payload.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't create group! Provide a valid request")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't create group! Provide a valid organization")

    if not check_if_in_list_of_dict(current_user['organizations'], payload.organization_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    group_query = db.query(
        group_model.Group
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id == payload.organization_id,
        group_model.Group.name == payload.name
    )
    group = group_query.first()
    if group:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create group! Group already exists!")

    updated_payload = dict(
        **payload.dict(),
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    new_group = group_model.Group(**updated_payload)

    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    if not new_group:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create group! Something went wrong")
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
                                    detail="Can't assign user to group! Provide a valid user")

            admin_group_payload = dict(
                user_id=user.id,
                group_id=new_group.id
            )
            new_admin_group = user_group_model.UserGroup(**admin_group_payload)

            db.add(new_admin_group)
            db.commit()
            db.refresh(new_admin_group)

            if not new_admin_group:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign user to group! Something went wrong")

        user_group_payload = dict(
            user_id=current_user["user"].id,
            group_id=new_group.id
        )
        new_user_group = user_group_model.UserGroup(**user_group_payload)

        db.add(new_user_group)
        db.commit()
        db.refresh(new_user_group)

        if not new_user_group:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't assign user to group! Something went wrong")

    return new_group


@router.get("/{id}", response_model=group_schema.GroupResponse)
async def get_group(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    group_query = db.query(
        group_model.Group
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.id == id
    )
    group = group_query.first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if not check_if_in_list_of_dict(current_user['organizations'], group.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return group


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    groups_query = db.query(
        group_model.Group
    ).filter(
        group_model.Group.id.in_(selected)
    )
    groups = groups_query.all()

    if not groups or len(groups) != len(selected):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    for group in groups:
        if not check_if_in_list_of_dict(current_user['organizations'], group.organization.id) or group.organization.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    groups_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=group_schema.GroupResponse)
async def update_group(
    id: int,
    payload: group_schema.GroupRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.name or not payload.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't update group! Provide a valid request")

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
                            detail="Cannot create a project! Provide a valid Organization")

    group_query = db.query(
        group_model.Group
    ).filter(
        group_model.Group.id == id
    )
    group = group_query.first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if not check_if_in_list_of_dict(current_user['organizations'], group.organization.id) or group.organization.tower.id != current_user["user"].tower.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if payload.name != group.name:
        new_group_query = db.query(
            group_model.Group
        ).join(
            organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
        ).filter(
            organization_model.Organization.tower_id == current_user["user"].tower.id,
            group_model.Group.organization_id == payload.organization_id,
            group_model.Group.name == payload.name
        )
        new_group = new_group_query.first()
        if new_group:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update group! Group already exists!")

    updated_payload = dict(
        **payload.dict(),
        last_modified_by=current_user["user"].username
    )

    group_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_group = group_query.first()

    return updated_group
