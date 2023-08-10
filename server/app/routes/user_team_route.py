from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.check_value_exists import check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_users_ids_list_from_response
from ..models import user_team_model, user_model, team_model
from ..schemas import common_schema, user_schema, user_team_schema, team_schema
from ..database.connection import get_db
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/users-teams",
    tags=['Users | Teams assigns']
)


@router.get("", response_model=List[team_schema.TeamResponse])
async def get_users_teams(
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
    my_teams: list = []

    users_teams_query = db.query(
        user_team_model.UserTeam
    ).join(
        user_model.User, user_model.User.id == user_team_model.UserTeam.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_team_model.UserTeam.user_id == current_user["user"].id
    )

    if skip:
        users_teams_query = users_teams_query.offset(skip)

    if limit:
        users_teams_query = users_teams_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_teams_query = users_teams_query.order_by(desc(sort))
        else:
            users_teams_query = users_teams_query.order_by(sort)
    else:
        users_teams_query = users_teams_query.order_by(
            user_team_model.UserTeam.user_team_id)

    if limit == 1:
        users_teams = users_teams_query.first()
    else:
        users_teams = users_teams_query.all()

    if not users_teams:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")
    else:
        for user_team in users_teams:
            my_teams.append(user_team.team)

    return my_teams


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_team_schema.UserTeamResponse)
async def create_users_teams(
    payload: user_team_schema.UserTeamPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.users_id or not payload.team_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign users to team! Provide a valid request")

    users_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id.in_(payload.users_id)
    )
    users = users_query.all()
    if not users or len(users) != len(payload.users_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to team! Provide a valid user")

    team_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id == payload.team_id
    )
    team = team_query.first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to team! Provide a valid team")

    users_teams_query = db.query(
        user_team_model.UserTeam
    ).join(
        user_model.User, user_model.User.id == user_team_model.UserTeam.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_team_model.UserTeam.user_id.in_(payload.users_id),
        user_team_model.UserTeam.team_id == payload.team_id
    )
    users_teams = users_teams_query.all()

    if set(payload.users_id) == set(get_users_ids_list_from_response(users_teams)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign users to team! Assign already exists!")

    for user_id in payload.users_id:
        if not check_if_users_ids_in_list_of_response(users_teams, user_id):
            user_team_payload = dict(
                user_id=user_id,
                team_id=payload.team_id
            )

            new_user_team = user_team_model.UserTeam(**user_team_payload)

            db.add(new_user_team)
            db.commit()
            db.refresh(new_user_team)

            if not new_user_team:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign users to team! Something went wrong")

    return new_user_team


@router.get("/{id}/users", response_model=List[user_team_schema.UsersTeamResponse])
async def get_users_team(
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
    users_team_query = db.query(
        user_team_model.UserTeam
    ).join(
        user_model.User, user_model.User.id == user_team_model.UserTeam.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_team_model.UserTeam.team_id == id
    )

    if skip:
        users_team_query = users_team_query.offset(skip)

    if limit:
        users_team_query = users_team_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_team_query = users_team_query.order_by(desc(sort))
        else:
            users_team_query = users_team_query.order_by(sort)
    else:
        users_team_query = users_team_query.order_by(
            user_team_model.UserTeam.user_team_id)

    if limit == 1:
        users_team = users_team_query.first()
    else:
        users_team = users_team_query.all()

    if not users_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_team


@router.get("/{id}/teams", response_model=List[user_team_schema.UserTeamsResponse])
async def get_user_teams(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    user_teams_query = db.query(
        user_team_model.UserTeam
    ).join(
        user_model.User, user_model.User.id == user_team_model.UserTeam.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_team_model.UserTeam.user_id == id
    )

    if skip:
        user_teams_query = user_teams_query.offset(skip)

    if limit:
        user_teams_query = user_teams_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            user_teams_query = user_teams_query.order_by(desc(sort))
        else:
            user_teams_query = user_teams_query.order_by(sort)
    else:
        user_teams_query = user_teams_query.order_by(
            user_team_model.UserTeam.user_team_id)

    if limit == 1:
        user_teams = user_teams_query.first()
    else:
        user_teams = user_teams_query.all()

    if not user_teams:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return user_teams


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_teams(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    user_team_query = db.query(
        user_team_model.UserTeam
    ).filter(
        user_team_model.UserTeam.user_team_id.in_(selected)
    )
    users_teams = user_team_query.all()

    if not users_teams or len(users_teams) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for user_team in users_teams:
        if user_team.user.tower.id != current_user["user"].tower.id or user_team.team.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    user_team_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
