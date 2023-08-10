from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import user_model
from ..schemas import user_schema, common_schema
from ..database.connection import get_db
from ..auth import oauth2
from ..utils import auth

router = APIRouter(
    prefix="/api/users",
    tags=['Users']
)


@router.get("", response_model=List[user_schema.UserResponse])
async def get_users(
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_first_name: Optional[str] = "",
    search_last_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id
    )

    if search_first_name:
        users_query = users_query.filter(
            user_model.User.first_name.contains(search_first_name)
        )

    if search_last_name:
        users_query = users_query.filter(
            user_model.User.last_name.contains(search_last_name)
        )

    if skip:
        users_query = users_query.offset(skip)

    if limit:
        users_query = users_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_query = users_query.order_by(desc(sort))
        else:
            users_query = users_query.order_by(sort)
    else:
        users_query = users_query.order_by(user_model.User.id)

    if limit == 1:
        users = users_query.first()
    else:
        users = users_query.all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find any users")

    return users


@router.get("/current", response_model=user_schema.UserResponse)
async def get_current_user(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find user")

    return current_user["user"]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserResponse)
async def create_user(
    payload: user_schema.UserRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.username or not payload.user_type or not payload.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't create user! Provide a valid request")

    user_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.username == payload.username
    )
    user = user_query.first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create user! User already exists!")

    admin_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.user_type == user_schema.UserType.admin
    )
    admin = admin_query.first()
    if admin and payload.user_type == user_schema.UserType.admin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create user! Only can exists one admin user!")

    hashed_password = auth.hash(payload.password)
    payload.password = hashed_password

    updated_payload = dict(
        **payload.dict(),
        tower_id=current_user["user"].tower.id,
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    new_user = user_model.User(**updated_payload)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if not new_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create user! Something went wrong")

    return new_user


@router.get("/{id}", response_model=user_schema.UserResponse)
async def get_user(
    id: int,
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    user_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id == id
    )
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    user_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id.in_(selected)
    )
    users = user_query.all()

    if not users or len(users) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some users not found")

    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/current", response_model=user_schema.UserResponse)
async def update_current_user(
    payload: user_schema.CurrentUserRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't update user! Provide a valid request")

    user_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id == current_user["user"].id
    )
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if current_user["user"].id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if payload.username != user.username:
        new_user_query = db.query(
            user_model.User
        ).filter(
            user_model.User.tower_id == current_user["user"].tower.id,
            user_model.User.username == payload.username
        )
        new_user = new_user_query.first()
        if new_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update user! User already exists!")

    # if payload.password:
    #     hashed_password = auth.hash(payload.password)
    #     payload.password = hashed_password

    updated_payload = dict(
        **payload.dict(),
        last_modified_by=current_user["user"].username
    )

    user_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_user = user_query.first()

    return updated_user


@router.put("/{id}", response_model=user_schema.UserResponse)
async def update_user(
    id: int,
    payload: user_schema.UserBase,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.username or not payload.user_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't update user! Provide a valid request")

    user_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id == id
    )
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if payload.username != user.username:
        new_user_query = db.query(
            user_model.User
        ).filter(
            user_model.User.tower_id == current_user["user"].tower.id,
            user_model.User.username == payload.username
        )
        new_user = new_user_query.first()
        if new_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update user! User already exists!")

    if payload.user_type != user.user_type:
        admin_query = db.query(
            user_model.User
        ).filter(
            user_model.User.tower_id == current_user["user"].tower.id,
            user_model.User.user_type == user_schema.UserType.admin
        )
        admin = admin_query.first()
        if admin and payload.user_type == user_schema.UserType.admin:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update user! Only can exists one admin user!")

    updated_payload = dict(
        **payload.dict(),
        last_modified_by=current_user["user"].username
    )

    user_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_user = user_query.first()

    return updated_user
