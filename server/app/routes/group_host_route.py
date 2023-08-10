from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import group_host_model, group_model, organization_model, host_model, host_model, group_host_model
from ..schemas import common_schema, user_schema, group_host_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_hosts_ids_in_list_of_response, check_if_in_list_of_dict
from app.utils.get_ids import get_hosts_ids_list_from_response, get_ids_list
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/groups-hosts",
    tags=['Groups | Hosts assigns']
)


@router.get("", response_model=List[group_host_schema.GroupHostResponse])
async def get_groups_hosts(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    groups_hosts_query = db.query(
        group_host_model.GroupHost
    ).join(
        host_model.Host, host_model.Host.id == group_host_model.GroupHost.host_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        groups_hosts_query = groups_hosts_query.offset(skip)

    if limit:
        groups_hosts_query = groups_hosts_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            groups_hosts_query = groups_hosts_query.order_by(desc(sort))
        else:
            groups_hosts_query = groups_hosts_query.order_by(sort)
    else:
        groups_hosts_query = groups_hosts_query.order_by(
            group_host_model.GroupHost.group_host_id)

    if limit == 1:
        groups_hosts = groups_hosts_query.first()
    else:
        groups_hosts = groups_hosts_query.all()

    if not groups_hosts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return groups_hosts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=group_host_schema.GroupHostResponse)
async def create_groups_hosts(
    payload: group_host_schema.GroupHostPostRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.hosts_id or not payload.group_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign hosts to group! Provide a valid request")

    hosts_query = db.query(
        host_model.Host
    ).join(
        organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        host_model.Host.id.in_(payload.hosts_id)
    )
    hosts = hosts_query.all()
    if not hosts or len(hosts) != len(payload.hosts_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign hosts to group! Provide a valid host")

    group_query = db.query(
        group_model.Group
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        group_model.Group.id == payload.group_id
    )
    group = group_query.first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign hosts to group! Provide a valid group")

    if not check_if_in_list_of_dict(current_user['organizations'], group.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    groups_hosts_query = db.query(
        group_host_model.GroupHost
    ).join(
        host_model.Host, host_model.Host.id == group_host_model.GroupHost.host_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_host_model.GroupHost.host_id.in_(payload.hosts_id),
        group_host_model.GroupHost.group_id == payload.group_id
    )
    groups_hosts = groups_hosts_query.all()

    if set(payload.hosts_id) == set(get_hosts_ids_list_from_response(groups_hosts)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign hosts to group! Assign already exists!")

    for host_id in payload.hosts_id:
        if not check_if_hosts_ids_in_list_of_response(groups_hosts, host_id):
            group_host_payload = dict(
                host_id=host_id,
                group_id=payload.group_id
            )
            new_group_host = group_host_model.GroupHost(**group_host_payload)

            db.add(new_group_host)
            db.commit()
            db.refresh(new_group_host)

            if not new_group_host:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign hosts to group! Something went wrong")

    return new_group_host


@router.get("/{id}/groups", response_model=List[group_host_schema.GroupsHostResponse])
async def get_groups_host(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    groups_host_query = db.query(
        group_host_model.GroupHost
    ).join(
        host_model.Host, host_model.Host.id == group_host_model.GroupHost.host_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        group_host_model.GroupHost.host_id == id
    )

    if skip:
        groups_host_query = groups_host_query.offset(skip)

    if limit:
        groups_host_query = groups_host_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            groups_host_query = groups_host_query.order_by(desc(sort))
        else:
            groups_host_query = groups_host_query.order_by(sort)
    else:
        groups_host_query = groups_host_query.order_by(
            group_host_model.GroupHost.group_host_id)

    if limit == 1:
        groups_host = groups_host_query.first()
    else:
        groups_host = groups_host_query.all()

    if not groups_host:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return groups_host


@router.get("/{id}/hosts", response_model=List[group_host_schema.GroupHostsResponse])
async def get_group_hosts(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    group_hosts_query = db.query(
        group_host_model.GroupHost
    ).join(
        group_model.Group, group_model.Group.id == group_host_model.GroupHost.group_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        group_host_model.GroupHost.group_id == id
    )

    if skip:
        group_hosts_query = group_hosts_query.offset(skip)

    if limit:
        group_hosts_query = group_hosts_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            group_hosts_query = group_hosts_query.order_by(desc(sort))
        else:
            group_hosts_query = group_hosts_query.order_by(sort)
    else:
        group_hosts_query = group_hosts_query.order_by(
            group_host_model.GroupHost.group_host_id)

    if limit == 1:
        group_hosts = group_hosts_query.first()
    else:
        group_hosts = group_hosts_query.all()

    if not group_hosts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return group_hosts


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_groups_hosts(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    groups_hosts_query = db.query(
        group_host_model.GroupHost
    ).filter(
        group_host_model.GroupHost.group_host_id.in_(selected)
    )
    groups_hosts = groups_hosts_query.all()

    if not groups_hosts or len(groups_hosts) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for group_host in groups_hosts:
        if not check_if_in_list_of_dict(current_user['organizations'], group_host.group.organization.id) or group_host.group.organization.tower_id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    groups_hosts_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
