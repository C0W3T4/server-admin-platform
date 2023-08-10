from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import team_model, user_model, user_team_model
from ..schemas import team_schema, user_schema, common_schema
from ..auth import oauth2
from ..database.connection import get_db

router = APIRouter(
    prefix="/api/teams",
    tags=['Teams']
)


@router.get("", response_model=List[team_schema.TeamResponse])
async def get_teams(
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    teams_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id
    )

    if search_by_name:
        teams_query = teams_query.filter(
            team_model.Team.name.contains(search_by_name)
        )

    if skip:
        teams_query = teams_query.offset(skip)

    if limit:
        teams_query = teams_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_query = teams_query.order_by(desc(sort))
        else:
            teams_query = teams_query.order_by(sort)
    else:
        teams_query = teams_query.order_by(team_model.Team.id)

    if limit == 1:
        teams = teams_query.first()
    else:
        teams = teams_query.all()

    if not teams:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find any teams")

    return teams


@router.get("/owner", response_model=List[team_schema.TeamResponse])
async def get_my_teams(
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    teams_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.created_by == current_user["user"].username
    )

    if search_by_name:
        teams_query = teams_query.filter(
            team_model.Team.name.contains(search_by_name)
        )

    if skip:
        teams_query = teams_query.offset(skip)

    if limit:
        teams_query = teams_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_query = teams_query.order_by(desc(sort))
        else:
            teams_query = teams_query.order_by(sort)
    else:
        teams_query = teams_query.order_by(team_model.Team.id)

    if limit == 1:
        teams = teams_query.first()
    else:
        teams = teams_query.all()

    if not teams:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find any teams")

    return teams


@router.post("", status_code=status.HTTP_201_CREATED, response_model=team_schema.TeamResponse)
async def create_team(
    payload: team_schema.TeamRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't create team! Provide a valid request")

    team_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.name == payload.name
    )
    team = team_query.first()

    if team:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create team! Team already exists!")

    updated_payload = dict(
        **payload.dict(),
        tower_id=current_user["user"].tower.id,
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    new_team = team_model.Team(**updated_payload)

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    if not new_team:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create team! Something went wrong")
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
                                    detail="Can't assign user to team! Provide a valid user")

            admin_team_payload = dict(
                user_id=user.id,
                team_id=new_team.id
            )
            new_admin_team = user_team_model.UserTeam(**admin_team_payload)

            db.add(new_admin_team)
            db.commit()
            db.refresh(new_admin_team)

            if not new_admin_team:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign user to team! Something went wrong")

        user_team_payload = dict(
            user_id=current_user["user"].id,
            team_id=new_team.id
        )
        new_user_team = user_team_model.UserTeam(**user_team_payload)

        db.add(new_user_team)
        db.commit()
        db.refresh(new_user_team)

        if not new_user_team:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't assign user to team! Something went wrong")

    return new_team


@router.get("/{id}", response_model=team_schema.TeamResponse)
async def get_team(
    id: int,
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    team_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id == id
    )
    team = team_query.first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    return team


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    team_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id.in_(selected)
    )
    teams = team_query.all()

    if not teams or len(teams) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some teams not found")

    team_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=team_schema.TeamResponse)
async def update_team(
    id: int,
    payload: team_schema.TeamRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't update team! Provide a valid request")

    team_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id == id
    )
    team = team_query.first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    updated_payload = dict(
        **payload.dict(),
        tower_id=team.tower.id,
        created_by=team.created_by,
        last_modified_by=current_user["user"].username
    )

    team_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_team = team_query.first()

    return updated_team
