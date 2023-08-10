from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import team_host_model, host_model, organization_model, team_model, user_team_model, user_model, user_host_model
from ..schemas import common_schema, user_schema, team_host_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_teams_ids_in_list_of_response, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_teams_ids_list_from_response, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/teams-hosts",
    tags=['Teams | Hosts assigns']
)


@router.get("", response_model=List[team_host_schema.TeamHostResponse])
async def get_teams_hosts(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    teams_hosts_query = db.query(
        team_host_model.TeamHost
    ).join(
        team_model.Team, team_model.Team.id == team_host_model.TeamHost.team_id
    ).join(
        host_model.Host, host_model.Host.id == team_host_model.TeamHost.host_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        teams_hosts_query = teams_hosts_query.offset(skip)

    if limit:
        teams_hosts_query = teams_hosts_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_hosts_query = teams_hosts_query.order_by(desc(sort))
        else:
            teams_hosts_query = teams_hosts_query.order_by(sort)
    else:
        teams_hosts_query = teams_hosts_query.order_by(
            team_host_model.TeamHost.team_host_id)

    if limit == 1:
        teams_hosts = teams_hosts_query.first()
    else:
        teams_hosts = teams_hosts_query.all()

    if not teams_hosts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_hosts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=team_host_schema.TeamHostResponse)
async def create_teams_hosts(
    payload: team_host_schema.TeamHostPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.teams_id or not payload.host_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign teams to host! Provide a valid request")

    teams_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id.in_(payload.teams_id)
    )
    teams = teams_query.all()
    if not teams or len(teams) != len(payload.teams_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to host! Provide a valid team")

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
                            detail="Can't assign teams to host! Provide a valid host")

    if not check_if_in_list_of_dict(current_user['organizations'], host.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    teams_hosts_query = db.query(
        team_host_model.TeamHost
    ).join(
        team_model.Team, team_model.Team.id == team_host_model.TeamHost.team_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_host_model.TeamHost.team_id.in_(payload.teams_id),
        team_host_model.TeamHost.host_id == payload.host_id
    )
    teams_hosts = teams_hosts_query.all()

    if set(payload.teams_id) == set(get_teams_ids_list_from_response(teams_hosts)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign teams to host! Assign already exists!")

    for team_id in payload.teams_id:
        if not check_if_teams_ids_in_list_of_response(teams_hosts, team_id):
            team_host_payload = dict(
                team_id=team_id,
                host_id=payload.host_id
            )
            new_team_host = team_host_model.TeamHost(**team_host_payload)

            db.add(new_team_host)
            db.commit()
            db.refresh(new_team_host)

            if not new_team_host:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign teams to host! Something went wrong")
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

                users_hosts_query = db.query(
                    user_host_model.UserHost
                ).join(
                    user_model.User, user_model.User.id == user_host_model.UserHost.user_id
                ).filter(
                    user_model.User.tower_id == current_user["user"].tower.id,
                    user_host_model.UserHost.user_id.in_(
                        get_users_ids_list_from_response(users_teams)),
                    user_host_model.UserHost.host_id == payload.host_id
                )
                users_hosts = users_hosts_query.all()

                for user_team in users_teams:
                    if not check_if_users_ids_in_list_of_response(users_hosts, user_team.user_id):
                        user_host_payload = dict(
                            user_id=user_team.user.id,
                            host_id=payload.host_id
                        )
                        new_user_host = user_host_model.UserHost(
                            **user_host_payload)

                        db.add(new_user_host)
                        db.commit()
                        db.refresh(new_user_host)

                        if not new_user_host:
                            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                detail="Can't assign users to host! Something went wrong")

    return new_team_host


@router.get("/{id}/teams", response_model=List[team_host_schema.TeamsHostResponse])
async def get_teams_host(
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
    teams_host_query = db.query(
        team_host_model.TeamHost
    ).join(
        team_model.Team, team_model.Team.id == team_host_model.TeamHost.team_id
    ).join(
        host_model.Host, host_model.Host.id == team_host_model.TeamHost.host_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        team_host_model.TeamHost.host_id == id
    )

    if skip:
        teams_host_query = teams_host_query.offset(skip)

    if limit:
        teams_host_query = teams_host_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_host_query = teams_host_query.order_by(desc(sort))
        else:
            teams_host_query = teams_host_query.order_by(sort)
    else:
        teams_host_query = teams_host_query.order_by(
            team_host_model.TeamHost.team_host_id)

    if limit == 1:
        teams_host = teams_host_query.first()
    else:
        teams_host = teams_host_query.all()

    if not teams_host:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_host


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teams_hosts(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    team_host_query = db.query(
        team_host_model.TeamHost
    ).filter(
        team_host_model.TeamHost.team_host_id.in_(selected)
    )
    teams_hosts = team_host_query.all()

    if not teams_hosts or len(teams_hosts) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for team_host in teams_hosts:
        if not check_if_in_list_of_dict(current_user['organizations'], team_host.host.organization.id) or team_host.team.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    team_host_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
