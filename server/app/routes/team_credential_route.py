from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import team_credential_model, credential_model, organization_model, team_model, user_team_model, user_model, user_credential_model
from ..schemas import common_schema, user_schema, team_credential_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_teams_ids_in_list_of_response, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_teams_ids_list_from_response, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/teams-credentials",
    tags=['Teams | Credentials assigns']
)


@router.get("", response_model=List[team_credential_schema.TeamCredentialResponse])
async def get_teams_credentials(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    teams_credentials_query = db.query(
        team_credential_model.TeamCredential
    ).join(
        team_model.Team, team_model.Team.id == team_credential_model.TeamCredential.team_id
    ).join(
        credential_model.Credential, credential_model.Credential.id == team_credential_model.TeamCredential.credential_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        credential_model.Credential.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        teams_credentials_query = teams_credentials_query.offset(skip)

    if limit:
        teams_credentials_query = teams_credentials_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_credentials_query = teams_credentials_query.order_by(
                desc(sort))
        else:
            teams_credentials_query = teams_credentials_query.order_by(sort)
    else:
        teams_credentials_query = teams_credentials_query.order_by(
            team_credential_model.TeamCredential.team_credential_id)

    if limit == 1:
        teams_credentials = teams_credentials_query.first()
    else:
        teams_credentials = teams_credentials_query.all()

    if not teams_credentials:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_credentials


@router.post("", status_code=status.HTTP_201_CREATED, response_model=team_credential_schema.TeamCredentialResponse)
async def create_teams_credentials(
    payload: team_credential_schema.TeamCredentialPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.teams_id or not payload.credential_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign teams to credential! Provide a valid request")

    teams_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id.in_(payload.teams_id)
    )
    teams = teams_query.all()
    if not teams or len(teams) != len(payload.teams_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to credential! Provide a valid team")

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
                            detail="Can't assign teams to credential! Provide a valid credential")

    if not check_if_in_list_of_dict(current_user['organizations'], credential.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    teams_credentials_query = db.query(
        team_credential_model.TeamCredential
    ).join(
        team_model.Team, team_model.Team.id == team_credential_model.TeamCredential.team_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_credential_model.TeamCredential.team_id.in_(payload.teams_id),
        team_credential_model.TeamCredential.credential_id == payload.credential_id
    )
    teams_credentials = teams_credentials_query.all()

    if set(payload.teams_id) == set(get_teams_ids_list_from_response(teams_credentials)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign teams to credential! Assign already exists!")

    for team_id in payload.teams_id:
        if not check_if_teams_ids_in_list_of_response(teams_credentials, team_id):
            team_credential_payload = dict(
                team_id=team_id,
                credential_id=payload.credential_id
            )
            new_team_credential = team_credential_model.TeamCredential(
                **team_credential_payload)

            db.add(new_team_credential)
            db.commit()
            db.refresh(new_team_credential)

            if not new_team_credential:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign teams to credential! Something went wrong")
            else:
                users_teams_query = db.query(
                    user_team_model.UserTeam
                ).join(
                    user_model.User, user_model.User.id == user_team_model.UserTeam.user_id
                ).filter(
                    user_model.User.tower_id == current_user["user"].tower.id,
                    user_team_model.UserTeam.team_id == team_id
                )
                users_teams = users_teams_query.all()

                users_credentials_query = db.query(
                    user_credential_model.UserCredential
                ).join(
                    user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
                ).filter(
                    user_model.User.tower_id == current_user["user"].tower.id,
                    user_credential_model.UserCredential.user_id.in_(
                        get_users_ids_list_from_response(users_teams)),
                    user_credential_model.UserCredential.credential_id == payload.credential_id
                )
                users_credentials = users_credentials_query.all()

                for user_team in users_teams:
                    if not check_if_users_ids_in_list_of_response(users_credentials, user_team.user_id):
                        user_credential_payload = dict(
                            user_id=user_team.user.id,
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

    return new_team_credential


@router.get("/{id}/teams", response_model=List[team_credential_schema.TeamsCredentialResponse])
async def get_teams_credential(
    id: int,
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    teams_credential_query = db.query(
        team_credential_model.TeamCredential
    ).join(
        team_model.Team, team_model.Team.id == team_credential_model.TeamCredential.team_id
    ).join(
        credential_model.Credential, credential_model.Credential.id == team_credential_model.TeamCredential.credential_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        credential_model.Credential.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        team_credential_model.TeamCredential.credential_id == id
    )

    if skip:
        teams_credential_query = teams_credential_query.offset(skip)

    if limit:
        teams_credential_query = teams_credential_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_credential_query = teams_credential_query.order_by(
                desc(sort))
        else:
            teams_credential_query = teams_credential_query.order_by(sort)
    else:
        teams_credential_query = teams_credential_query.order_by(
            team_credential_model.TeamCredential.team_credential_id)

    if limit == 1:
        teams_credential = teams_credential_query.first()
    else:
        teams_credential = teams_credential_query.all()

    if not teams_credential:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_credential


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teams_credentials(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    team_credential_query = db.query(
        team_credential_model.TeamCredential
    ).filter(
        team_credential_model.TeamCredential.team_credential_id.in_(selected)
    )
    teams_credentials = team_credential_query.all()

    if not teams_credentials or len(teams_credentials) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for team_credential in teams_credentials:
        if not check_if_in_list_of_dict(current_user['organizations'], team_credential.credential.organization.id) or team_credential.team.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    team_credential_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
