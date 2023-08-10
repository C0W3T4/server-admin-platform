from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import user_credential_model, user_model, credential_model, organization_model
from ..schemas import common_schema, user_schema, user_credential_schema, credential_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/users-credentials",
    tags=['Users | Credentials assigns']
)


@router.get("", response_model=List[user_credential_schema.UserCredentialResponse])
async def get_users_credentials(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_credentials_query = db.query(
        user_credential_model.UserCredential
    ).join(
        user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
    ).join(
        credential_model.Credential, credential_model.Credential.id == user_credential_model.UserCredential.credential_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        credential_model.Credential.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        users_credentials_query = users_credentials_query.offset(skip)

    if limit:
        users_credentials_query = users_credentials_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_credentials_query = users_credentials_query.order_by(
                desc(sort))
        else:
            users_credentials_query = users_credentials_query.order_by(sort)
    else:
        users_credentials_query = users_credentials_query.order_by(
            user_credential_model.UserCredential.user_credential_id)

    if limit == 1:
        users_credentials = users_credentials_query.first()
    else:
        users_credentials = users_credentials_query.all()

    if not users_credentials:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_credentials


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_credential_schema.UserCredentialResponse)
async def create_users_credentials(
    payload: user_credential_schema.UserCredentialPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.users_id or not payload.credential_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign users to credential! Provide a valid request")

    users_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id.in_(payload.users_id)
    )
    users = users_query.all()
    if not users or len(users) != len(payload.users_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to credential! Provide a valid user")

    credential_query = db.query(
        credential_model.Credential
    ).join(
        organization_model.Organization, organization_model.Organization.id == credential_model.Credential.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        credential_model.Credential.id == payload.credential_id
    )
    credential = credential_query.first()
    if not credential:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to credential! Provide a valid credential")

    if not check_if_in_list_of_dict(current_user['organizations'], credential.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if credential.credential_type == credential_schema.CredentialType.source_control:
        source_users_credentials_query = db.query(
            user_credential_model.UserCredential
        ).join(
            user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
        ).join(
            credential_model.Credential, credential_model.Credential.id == user_credential_model.UserCredential.credential_id
        ).filter(
            user_model.User.tower_id == current_user["user"].tower.id,
            user_credential_model.UserCredential.user_id.in_(payload.users_id),
            credential_model.Credential.credential_type == credential_schema.CredentialType.source_control
        )
        source_users_credentials = source_users_credentials_query.all()

        if source_users_credentials:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't assign users to credential! Some users already have source control credential type!")

    users_credentials_query = db.query(
        user_credential_model.UserCredential
    ).join(
        user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_credential_model.UserCredential.user_id.in_(payload.users_id),
        user_credential_model.UserCredential.credential_id == payload.credential_id
    )
    users_credentials = users_credentials_query.all()

    if set(payload.users_id) == set(get_users_ids_list_from_response(users_credentials)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign users to credential! Assign already exists!")

    for user_id in payload.users_id:
        if not check_if_users_ids_in_list_of_response(users_credentials, user_id):
            user_credential_payload = dict(
                user_id=user_id,
                credential_id=payload.credential_id
            )
            new_user_credential = user_credential_model.UserCredential(
                **user_credential_payload)

            db.add(new_user_credential)
            db.commit()
            db.refresh(new_user_credential)

            if not new_user_credential:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign users to credential! Something went wrong")

    return new_user_credential


@router.get("/{id}/users", response_model=List[user_credential_schema.UsersCredentialResponse])
async def get_users_credential(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_credential_query = db.query(
        user_credential_model.UserCredential
    ).join(
        user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
    ).join(
        credential_model.Credential, credential_model.Credential.id == user_credential_model.UserCredential.credential_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        credential_model.Credential.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_credential_model.UserCredential.credential_id == id
    )

    if skip:
        users_credential_query = users_credential_query.offset(skip)

    if limit:
        users_credential_query = users_credential_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_credential_query = users_credential_query.order_by(
                desc(sort))
        else:
            users_credential_query = users_credential_query.order_by(sort)
    else:
        users_credential_query = users_credential_query.order_by(
            user_credential_model.UserCredential.user_credential_id)

    if limit == 1:
        users_credential = users_credential_query.first()
    else:
        users_credential = users_credential_query.all()

    if not users_credential:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_credential


@router.get("/{id}/credentials", response_model=List[credential_schema.CredentialResponse])
async def get_user_credentials(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_credentials: list = []

    user_credentials_query = db.query(
        user_credential_model.UserCredential
    ).join(
        user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
    ).join(
        credential_model.Credential, credential_model.Credential.id == user_credential_model.UserCredential.credential_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        credential_model.Credential.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_credential_model.UserCredential.user_id == id
    )

    if skip:
        user_credentials_query = user_credentials_query.offset(skip)

    if limit:
        user_credentials_query = user_credentials_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            user_credentials_query = user_credentials_query.order_by(
                desc(sort))
        else:
            user_credentials_query = user_credentials_query.order_by(sort)
    else:
        user_credentials_query = user_credentials_query.order_by(
            user_credential_model.UserCredential.user_credential_id)

    if limit == 1:
        user_credentials = user_credentials_query.first()
    else:
        user_credentials = user_credentials_query.all()

    if not user_credentials:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")
    else:
        for user_credential in user_credentials:
            my_credentials.append(user_credential.credential)

    return my_credentials


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_credentials(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    users_credentials_query = db.query(
        user_credential_model.UserCredential
    ).filter(
        user_credential_model.UserCredential.user_credential_id.in_(selected)
    )
    users_credentials = users_credentials_query.all()

    if not users_credentials or len(users_credentials) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for user_credential in users_credentials:
        if not check_if_in_list_of_dict(current_user['organizations'], user_credential.credential.organization.id) or user_credential.user.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    users_credentials_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
