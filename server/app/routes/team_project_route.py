from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import team_project_model, project_model, organization_model, team_model, user_team_model, user_model, user_project_model
from ..schemas import common_schema, user_schema, team_project_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_teams_ids_in_list_of_response, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_teams_ids_list_from_response, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/teams-projects",
    tags=['Teams | Projects assigns']
)


@router.get("", response_model=List[team_project_schema.TeamProjectResponse])
async def get_teams_projects(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    teams_projects_query = db.query(
        team_project_model.TeamProject
    ).join(
        team_model.Team, team_model.Team.id == team_project_model.TeamProject.team_id
    ).join(
        project_model.Project, project_model.Project.id == team_project_model.TeamProject.project_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        teams_projects_query = teams_projects_query.offset(skip)

    if limit:
        teams_projects_query = teams_projects_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_projects_query = teams_projects_query.order_by(desc(sort))
        else:
            teams_projects_query = teams_projects_query.order_by(sort)
    else:
        teams_projects_query = teams_projects_query.order_by(
            team_project_model.TeamProject.team_project_id)

    if limit == 1:
        teams_projects = teams_projects_query.first()
    else:
        teams_projects = teams_projects_query.all()

    if not teams_projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_projects


@router.post("", status_code=status.HTTP_201_CREATED, response_model=team_project_schema.TeamProjectResponse)
async def create_teams_projects(
    payload: team_project_schema.TeamProjectPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.teams_id or not payload.project_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign teams to project! Provide a valid request")

    teams_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id.in_(payload.teams_id)
    )
    teams = teams_query.all()
    if not teams or len(teams) != len(payload.teams_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to project! Provide a valid team")

    project_query = db.query(
        project_model.Project
    ).join(
        organization_model.Organization, organization_model.Organization.id == project_model.Project.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        project_model.Project.id == payload.project_id
    )
    project = project_query.first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to project! Provide a valid project")

    if not check_if_in_list_of_dict(current_user['organizations'], project.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    teams_projects_query = db.query(
        team_project_model.TeamProject
    ).join(
        team_model.Team, team_model.Team.id == team_project_model.TeamProject.team_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_project_model.TeamProject.team_id.in_(payload.teams_id),
        team_project_model.TeamProject.project_id == payload.project_id
    )
    teams_projects = teams_projects_query.all()

    if set(payload.teams_id) == set(get_teams_ids_list_from_response(teams_projects)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign teams to project! Assign already exists!")

    for team_id in payload.teams_id:
        if not check_if_teams_ids_in_list_of_response(teams_projects, team_id):
            team_project_payload = dict(
                team_id=team_id,
                project_id=payload.project_id
            )
            new_team_project = team_project_model.TeamProject(
                **team_project_payload)

            db.add(new_team_project)
            db.commit()
            db.refresh(new_team_project)

            if not new_team_project:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign teams to project! Something went wrong")
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

                users_projects_query = db.query(
                    user_project_model.UserProject
                ).join(
                    user_model.User, user_model.User.id == user_project_model.UserProject.user_id
                ).filter(
                    user_model.User.tower_id == current_user["user"].tower.id,
                    user_project_model.UserProject.user_id.in_(
                        get_users_ids_list_from_response(users_teams)),
                    user_project_model.UserProject.project_id == payload.project_id
                )
                users_projects = users_projects_query.all()

                for user_team in users_teams:
                    if not check_if_users_ids_in_list_of_response(users_projects, user_team.user_id):
                        user_project_payload = dict(
                            user_id=user_team.user.id,
                            project_id=payload.project_id
                        )
                        new_user_project = user_project_model.UserProject(
                            **user_project_payload)

                        db.add(new_user_project)
                        db.commit()
                        db.refresh(new_user_project)

                        if not new_user_project:
                            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                detail="Can't assign users to project! Something went wrong")

    return new_team_project


@router.get("/{id}/teams", response_model=List[team_project_schema.TeamsProjectResponse])
async def get_teams_project(
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
    teams_project_query = db.query(
        team_project_model.TeamProject
    ).join(
        team_model.Team, team_model.Team.id == team_project_model.TeamProject.team_id
    ).join(
        project_model.Project, project_model.Project.id == team_project_model.TeamProject.project_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        team_project_model.TeamProject.project_id == id
    )

    if skip:
        teams_project_query = teams_project_query.offset(skip)

    if limit:
        teams_project_query = teams_project_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_project_query = teams_project_query.order_by(desc(sort))
        else:
            teams_project_query = teams_project_query.order_by(sort)
    else:
        teams_project_query = teams_project_query.order_by(
            team_project_model.TeamProject.team_project_id)

    if limit == 1:
        teams_project = teams_project_query.first()
    else:
        teams_project = teams_project_query.all()

    if not teams_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_project


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teams_projects(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    team_project_query = db.query(
        team_project_model.TeamProject
    ).filter(
        team_project_model.TeamProject.team_project_id.in_(selected)
    )
    teams_projects = team_project_query.all()

    if not teams_projects or len(teams_projects) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for team_project in teams_projects:
        if not check_if_in_list_of_dict(current_user['organizations'], team_project.project.organization.id) or team_project.team.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    team_project_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
