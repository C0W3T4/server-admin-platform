from jose import jwt, JWTError
from fastapi import status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..schemas import auth_schema, user_schema, tower_schema
from ..models import user_model, user_team_model, user_organization_model, tower_model
# from datetime import datetime, timedelta
from ..configs.env_vars import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/login')

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception

        token_data = auth_schema.TokenData(user_id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def check_if_user_is_administrator(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> bool:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)

    user_query = db.query(
        user_model.User
    ).filter(
        user_model.User.id == token_data.user_id
    )
    user = user_query.first()

    if user.user_type == user_schema.UserType.admin or user.user_type == user_schema.UserType.system_administrator:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


def check_if_user_is_at_least_auditor(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> bool:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)

    user_query = db.query(
        user_model.User
    ).filter(
        user_model.User.id == token_data.user_id
    )
    user = user_query.first()

    if user.user_type == user_schema.UserType.admin or user.user_type == user_schema.UserType.system_administrator or user.user_type == user_schema.UserType.system_auditor:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> user_schema.CurrentUserResponse:
    my_teams: list = []
    my_organizations: list = []

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)

    user_query = db.query(
        user_model.User
    ).filter(
        user_model.User.id == token_data.user_id
    )
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't find user information")

    current_user_team_query = db.query(
        user_team_model.UserTeam
    ).join(
        user_model.User, user_model.User.id == user_team_model.UserTeam.user_id
    ).filter(
        user_model.User.tower_id == user.tower.id,
        user_team_model.UserTeam.user_id == user.id
    )
    current_user_team = current_user_team_query.all()

    if current_user_team:
        for user_team in current_user_team:
            my_teams.append(user_team.team)

    current_user_organization_query = db.query(
        user_organization_model.UserOrganization
    ).join(
        user_model.User, user_model.User.id == user_organization_model.UserOrganization.user_id
    ).filter(
        user_model.User.tower_id == user.tower.id,
        user_organization_model.UserOrganization.user_id == user.id
    )
    current_user_organization = current_user_organization_query.all()

    if current_user_organization:
        for user_organization in current_user_organization:
            my_organizations.append(user_organization.organization)

    return {
        "user": user,
        "teams": my_teams,
        "organizations": my_organizations
    }


def get_tower(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> tower_schema.TowerResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)

    user_query = db.query(
        user_model.User
    ).filter(
        user_model.User.id == token_data.user_id
    )
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't find user information")

    tower_query = db.query(
        tower_model.Tower
    ).filter(
        tower_model.Tower.id == user.tower_id
    )
    tower = tower_query.first()
    if not tower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't find tower information")

    return tower
