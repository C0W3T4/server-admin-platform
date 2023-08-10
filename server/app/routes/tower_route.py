from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.services.tower.tower_service import update_company_name
from ..schemas import user_schema, tower_schema
from ..models import tower_model
from ..database.connection import get_db
from ..auth import oauth2

router = APIRouter(
    prefix="/api/towers",
    tags=['Towers']
)


@router.get("/owner", response_model=tower_schema.TowerResponse)
async def get_my_tower(
    db: Session = Depends(get_db),
    is_at_least_auditor: bool = Depends(
        oauth2.check_if_user_is_at_least_auditor),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    my_tower_query = db.query(
        tower_model.Tower
    ).filter(
        tower_model.Tower.id == current_user["user"].tower.id
    )
    my_tower = my_tower_query.first()

    if not my_tower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tower not found")

    return my_tower


@router.put("/owner", response_model=tower_schema.TowerResponse)
async def update_tower(
    payload: tower_schema.TowerBase,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    my_tower: tower_schema.TowerResponse = Depends(oauth2.get_tower)
):
    if not payload.company or not payload.hostname or not payload.ipv4 or not payload.username or not payload.port:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't update tower! Provide a valid request")

    tower_query = db.query(
        tower_model.Tower
    ).filter(
        tower_model.Tower.id == current_user["user"].tower.id
    )
    tower = tower_query.first()
    if not tower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tower not found")

    if payload.company != tower.company:
        new_tower_query = db.query(
            tower_model.Tower
        ).filter(
            tower_model.Tower.company == payload.company
        )
        new_tower = new_tower_query.first()
        if new_tower:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update account! Company already exists!")

        updated_company_name = update_company_name(
            my_tower.company,
            payload.company,
            my_tower.ipv4,
            my_tower.port,
            my_tower.username,
            my_tower.password,
            10
        )
        if not updated_company_name:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't update company name on remote! Something went wrong")

    updated_payload = dict(
        **payload.dict(),
        last_modified_by=current_user["user"].username
    )

    tower_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_tower = tower_query.first()

    return updated_tower
