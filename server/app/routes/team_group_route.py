from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import team_group_model, group_model, organization_model, team_model, user_team_model, user_model, user_group_model
from ..schemas import common_schema, user_schema, team_group_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_teams_ids_in_list_of_response, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_teams_ids_list_from_response, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/teams-groups",
    tags=['Teams | Groups assigns']
)


@router.get("", response_model=List[team_group_schema.TeamGroupResponse])
async def get_teams_groups(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    teams_groups_query = db.query(
        team_group_model.TeamGroup
    ).join(
        team_model.Team, team_model.Team.id == team_group_model.TeamGroup.team_id
    ).join(
        group_model.Group, group_model.Group.id == team_group_model.TeamGroup.group_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        teams_groups_query = teams_groups_query.offset(skip)

    if limit:
        teams_groups_query = teams_groups_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_groups_query = teams_groups_query.order_by(desc(sort))
        else:
            teams_groups_query = teams_groups_query.order_by(sort)
    else:
        teams_groups_query = teams_groups_query.order_by(
            team_group_model.TeamGroup.team_group_id)

    if limit == 1:
        teams_groups = teams_groups_query.first()
    else:
        teams_groups = teams_groups_query.all()

    if not teams_groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_groups


@router.post("", status_code=status.HTTP_201_CREATED, response_model=team_group_schema.TeamGroupResponse)
async def create_teams_groups(
    payload: team_group_schema.TeamGroupPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.teams_id or not payload.group_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign teams to group! Provide a valid request")

    teams_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id.in_(payload.teams_id)
    )
    teams = teams_query.all()
    if not teams or len(teams) != len(payload.teams_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to group! Provide a valid team")

    group_query = db.query(
        group_model.Group
    ).join(
        organization_model.Organization, organization_model.Organization.id == group_model.Group.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        group_model.Group.id == payload.group_id
    )
    group = group_query.first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to group! Provide a valid group")

    if not check_if_in_list_of_dict(current_user['organizations'], group.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    teams_groups_query = db.query(
        team_group_model.TeamGroup
    ).join(
        team_model.Team, team_model.Team.id == team_group_model.TeamGroup.team_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_group_model.TeamGroup.team_id.in_(payload.teams_id),
        team_group_model.TeamGroup.group_id == payload.group_id
    )
    teams_groups = teams_groups_query.all()

    if set(payload.teams_id) == set(get_teams_ids_list_from_response(teams_groups)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign teams to group! Assign already exists!")

    for team_id in payload.teams_id:
        if not check_if_teams_ids_in_list_of_response(teams_groups, team_id):
            team_group_payload = dict(
                team_id=team_id,
                group_id=payload.group_id
            )
            new_team_group = team_group_model.TeamGroup(**team_group_payload)

            db.add(new_team_group)
            db.commit()
            db.refresh(new_team_group)

            if not new_team_group:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign teams to group! Something went wrong")
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

                users_groups_query = db.query(
                    user_group_model.UserGroup
                ).join(
                    user_model.User, user_model.User.id == user_group_model.UserGroup.user_id
                ).filter(
                    user_model.User.tower_id == current_user["user"].tower.id,
                    user_group_model.UserGroup.user_id.in_(
                        get_users_ids_list_from_response(users_teams)),
                    user_group_model.UserGroup.group_id == payload.group_id
                )
                users_groups = users_groups_query.all()

                for user_team in users_teams:
                    if not check_if_users_ids_in_list_of_response(users_groups, user_team.user_id):
                        user_group_payload = dict(
                            user_id=user_team.user.id,
                            group_id=payload.group_id
                        )
                        new_user_group = user_group_model.UserGroup(
                            **user_group_payload)

                        db.add(new_user_group)
                        db.commit()
                        db.refresh(new_user_group)

                        if not new_user_group:
                            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                detail="Can't assign users to group! Something went wrong")

    return new_team_group


@router.get("/{id}/teams", response_model=List[team_group_schema.TeamsGroupResponse])
async def get_teams_group(
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
    teams_group_query = db.query(
        team_group_model.TeamGroup
    ).join(
        team_model.Team, team_model.Team.id == team_group_model.TeamGroup.team_id
    ).join(
        group_model.Group, group_model.Group.id == team_group_model.TeamGroup.group_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        team_group_model.TeamGroup.group_id == id
    )

    if skip:
        teams_group_query = teams_group_query.offset(skip)

    if limit:
        teams_group_query = teams_group_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_group_query = teams_group_query.order_by(desc(sort))
        else:
            teams_group_query = teams_group_query.order_by(sort)
    else:
        teams_group_query = teams_group_query.order_by(
            team_group_model.TeamGroup.team_group_id)

    if limit == 1:
        teams_group = teams_group_query.first()
    else:
        teams_group = teams_group_query.all()

    if not teams_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_group


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teams_groups(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    team_group_query = db.query(
        team_group_model.TeamGroup
    ).filter(
        team_group_model.TeamGroup.team_group_id.in_(selected)
    )
    teams_groups = team_group_query.all()

    if not teams_groups or len(teams_groups) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for team_group in teams_groups:
        if not check_if_in_list_of_dict(current_user['organizations'], team_group.group.organization.id) or team_group.team.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    team_group_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
