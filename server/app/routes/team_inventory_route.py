from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import team_inventory_model, inventory_model, organization_model, team_model, user_team_model, user_model, user_inventory_model
from ..schemas import common_schema, user_schema, team_inventory_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_teams_ids_in_list_of_response, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_teams_ids_list_from_response, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/teams-inventories",
    tags=['Teams | Inventories assigns']
)


@router.get("", response_model=List[team_inventory_schema.TeamInventoryResponse])
async def get_teams_inventories(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    teams_inventories_query = db.query(
        team_inventory_model.TeamInventory
    ).join(
        team_model.Team, team_model.Team.id == team_inventory_model.TeamInventory.team_id
    ).join(
        inventory_model.Inventory, inventory_model.Inventory.id == team_inventory_model.TeamInventory.inventory_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        teams_inventories_query = teams_inventories_query.offset(skip)

    if limit:
        teams_inventories_query = teams_inventories_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_inventories_query = teams_inventories_query.order_by(
                desc(sort))
        else:
            teams_inventories_query = teams_inventories_query.order_by(sort)
    else:
        teams_inventories_query = teams_inventories_query.order_by(
            team_inventory_model.TeamInventory.team_inventory_id)

    if limit == 1:
        teams_inventories = teams_inventories_query.first()
    else:
        teams_inventories = teams_inventories_query.all()

    if not teams_inventories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_inventories


@router.post("", status_code=status.HTTP_201_CREATED, response_model=team_inventory_schema.TeamInventoryResponse)
async def create_teams_inventories(
    payload: team_inventory_schema.TeamInventoryPostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.teams_id or not payload.inventory_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign teams to inventory! Provide a valid request")

    teams_query = db.query(
        team_model.Team
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_model.Team.id.in_(payload.teams_id)
    )
    teams = teams_query.all()
    if not teams or len(teams) != len(payload.teams_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to inventory! Provide a valid team")

    inventory_query = db.query(
        inventory_model.Inventory
    ).join(
        organization_model.Organization, organization_model.Organization.id == inventory_model.Inventory.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.id == payload.inventory_id
    )
    inventory = inventory_query.first()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign teams to inventory! Provide a valid inventory")

    if not check_if_in_list_of_dict(current_user['organizations'], inventory.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    teams_inventories_query = db.query(
        team_inventory_model.TeamInventory
    ).join(
        team_model.Team, team_model.Team.id == team_inventory_model.TeamInventory.team_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        team_inventory_model.TeamInventory.team_id.in_(payload.teams_id),
        team_inventory_model.TeamInventory.inventory_id == payload.inventory_id
    )
    teams_inventories = teams_inventories_query.all()

    if set(payload.teams_id) == set(get_teams_ids_list_from_response(teams_inventories)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign teams to inventory! Assign already exists!")

    for team_id in payload.teams_id:
        if not check_if_teams_ids_in_list_of_response(teams_inventories, team_id):
            team_inventory_payload = dict(
                team_id=team_id,
                inventory_id=payload.inventory_id
            )
            new_team_inventory = team_inventory_model.TeamInventory(
                **team_inventory_payload)

            db.add(new_team_inventory)
            db.commit()
            db.refresh(new_team_inventory)

            if not new_team_inventory:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign teams to inventory! Something went wrong")
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

                users_inventories_query = db.query(
                    user_inventory_model.UserInventory
                ).join(
                    user_model.User, user_model.User.id == user_inventory_model.UserInventory.user_id
                ).filter(
                    user_model.User.tower_id == current_user["user"].tower.id,
                    user_inventory_model.UserInventory.user_id.in_(
                        get_users_ids_list_from_response(users_teams)),
                    user_inventory_model.UserInventory.inventory_id == payload.inventory_id
                )
                users_inventories = users_inventories_query.all()

                for user_team in users_teams:
                    if not check_if_users_ids_in_list_of_response(users_inventories, user_team.user_id):
                        user_inventory_payload = dict(
                            user_id=user_team.user.id,
                            inventory_id=payload.inventory_id
                        )
                        new_user_inventory = user_inventory_model.UserInventory(
                            **user_inventory_payload)

                        db.add(new_user_inventory)
                        db.commit()
                        db.refresh(new_user_inventory)

                        if not new_user_inventory:
                            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                detail="Can't assign users to inventory! Something went wrong")

    return new_team_inventory


@router.get("/{id}/teams", response_model=List[team_inventory_schema.TeamsInventoryResponse])
async def get_teams_inventory(
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
    teams_inventory_query = db.query(
        team_inventory_model.TeamInventory
    ).join(
        team_model.Team, team_model.Team.id == team_inventory_model.TeamInventory.team_id
    ).join(
        inventory_model.Inventory, inventory_model.Inventory.id == team_inventory_model.TeamInventory.inventory_id
    ).filter(
        team_model.Team.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        team_inventory_model.TeamInventory.inventory_id == id
    )

    if skip:
        teams_inventory_query = teams_inventory_query.offset(skip)

    if limit:
        teams_inventory_query = teams_inventory_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            teams_inventory_query = teams_inventory_query.order_by(desc(sort))
        else:
            teams_inventory_query = teams_inventory_query.order_by(sort)
    else:
        teams_inventory_query = teams_inventory_query.order_by(
            team_inventory_model.TeamInventory.team_inventory_id)

    if limit == 1:
        teams_inventory = teams_inventory_query.first()
    else:
        teams_inventory = teams_inventory_query.all()

    if not teams_inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return teams_inventory


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teams_inventories(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    team_inventory_query = db.query(
        team_inventory_model.TeamInventory
    ).filter(
        team_inventory_model.TeamInventory.team_inventory_id.in_(selected)
    )
    teams_inventories = team_inventory_query.all()

    if not teams_inventories or len(teams_inventories) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for team_inventory in teams_inventories:
        if not check_if_in_list_of_dict(current_user['organizations'], team_inventory.inventory.organization.id) or team_inventory.team.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    team_inventory_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
