from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import team_template_model, template_model, organization_model, team_model, user_team_model, user_model, user_template_model
from ..schemas import common_schema, user_schema, team_template_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_teams_ids_in_list_of_response, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_teams_ids_list_from_response, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/teams-templates",
    tags=['Teams | Templates assigns']
)


@router.get("", response_model=List[team_template_schema.TeamTemplateResponse])
async def get_teams_templates(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    teams_templates_query = db.query(
        team_template_model.TeamTemplate
    ).join(
        team_model.Team, team_model.Team.id == team_template_model.TeamTemplate.team_id
    ).join(
        template_model.Template, template_model.Template.id == team_template_model.TeamTemplate.template_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        teams_templates_query = teams_templates_query.offset(skip)

    if limit:
        teams_templates_query = teams_templates_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_templates_query = teams_templates_query.order_by(desc(sort))
        else:
            teams_templates_query = teams_templates_query.order_by(sort)
    else:
        teams_templates_query = teams_templates_query.order_by(
            team_template_model.TeamTemplate.team_template_id)

    if limit == 1:
        teams_templates = teams_templates_query.first()
    else:
        teams_templates = teams_templates_query.all()

    if not teams_templates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_templates


@router.post("", status_code=status.HTTP_201_CREATED, response_model=team_template_schema.TeamTemplateResponse)
async def create_teams_templates(
    payload: team_template_schema.TeamTemplatePostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.teams_id or not payload.template_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign teams to template! Provide a valid request")

    teams_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id.in_(payload.teams_id)
    )
    teams = teams_query.all()
    if not teams or len(teams) != len(payload.teams_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to template! Provide a valid team")

    template_query = db.query(
        template_model.Template
    ).join(
        organization_model.Organization, organization_model.Organization.id == template_model.Template.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        template_model.Template.id == payload.template_id
    )
    template = template_query.first()
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to template! Provide a valid template")

    if not check_if_in_list_of_dict(current_user['organizations'], template.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    teams_templates_query = db.query(
        team_template_model.TeamTemplate
    ).join(
        team_model.Team, team_model.Team.id == team_template_model.TeamTemplate.team_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_template_model.TeamTemplate.team_id.in_(payload.teams_id),
        team_template_model.TeamTemplate.template_id == payload.template_id
    )
    teams_templates = teams_templates_query.all()

    if set(payload.teams_id) == set(get_teams_ids_list_from_response(teams_templates)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign teams to template! Assign already exists!")

    for team_id in payload.teams_id:
        if not check_if_teams_ids_in_list_of_response(teams_templates, team_id):
            team_template_payload = dict(
                team_id=team_id,
                template_id=payload.template_id
            )
            new_team_template = team_template_model.TeamTemplate(
                **team_template_payload)

            db.add(new_team_template)
            db.commit()
            db.refresh(new_team_template)

            if not new_team_template:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign teams to template! Something went wrong")
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

                users_templates_query = db.query(
                    user_template_model.UserTemplate
                ).join(
                    user_model.User, user_model.User.id == user_template_model.UserTemplate.user_id
                ).filter(
                    user_model.User.tower_id == current_user["user"].tower.id,
                    user_template_model.UserTemplate.user_id.in_(
                        get_users_ids_list_from_response(users_teams)),
                    user_template_model.UserTemplate.template_id == payload.template_id
                )
                users_templates = users_templates_query.all()

                for user_team in users_teams:
                    if not check_if_users_ids_in_list_of_response(users_templates, user_team.user_id):
                        user_template_payload = dict(
                            user_id=user_team.user.id,
                            template_id=payload.template_id
                        )
                        new_user_template = user_template_model.UserTemplate(
                            **user_template_payload)

                        db.add(new_user_template)
                        db.commit()
                        db.refresh(new_user_template)

                        if not new_user_template:
                            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                detail="Can't assign users to template! Something went wrong")

    return new_team_template


@router.get("/{id}/teams", response_model=List[team_template_schema.TeamsTemplateResponse])
async def get_teams_template(
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
    teams_template_query = db.query(
        team_template_model.TeamTemplate
    ).join(
        team_model.Team, team_model.Team.id == team_template_model.TeamTemplate.team_id
    ).join(
        template_model.Template, template_model.Template.id == team_template_model.TeamTemplate.template_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        team_template_model.TeamTemplate.template_id == id
    )

    if skip:
        teams_template_query = teams_template_query.offset(skip)

    if limit:
        teams_template_query = teams_template_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_template_query = teams_template_query.order_by(desc(sort))
        else:
            teams_template_query = teams_template_query.order_by(sort)
    else:
        teams_template_query = teams_template_query.order_by(
            team_template_model.TeamTemplate.team_template_id)

    if limit == 1:
        teams_template = teams_template_query.first()
    else:
        teams_template = teams_template_query.all()

    if not teams_template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_template


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teams_templates(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    team_template_query = db.query(
        team_template_model.TeamTemplate
    ).filter(
        team_template_model.TeamTemplate.team_template_id.in_(selected)
    )
    teams_templates = team_template_query.all()

    if not teams_templates or len(teams_templates) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for team_template in teams_templates:
        if not check_if_in_list_of_dict(current_user['organizations'], team_template.template.organization.id) or team_template.team.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    team_template_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
