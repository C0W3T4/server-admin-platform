from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.check_value_exists import check_if_teams_ids_in_list_of_response, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_teams_ids_list_from_response, get_users_ids_list_from_response
from ..models import team_organization_model, organization_model, team_model, user_model, user_team_model, user_organization_model
from ..schemas import common_schema, user_schema, team_organization_schema
from ..database.connection import get_db
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/teams-organizations",
    tags=['Teams | Organizations assigns']
)


@router.get("", response_model=List[team_organization_schema.TeamOrganizationResponse])
async def get_teams_organizations(
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
    teams_organizations_query = db.query(
        team_organization_model.TeamOrganization
    ).join(
        organization_model.Organization, organization_model.Organization.id == team_organization_model.TeamOrganization.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id
    )

    if skip:
        teams_organizations_query = teams_organizations_query.offset(skip)

    if limit:
        teams_organizations_query = teams_organizations_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_organizations_query = teams_organizations_query.order_by(
                desc(sort))
        else:
            teams_organizations_query = teams_organizations_query.order_by(
                sort)
    else:
        teams_organizations_query = teams_organizations_query.order_by(
            team_organization_model.TeamOrganization.team_organization_id)

    if limit == 1:
        teams_organizations = teams_organizations_query.first()
    else:
        teams_organizations = teams_organizations_query.all()

    if not teams_organizations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_organizations


@router.post("", status_code=status.HTTP_201_CREATED, response_model=team_organization_schema.TeamOrganizationResponse)
async def create_teams_organizations(
    payload: team_organization_schema.TeamOrganizationPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.teams_id or not payload.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign teams to organization! Provide a valid request")

    teams_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id.in_(payload.teams_id)
    )
    teams = teams_query.all()
    if not teams or len(teams) != len(payload.teams_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to organization! Provide a valid team")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to organization! Provide a valid organization")

    teams_organizations_query = db.query(
        team_organization_model.TeamOrganization
    ).join(
        organization_model.Organization, organization_model.Organization.id == team_organization_model.TeamOrganization.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        team_organization_model.TeamOrganization.team_id.in_(payload.teams_id),
        team_organization_model.TeamOrganization.organization_id == payload.organization_id
    )
    teams_organizations = teams_organizations_query.all()

    if set(payload.teams_id) == set(get_teams_ids_list_from_response(teams_organizations)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign teams to organization! Assign already exists!")

    for team_id in payload.teams_id:
        if not check_if_teams_ids_in_list_of_response(teams_organizations, team_id):
            team_organization_payload = dict(
                team_id=team_id,
                organization_id=payload.organization_id
            )
            new_team_organization = team_organization_model.TeamOrganization(
                **team_organization_payload)

            db.add(new_team_organization)
            db.commit()
            db.refresh(new_team_organization)

            if not new_team_organization:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign teams to organization! Something went wrong")
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

                users_organizations_query = db.query(
                    user_organization_model.UserOrganization
                ).join(
                    user_model.User, user_model.User.id == user_organization_model.UserOrganization.user_id
                ).filter(
                    user_model.User.tower_id == current_user["user"].tower.id,
                    user_organization_model.UserOrganization.user_id.in_(
                        get_users_ids_list_from_response(users_teams)),
                    user_organization_model.UserOrganization.organization_id == payload.organization_id
                )
                users_organizations = users_organizations_query.all()

                for user_team in users_teams:
                    if not check_if_users_ids_in_list_of_response(users_organizations, user_team.user_id):
                        user_organization_payload = dict(
                            user_id=user_team.user.id,
                            organization_id=payload.organization_id
                        )
                        new_user_organization = user_organization_model.UserOrganization(
                            **user_organization_payload)

                        db.add(new_user_organization)
                        db.commit()
                        db.refresh(new_user_organization)

                        if not new_user_organization:
                            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                detail="Can't assign users to organization! Something went wrong")

    return new_team_organization


@router.get("/{id}/teams", response_model=List[team_organization_schema.TeamsOrganizationResponse])
async def get_teams_organization(
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
    teams_organization_query = db.query(
        team_organization_model.TeamOrganization
    ).join(
        organization_model.Organization, organization_model.Organization.id == team_organization_model.TeamOrganization.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        team_organization_model.TeamOrganization.organization_id == id
    )

    if skip:
        teams_organization_query = teams_organization_query.offset(skip)

    if limit:
        teams_organization_query = teams_organization_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_organization_query = teams_organization_query.order_by(
                desc(sort))
        else:
            teams_organization_query = teams_organization_query.order_by(sort)
    else:
        teams_organization_query = teams_organization_query.order_by(
            team_organization_model.TeamOrganization.team_organization_id)

    if limit == 1:
        teams_organization = teams_organization_query.first()
    else:
        teams_organization = teams_organization_query.all()

    if not teams_organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_organization


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teams_organizations(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    team_organization_query = db.query(
        team_organization_model.TeamOrganization
    ).filter(
        team_organization_model.TeamOrganization.team_organization_id.in_(
            selected)
    )
    teams_organizations = team_organization_query.all()

    if not teams_organizations or len(teams_organizations) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for team_organization in teams_organizations:
        if team_organization.team.tower.id != current_user["user"].tower.id or team_organization.organization.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    team_organization_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
