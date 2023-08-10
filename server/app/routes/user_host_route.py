from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import user_host_model, user_model, host_model, organization_model
from ..schemas import common_schema, user_schema, user_host_schema, host_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/users-hosts",
    tags=['Users | Hosts assigns']
)


@router.get("", response_model=List[user_host_schema.UserHostResponse])
async def get_users_hosts(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_hosts_query = db.query(
        user_host_model.UserHost
    ).join(
        user_model.User, user_model.User.id == user_host_model.UserHost.user_id
    ).join(
        host_model.Host, host_model.Host.id == user_host_model.UserHost.host_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        users_hosts_query = users_hosts_query.offset(skip)

    if limit:
        users_hosts_query = users_hosts_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_hosts_query = users_hosts_query.order_by(desc(sort))
        else:
            users_hosts_query = users_hosts_query.order_by(sort)
    else:
        users_hosts_query = users_hosts_query.order_by(
            user_host_model.UserHost.user_host_id)

    if limit == 1:
        users_hosts = users_hosts_query.first()
    else:
        users_hosts = users_hosts_query.all()

    if not users_hosts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_hosts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_host_schema.UserHostResponse)
async def create_users_hosts(
    payload: user_host_schema.UserHostPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.users_id or not payload.host_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign users to host! Provide a valid request")

    users_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id.in_(payload.users_id)
    )
    users = users_query.all()
    if not users or len(users) != len(payload.users_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to host! Provide a valid user")

    host_query = db.query(
        host_model.Host
    ).join(
        organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        host_model.Host.id == payload.host_id
    )
    host = host_query.first()
    if not host:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to host! Provide a valid host")

    if not check_if_in_list_of_dict(current_user['organizations'], host.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    users_hosts_query = db.query(
        user_host_model.UserHost
    ).join(
        user_model.User, user_model.User.id == user_host_model.UserHost.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_host_model.UserHost.user_id.in_(payload.users_id),
        user_host_model.UserHost.host_id == payload.host_id
    )
    users_hosts = users_hosts_query.all()

    if set(payload.users_id) == set(get_users_ids_list_from_response(users_hosts)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign users to host! Assign already exists!")

    for user_id in payload.users_id:
        if not check_if_users_ids_in_list_of_response(users_hosts, user_id):
            user_host_payload = dict(
                user_id=user_id,
                host_id=payload.host_id
            )
            new_user_host = user_host_model.UserHost(**user_host_payload)

            db.add(new_user_host)
            db.commit()
            db.refresh(new_user_host)

            if not new_user_host:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign users to host! Something went wrong")

    return new_user_host


@router.get("/{id}/users", response_model=List[user_host_schema.UsersHostResponse])
async def get_users_host(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_host_query = db.query(
        user_host_model.UserHost
    ).join(
        user_model.User, user_model.User.id == user_host_model.UserHost.user_id
    ).join(
        host_model.Host, host_model.Host.id == user_host_model.UserHost.host_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_host_model.UserHost.host_id == id
    )

    if skip:
        users_host_query = users_host_query.offset(skip)

    if limit:
        users_host_query = users_host_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_host_query = users_host_query.order_by(desc(sort))
        else:
            users_host_query = users_host_query.order_by(sort)
    else:
        users_host_query = users_host_query.order_by(
            user_host_model.UserHost.user_host_id)

    if limit == 1:
        users_host = users_host_query.first()
    else:
        users_host = users_host_query.all()

    if not users_host:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_host


@router.get("/{id}/hosts", response_model=List[host_schema.HostResponse])
async def get_user_hosts(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_hosts: list = []

    user_hosts_query = db.query(
        user_host_model.UserHost
    ).join(
        user_model.User, user_model.User.id == user_host_model.UserHost.user_id
    ).join(
        host_model.Host, host_model.Host.id == user_host_model.UserHost.host_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_host_model.UserHost.user_id == id
    )

    if skip:
        user_hosts_query = user_hosts_query.offset(skip)

    if limit:
        user_hosts_query = user_hosts_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            user_hosts_query = user_hosts_query.order_by(desc(sort))
        else:
            user_hosts_query = user_hosts_query.order_by(sort)
    else:
        user_hosts_query = user_hosts_query.order_by(
            user_host_model.UserHost.user_host_id)

    if limit == 1:
        user_hosts = user_hosts_query.first()
    else:
        user_hosts = user_hosts_query.all()

    if not user_hosts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")
    else:
        for user_host in user_hosts:
            my_hosts.append(user_host.host)

    return my_hosts


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_hosts(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    users_hosts_query = db.query(
        user_host_model.UserHost
    ).filter(
        user_host_model.UserHost.user_host_id.in_(selected)
    )
    users_hosts = users_hosts_query.all()

    if not users_hosts or len(users_hosts) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for user_host in users_hosts:
        if not check_if_in_list_of_dict(current_user['organizations'], user_host.host.organization.id) or user_host.user.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    users_hosts_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
