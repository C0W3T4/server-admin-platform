from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import user_template_model, user_model, template_model, organization_model
from ..schemas import common_schema, user_schema, user_template_schema, template_schema
from ..database.connection import get_db
from app.utils.check_value_exists import check_if_in_list_of_dict, check_if_users_ids_in_list_of_response
from app.utils.get_ids import get_ids_list, get_users_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/assigns/users-templates",
    tags=['Users | Templates assigns']
)


@router.get("", response_model=List[user_template_schema.UserTemplateResponse])
async def get_users_templates(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_templates_query = db.query(
        user_template_model.UserTemplate
    ).join(
        user_model.User, user_model.User.id == user_template_model.UserTemplate.user_id
    ).join(
        template_model.Template, template_model.Template.id == user_template_model.UserTemplate.template_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if skip:
        users_templates_query = users_templates_query.offset(skip)

    if limit:
        users_templates_query = users_templates_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_templates_query = users_templates_query.order_by(desc(sort))
        else:
            users_templates_query = users_templates_query.order_by(sort)
    else:
        users_templates_query = users_templates_query.order_by(
            user_template_model.UserTemplate.user_template_id)

    if limit == 1:
        users_templates = users_templates_query.first()
    else:
        users_templates = users_templates_query.all()

    if not users_templates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_templates


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user_template_schema.UserTemplateResponse)
async def create_users_templates(
    payload: user_template_schema.UserTemplatePostRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.users_id or not payload.template_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't assign users to template! Provide a valid request")

    users_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_model.User.id.in_(payload.users_id)
    )
    users = users_query.all()
    if not users or len(users) != len(payload.users_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't assign users to template! Provide a valid user")

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
                            detail="Can't assign users to template! Provide a valid template")

    if not check_if_in_list_of_dict(current_user['organizations'], template.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    users_templates_query = db.query(
        user_template_model.UserTemplate
    ).join(
        user_model.User, user_model.User.id == user_template_model.UserTemplate.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_template_model.UserTemplate.user_id.in_(payload.users_id),
        user_template_model.UserTemplate.template_id == payload.template_id
    )
    users_templates = users_templates_query.all()

    if set(payload.users_id) == set(get_users_ids_list_from_response(users_templates)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't assign users to template! Assign already exists!")

    for user_id in payload.users_id:
        if not check_if_users_ids_in_list_of_response(users_templates, user_id):
            user_template_payload = dict(
                user_id=user_id,
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

    return new_user_template


@router.get("/{id}/users", response_model=List[user_template_schema.UsersTemplateResponse])
async def get_users_template(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    users_template_query = db.query(
        user_template_model.UserTemplate
    ).join(
        user_model.User, user_model.User.id == user_template_model.UserTemplate.user_id
    ).join(
        template_model.Template, template_model.Template.id == user_template_model.UserTemplate.template_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_template_model.UserTemplate.template_id == id
    )

    if skip:
        users_template_query = users_template_query.offset(skip)

    if limit:
        users_template_query = users_template_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            users_template_query = users_template_query.order_by(desc(sort))
        else:
            users_template_query = users_template_query.order_by(sort)
    else:
        users_template_query = users_template_query.order_by(
            user_template_model.UserTemplate.user_template_id)

    if limit == 1:
        users_template = users_template_query.first()
    else:
        users_template = users_template_query.all()

    if not users_template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")

    return users_template


@router.get("/{id}/templates", response_model=List[template_schema.TemplateResponse])
async def get_user_templates(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_templates: list = []

    user_templates_query = db.query(
        user_template_model.UserTemplate
    ).join(
        user_model.User, user_model.User.id == user_template_model.UserTemplate.user_id
    ).join(
        template_model.Template, template_model.Template.id == user_template_model.UserTemplate.template_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_template_model.UserTemplate.user_id == id
    )

    if skip:
        user_templates_query = user_templates_query.offset(skip)

    if limit:
        user_templates_query = user_templates_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            user_templates_query = user_templates_query.order_by(desc(sort))
        else:
            user_templates_query = user_templates_query.order_by(sort)
    else:
        user_templates_query = user_templates_query.order_by(
            user_template_model.UserTemplate.user_template_id)

    if limit == 1:
        user_templates = user_templates_query.first()
    else:
        user_templates = user_templates_query.all()

    if not user_templates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any assignments")
    else:
        for user_template in user_templates:
            my_templates.append(user_template.template)

    return my_templates


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_templates(
    selected: List[int],
    db: Session = Depends(get_db),
    is_admin: bool = Depends(oauth2.check_if_user_is_administrator),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    users_templates_query = db.query(
        user_template_model.UserTemplate
    ).filter(
        user_template_model.UserTemplate.user_template_id.in_(selected)
    )
    users_templates = users_templates_query.all()

    if not users_templates or len(users_templates) != len(selected):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are some assignments not found")

    for user_template in users_templates:
        if not check_if_in_list_of_dict(current_user['organizations'], user_template.template.organization.id) or user_template.user.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    users_templates_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
