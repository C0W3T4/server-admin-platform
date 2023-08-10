from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models import host_model, organization_model, user_model, user_host_model
from ..schemas import host_schema, user_schema, common_schema, tower_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict
from app.services.tower.tower_service import add_host_fingerprint, delete_host_fingerprint
from app.utils.get_ids import get_ids_list
from ..auth import oauth2

router = APIRouter(
    prefix="/api/hosts",
    tags=['Hosts']
)


@router.get("", response_model=List[host_schema.HostResponse])
async def get_hosts(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_hostname: Optional[str] = "",
    search_by_ipv4: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    hosts_query = db.query(
        host_model.Host
    ).join(
        organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if search_by_hostname:
        hosts_query = hosts_query.filter(
            host_model.Host.hostname.contains(search_by_hostname)
        )

    if search_by_ipv4:
        hosts_query = hosts_query.filter(
            host_model.Host.ipv4.contains(search_by_ipv4))

    if skip:
        hosts_query = hosts_query.offset(skip)

    if limit:
        hosts_query = hosts_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            hosts_query = hosts_query.order_by(desc(sort))
        else:
            hosts_query = hosts_query.order_by(sort)
    else:
        hosts_query = hosts_query.order_by(host_model.Host.id)

    if limit == 1:
        hosts = hosts_query.first()
    else:
        hosts = hosts_query.all()

    if not hosts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find any hosts")

    return hosts


@router.get("/owner", response_model=List[host_schema.HostResponse])
async def get_my_hosts(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_hostname: Optional[str] = "",
    search_by_ipv4: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_hosts_query = db.query(
        host_model.Host
    ).join(
        organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        host_model.Host.created_by == current_user['user'].username
    ).distinct(
        host_model.Host.id
    )

    if search_by_hostname:
        hosts_query = hosts_query.filter(
            host_model.Host.hostname.contains(search_by_hostname)
        )

    if search_by_ipv4:
        hosts_query = hosts_query.filter(
            host_model.Host.ipv4.contains(search_by_ipv4)
        )

    if skip:
        my_hosts_query = my_hosts_query.offset(skip)

    if limit:
        my_hosts_query = my_hosts_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            my_hosts_query = my_hosts_query.order_by(desc(sort))
        else:
            my_hosts_query = my_hosts_query.order_by(sort)
    else:
        my_hosts_query = my_hosts_query.order_by(host_model.Host.id)

    if limit == 1:
        my_hosts = my_hosts_query.first()
    else:
        my_hosts = my_hosts_query.all()

    if not my_hosts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find any hosts")

    return my_hosts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=host_schema.HostResponse)
async def create_hosts(
    payload: host_schema.HostRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    if not payload.hostname or not payload.ipv4 or not payload.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't create host! Provide a valid request")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot create a host! Provide a valid Organization")

    if not check_if_in_list_of_dict(current_user['organizations'], payload.organization_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    host_query = db.query(
        host_model.Host
    ).join(
        organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id == payload.organization_id
    ).filter(
        or_(
            host_model.Host.hostname == payload.hostname,
            host_model.Host.ipv4 == payload.ipv4
        )
    )
    host = host_query.first()
    if host:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create host! Host already exists!")

    new_host_status = add_host_fingerprint(
        payload.ipv4,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not new_host_status:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't sync host! Something went wrong")

    updated_payload = dict(
        **payload.dict(),
        host_status=new_host_status if new_host_status else host_schema.HostStatus.alive,
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    new_host = host_model.Host(**updated_payload)

    db.add(new_host)
    db.commit()
    db.refresh(new_host)

    if not new_host:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create host! Something went wrong")
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
                                    detail="Can't assign user to host! Provide a valid user")

            admin_host_payload = dict(
                user_id=user.id,
                host_id=new_host.id
            )
            new_admin_host = user_host_model.UserHost(**admin_host_payload)

            db.add(new_admin_host)
            db.commit()
            db.refresh(new_admin_host)

            if not new_admin_host:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign user to host! Something went wrong")

        user_host_payload = dict(
            user_id=current_user["user"].id,
            host_id=new_host.id
        )
        new_user_host = user_host_model.new_admin_host = user_host_model.UserHost(
            **user_host_payload)

        db.add(new_user_host)
        db.commit()
        db.refresh(new_user_host)

        if not new_user_host:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't assign user to host! Something went wrong")

    return new_host


@router.get("/{id}", response_model=host_schema.HostResponse)
async def get_host(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    host_query = db.query(
        host_model.Host
    ).join(
        organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        host_model.Host.id == id
    )
    host = host_query.first()
    if not host:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Host not found")

    if not check_if_in_list_of_dict(current_user['organizations'], host.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return host


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_host(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    hosts_query = db.query(
        host_model.Host
    ).filter(
        host_model.Host.id.in_(selected)
    )
    hosts = hosts_query.all()

    if not hosts or len(hosts) != len(selected):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Host not found")

    for host in hosts:
        if not check_if_in_list_of_dict(current_user['organizations'], host.organization.id) or host.organization.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    deleted_host_key = delete_host_fingerprint(
        host.ipv4,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not deleted_host_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't delete host key! Something went wrong")

    hosts_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=host_schema.HostResponse)
async def update_host(
    id: int,
    payload: host_schema.HostRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    if not payload.hostname or not payload.ipv4 or not payload.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't update project! Provide a valid request")

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

    host_query = db.query(
        host_model.Host
    ).filter(
        host_model.Host.id == id
    )
    host = host_query.first()
    if not host:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Host not found")

    if not check_if_in_list_of_dict(current_user['organizations'], host.organization.id) or host.organization.tower.id != current_user["user"].tower.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if payload.hostname != host.hostname or payload.ipv4 != host.ipv4:
        new_host_query = db.query(
            host_model.Host
        ).join(
            organization_model.Organization, organization_model.Organization.id == host_model.Host.organization_id
        ).filter(
            organization_model.Organization.tower_id == current_user["user"].tower.id,
            host_model.Host.organization_id == payload.organization_id
        )
        if payload.hostname == host.hostname:
            new_host_query = new_host_query.filter(
                host_model.Host.ipv4 == payload.ipv4
            )
        elif payload.ipv4 == host.ipv4:
            new_host_query = new_host_query.filter(
                host_model.Host.hostname == payload.hostname
            )
        new_host = new_host_query.first()
        if new_host:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update host! Already exists!")

    if payload.ipv4 != host.ipv4:
        deleted_host_key = delete_host_fingerprint(
            host.ipv4,
            my_tower.ipv4,
            my_tower.port,
            my_tower.username,
            my_tower.password,
            10
        )
        if not deleted_host_key:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't delete host key! Something went wrong")

        new_host_status = add_host_fingerprint(
            payload.ipv4,
            my_tower.ipv4,
            my_tower.port,
            my_tower.username,
            my_tower.password,
            10
        )
        if not new_host_status:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't sync host! Something went wrong")

    updated_payload = dict(
        **payload.dict(),
        host_status=new_host_status if new_host_status else host.host_status,
        last_modified_by=current_user["user"].username
    )

    host_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_host = host_query.first()

    return updated_host


@router.put("/{id}/status", response_model=host_schema.HostResponse)
async def update_host_status(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    host_query = db.query(
        host_model.Host
    ).filter(
        host_model.Host.id == id
    )
    host = host_query.first()
    if not host:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Host not found")

    if not check_if_in_list_of_dict(current_user['organizations'], host.organization.id) or host.organization.tower.id != current_user["user"].tower.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    new_host_status = add_host_fingerprint(
        host.ipv4,
        my_tower.ipv4,
        my_tower.port,
        my_tower.username,
        my_tower.password,
        10
    )
    if not new_host_status:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't sync host! Something went wrong")

    updated_payload = dict(
        hostname=host.hostname,
        ipv4=host.ipv4,
        host_status=new_host_status if new_host_status else host.host_status,
        organization_id=host.organization_id,
        last_modified_by=current_user["user"].username
    )

    host_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_host = host_query.first()

    return updated_host
