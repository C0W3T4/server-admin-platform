from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models import user_model, tower_model, organization_model, user_team_model, user_organization_model
from ..schemas import auth_schema, user_schema, tower_schema
from ..database.connection import get_db
from ..utils import auth
from ..auth.oauth2 import create_access_token
from app.services.tower.tower_service import check_host_connection, create_tower_directory, install_tower_services
from app.services.tower.organization_service import create_organization_directories

router = APIRouter(
    prefix="/api",
    tags=['Authentication']
)


@router.post("/register", response_model=auth_schema.RegisterAccountResponse)
async def register_account(
    payload: auth_schema.RegisterAccountRequest,
    db: Session = Depends(get_db)
):
    if not payload.company or not payload.hostname or not payload.ipv4 or not payload.username or not payload.password or not payload.port or not payload.admin_username or not payload.admin_password or not payload.organization_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't create account! Provide a valid request")

    tower_query = db.query(
        tower_model.Tower
    ).filter(
        tower_model.Tower.company == payload.company
    )
    tower = tower_query.first()
    if tower:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create account! Account already exists!")

    # TODO: Hash hosts passwords
    hashed_admin_password = auth.hash(payload.admin_password)
    payload.admin_password = hashed_admin_password

    tower_status = check_host_connection(
        payload.ipv4,
        payload.port,
        payload.username,
        payload.password,
        10
    )
    if not tower_status:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't connect to tower! Something went wrong")

    services_installed = install_tower_services(
        payload.ipv4,
        payload.port,
        payload.username,
        payload.password,
        10
    )
    if not services_installed:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't install tower services! Something went wrong")

    tower_directory = create_tower_directory(
        payload.company,
        payload.ipv4,
        payload.port,
        payload.username,
        payload.password,
        10
    )
    if not tower_directory:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create directory! Something went wrong")

    organization_directories = create_organization_directories(
        payload.company,
        payload.organization_name,
        payload.ipv4,
        payload.port,
        payload.username,
        payload.password,
        10
    )
    if not organization_directories:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create organization directories! Something went wrong")

    tower_payload = dict(
        company=payload.company,
        hostname=payload.hostname,
        ipv4=payload.ipv4,
        username=payload.username,
        port=payload.port,
        password=payload.password,
        tower_status=tower_schema.TowerStatus.alive,
        created_by=payload.admin_username,
        last_modified_by=payload.admin_username
    )

    new_tower = tower_model.Tower(**tower_payload)

    db.add(new_tower)
    db.commit()
    db.refresh(new_tower)

    if not new_tower:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create tower! Something went wrong")

    user_payload = dict(
        username=payload.admin_username,
        user_type=user_schema.UserType.admin,
        password=payload.admin_password,
        tower_id=new_tower.id,
        created_by=payload.admin_username,
        last_modified_by=payload.admin_username
    )

    new_user = user_model.User(**user_payload)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if not new_user:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create user! Something went wrong")

    organization_payload = dict(
        name=payload.organization_name,
        tower_id=new_tower.id,
        created_by=payload.admin_username,
        last_modified_by=payload.admin_username
    )

    new_organization = organization_model.Organization(**organization_payload)

    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)

    if not new_organization:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create organization! Something went wrong")

    if new_user and new_organization:
        user_organization_payload = dict(
            user_id=new_user.id,
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

    return {
        "tower": new_tower,
        "user": new_user,
        "organization": new_organization
    }


@router.post("/login", response_model=auth_schema.TokenResponse)
async def login(
    payload: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    my_teams: list = []
    my_organizations: list = []

    tower_query = db.query(
        tower_model.Tower
    ).filter(
        tower_model.Tower.company == payload.client_id
    )
    tower = tower_query.first()
    if not tower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tower not found")

    user_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == tower.id,
        user_model.User.username == payload.username
    )
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not auth.verify(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    current_user_team_query = db.query(
        user_team_model.UserTeam
    ).filter(
        user_team_model.UserTeam.user_id == user.id
    )
    current_user_team = current_user_team_query.all()

    if current_user_team:
        for user_team in current_user_team:
            my_teams.append(user_team.team)

    current_user_organization_query = db.query(
        user_organization_model.UserOrganization
    ).filter(
        user_organization_model.UserOrganization.user_id == user.id
    )
    current_user_organization = current_user_organization_query.all()

    if current_user_organization:
        for user_organization in current_user_organization:
            my_organizations.append(user_organization.organization)

    access_token = create_access_token(data={"user_id": user.id})

    return {
        "user": user,
        "teams": my_teams,
        "organizations": my_organizations,
        "access_token": access_token,
        "token_type": "Bearer"
    }
