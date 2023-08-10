from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import credential_model, organization_model, user_credential_model, user_model
from ..schemas import credential_schema, user_schema, common_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict
from app.utils.get_ids import get_ids_list
from ..auth import oauth2

router = APIRouter(
    prefix="/api/credentials",
    tags=['Credentials']
)


@router.get("", response_model=List[credential_schema.CredentialResponse])
async def get_credentials(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    credentials_query = db.query(
        credential_model.Credential
    ).join(
        organization_model.Organization, organization_model.Organization.id == credential_model.Credential.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        credential_model.Credential.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if search_by_name:
        credentials_query = credentials_query.filter(
            credential_model.Credential.name.contains(search_by_name)
        )

    if skip:
        credentials_query = credentials_query.offset(skip)

    if limit:
        credentials_query = credentials_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            credentials_query = credentials_query.order_by(desc(sort))
        else:
            credentials_query = credentials_query.order_by(sort)
    else:
        credentials_query = credentials_query.order_by(
            credential_model.Credential.id)

    if limit == 1:
        credentials = credentials_query.first()
    else:
        credentials = credentials_query.all()

    if not credentials:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any credentials")

    return credentials


@router.get("/owner", response_model=List[credential_schema.CredentialResponse])
async def get_my_credentials(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_credentials_query = db.query(
        credential_model.Credential
    ).join(
        organization_model.Organization, organization_model.Organization.id == credential_model.Credential.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        credential_model.Credential.created_by == current_user['user'].username
    ).distinct(
        credential_model.Credential.id
    )

    if search_by_name:
        my_credentials_query = my_credentials_query.filter(
            credential_model.Credential.name.contains(search_by_name)
        )

    if skip:
        my_credentials_query = my_credentials_query.offset(skip)

    if limit:
        my_credentials_query = my_credentials_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            my_credentials_query = my_credentials_query.order_by(desc(sort))
        else:
            my_credentials_query = my_credentials_query.order_by(sort)
    else:
        my_credentials_query = my_credentials_query.order_by(
            credential_model.Credential.id)

    if limit == 1:
        my_credentials = my_credentials_query.first()
    else:
        my_credentials = my_credentials_query.all()

    if not my_credentials:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any credentials")

    return my_credentials


@router.post("", status_code=status.HTTP_201_CREATED, response_model=credential_schema.CredentialResponse)
async def create_credentials(
    payload: credential_schema.CredentialRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.name or not payload.username or not payload.password or not payload.port or not payload.organization_id or not payload.credential_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create credential")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot create a credential! Provide a valid organization")

    if not check_if_in_list_of_dict(current_user['organizations'], payload.organization_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    credential_query = db.query(
        credential_model.Credential
    ).join(
        organization_model.Organization, organization_model.Organization.id == credential_model.Credential.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        credential_model.Credential.organization_id == payload.organization_id,
        credential_model.Credential.name == payload.name
    )
    credential = credential_query.first()
    if credential:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create credential! Credential already exists!")

    user_credentials_query = db.query(
        user_credential_model.UserCredential
    ).join(
        user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
    ).join(
        credential_model.Credential, credential_model.Credential.id == user_credential_model.UserCredential.credential_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_credential_model.UserCredential.user_id == current_user["user"].id,
        credential_model.Credential.credential_type == credential_schema.CredentialType.source_control,
    )
    user_credentials = user_credentials_query.all()

    if user_credentials and payload.credential_type == credential_schema.CredentialType.source_control:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create credential! Already have source control credential type!")

    # TODO
    # hashed_password = hash(payload.password)
    # payload.password = hashed_password

    updated_payload = dict(
        **payload.dict(),
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    new_credential = credential_model.Credential(**updated_payload)

    db.add(new_credential)
    db.commit()
    db.refresh(new_credential)

    if not new_credential:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create credential! Something went wrong")
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
                                    detail="Can't assign user to credential! Provide a valid user")

            admin_credential_payload = dict(
                user_id=user.id,
                credential_id=new_credential.id
            )
            new_admin_credential = user_credential_model.UserCredential(
                **admin_credential_payload)

            db.add(new_admin_credential)
            db.commit()
            db.refresh(new_admin_credential)

            if not new_admin_credential:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign user to credential! Something went wrong")

        user_credential_payload = dict(
            user_id=current_user["user"].id,
            credential_id=new_credential.id
        )
        new_user_credential = user_credential_model.UserCredential(
            **user_credential_payload)

        db.add(new_user_credential)
        db.commit()
        db.refresh(new_user_credential)

        if not new_user_credential:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't assign user to credential! Something went wrong")

    return new_credential


@router.get("/{id}", response_model=credential_schema.CredentialResponse)
async def get_credential(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    credential_query = db.query(
        credential_model.Credential
    ).join(
        organization_model.Organization, organization_model.Organization.id == credential_model.Credential.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        credential_model.Credential.id == id
    )
    credential = credential_query.first()
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")

    if not check_if_in_list_of_dict(current_user['organizations'], credential.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return credential


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_credential(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    credentials_query = db.query(
        credential_model.Credential
    ).filter(
        credential_model.Credential.id.in_(selected)
    )
    credentials = credentials_query.all()

    if not credentials or len(credentials) != len(selected):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credentials not found")

    for credential in credentials:
        if not check_if_in_list_of_dict(current_user['organizations'], credential.organization.id) or credential.organization.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    credentials_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=credential_schema.CredentialResponse)
async def update_credential(
    id: int,
    payload: credential_schema.CredentialUpdateRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.name or not payload.username or not payload.port or not payload.organization_id or not payload.credential_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update credential")

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
                            detail="Cannot create a credential! Provide a valid organization")

    credential_query = db.query(
        credential_model.Credential
    ).filter(
        credential_model.Credential.id == id
    )
    credential = credential_query.first()

    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credential not found")

    if not check_if_in_list_of_dict(current_user['organizations'], credential.organization.id) or credential.organization.tower.id != current_user["user"].tower.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if payload.name != credential.name:
        new_credential_query = db.query(
            credential_model.Credential
        ).join(
            organization_model.Organization, organization_model.Organization.id == credential_model.Credential.organization_id
        ).filter(
            organization_model.Organization.tower_id == current_user["user"].tower.id,
            credential_model.Credential.organization_id == payload.organization_id,
            credential_model.Credential.name == payload.name
        )
        new_credential = new_credential_query.first()
        if new_credential:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update credential! Already exists!")

    if payload.credential_type != credential.credential_type:
        user_credentials_query = db.query(
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
        user_credentials = user_credentials_query.all()

        if user_credentials and payload.credential_type == credential_schema.CredentialType.source_control:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update credential! Already have source control credential type!")

    updated_payload = dict(
        **payload.dict(),
        password=credential.password,
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    credential_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_credential = credential_query.first()

    return updated_credential
