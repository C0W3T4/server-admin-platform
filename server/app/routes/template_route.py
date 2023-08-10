from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models import template_model, organization_model, inventory_model, credential_model, project_model, user_model, user_template_model
from ..schemas import template_schema, user_schema, common_schema
from ..database.connection import get_db
from app.utils.get_ids import get_ids_list
from app.utils.check_value_exists import check_if_in_list_of_dict
from ..auth import oauth2

router = APIRouter(
    prefix="/api/templates",
    tags=['Templates']
)


@router.get("", response_model=List[template_schema.TemplateResponse])
async def get_templates(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    templates_query = db.query(
        template_model.Template
    ).join(
        organization_model.Organization, organization_model.Organization.id == template_model.Template.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )

    if search_by_name:
        templates_query = templates_query.filter(
            template_model.Template.name.contains(search_by_name)
        )

    if skip:
        templates_query = templates_query.offset(skip)

    if limit:
        templates_query = templates_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            templates_query = templates_query.order_by(desc(sort))
        else:
            templates_query = templates_query.order_by(sort)
    else:
        templates_query = templates_query.order_by(template_model.Template.id)

    if limit == 1:
        templates = templates_query.first()
    else:
        templates = templates_query.all()

    if not templates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any templates")

    return templates


@router.get("/owner", response_model=List[template_schema.TemplateResponse])
async def get_my_templates(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user),
    limit: Optional[int] = None,
    skip: Optional[int] = 0,
    search_by_name: Optional[str] = "",
    sort: Optional[str] = None,
    sort_dir: Optional[common_schema.SortDir] = None
):
    my_templates_query = db.query(
        template_model.Template
    ).join(
        organization_model.Organization, organization_model.Organization.id == template_model.Template.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        template_model.Template.created_by == current_user['user'].username
    ).distinct(
        template_model.Template.id
    )

    if search_by_name:
        my_templates_query = my_templates_query.filter(
            template_model.Template.name.contains(search_by_name)
        )

    if skip:
        my_templates_query = my_templates_query.offset(skip)

    if limit:
        my_templates_query = my_templates_query.limit(limit)

    if sort:
        if sort_dir == common_schema.SortDir.desc:
            my_templates_query = my_templates_query.order_by(desc(sort))
        else:
            my_templates_query = my_templates_query.order_by(sort)
    else:
        my_templates_query = my_templates_query.order_by(
            template_model.Template.id)

    if limit == 1:
        my_templates = my_templates_query.first()
    else:
        my_templates = my_templates_query.all()

    if not my_templates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot find any templates")

    return my_templates


@router.post("", status_code=status.HTTP_201_CREATED, response_model=template_schema.TemplateResponse)
async def create_template(
    payload: template_schema.TemplateRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.name or not payload.launch_type or not payload.playbook_name or not payload.inventory_id or not payload.project_id or not payload.credential_id or not payload.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can't create template")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot create a template! Provide a valid organization")

    if not check_if_in_list_of_dict(current_user['organizations'], payload.organization_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

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
                            detail="Cannot create a template! Provide a valid inventory")

    credential_query = db.query(
        credential_model.Credential
    ).join(
        organization_model.Organization, organization_model.Organization.id == credential_model.Credential.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        credential_model.Credential.id == payload.credential_id
    )
    credential = credential_query.first()
    if not credential:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot create a template! Provide a valid credential")

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
                            detail="Cannot create a template! Provide a valid project")

    template_query = db.query(
        template_model.Template
    ).join(
        organization_model.Organization, organization_model.Organization.id == template_model.Template.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        template_model.Template.organization_id == payload.organization_id,
        template_model.Template.name == payload.name
    )
    template = template_query.first()
    if template:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Can't create template! Template already exists")

    updated_payload = dict(
        **payload.dict(),
        created_by=current_user["user"].username,
        last_modified_by=current_user["user"].username
    )

    new_template = template_model.Template(**updated_payload)

    db.add(new_template)
    db.commit()
    db.refresh(new_template)

    if not new_template:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Can't create template! Something went wrong")
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
                                    detail="Can't assign user to template! Provide a valid user")

            admin_template_payload = dict(
                user_id=user.id,
                template_id=new_template.id
            )
            new_admin_template = user_template_model.UserTemplate(
                **admin_template_payload)

            db.add(new_admin_template)
            db.commit()
            db.refresh(new_admin_template)

            if not new_admin_template:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Can't assign user to template! Something went wrong")

        user_template_payload = dict(
            user_id=current_user["user"].id,
            template_id=new_template.id
        )
        new_user_template = user_template_model.UserTemplate(
            **user_template_payload)

        db.add(new_user_template)
        db.commit()
        db.refresh(new_user_template)

        if not new_user_template:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Can't assign user to template! Something went wrong")

    return new_template


@router.get("/{id}", response_model=template_schema.TemplateResponse)
async def get_template(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    template_query = db.query(
        template_model.Template
    ).join(
        organization_model.Organization, organization_model.Organization.id == template_model.Template.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        template_model.Template.id == id
    )
    template = template_query.first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

    if not check_if_in_list_of_dict(current_user['organizations'], template.organization.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return template


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    selected: List[int],
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    templates_query = db.query(
        template_model.Template
    ).filter(
        template_model.Template.id.in_(selected)
    )
    templates = templates_query.all()

    if not templates or len(templates) != len(selected):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

    for template in templates:
        if not check_if_in_list_of_dict(current_user['organizations'], template.organization.id) or template.organization.tower.id != current_user["user"].tower.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")

    templates_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=template_schema.TemplateResponse)
async def update_template(
    id: int,
    payload: template_schema.TemplateRequest,
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    if not payload.name or not payload.launch_type or not payload.playbook_name or not payload.inventory_id or not payload.project_id or not payload.credential_id or not payload.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't update template! Provide a valid request")

    if not check_if_in_list_of_dict(current_user['organizations'], payload.organization_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    organization_query = db.query(
        organization_model.Organization
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        organization_model.Organization.id == payload.organization_id
    )
    organization = organization_query.first()
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Can't update a template! Provide a valid organization")

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
                            detail="Can't update a template! Provide a valid inventory")

    credential_query = db.query(
        credential_model.Credential
    ).join(
        organization_model.Organization, organization_model.Organization.id == credential_model.Credential.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        credential_model.Credential.id == payload.credential_id
    )
    credential = credential_query.first()
    if not credential:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cannot create a template! Provide a valid credential")

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
                            detail="Cannot create a template! Provide a valid project")

    template_query = db.query(
        template_model.Template
    ).filter(
        template_model.Template.id == id
    )
    template = template_query.first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

    if not check_if_in_list_of_dict(current_user['organizations'], template.organization.id) or template.organization.tower.id != current_user["user"].tower.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if payload.name != template.name:
        new_template_query = db.query(
            template_model.Template
        ).join(
            organization_model.Organization, organization_model.Organization.id == template_model.Template.organization_id
        ).filter(
            organization_model.Organization.tower_id == current_user["user"].tower.id,
            template_model.Template.organization_id == payload.organization_id,
            template_model.Template.name == payload.name
        )
        new_template = new_template_query.first()
        if new_template:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Can't update template! Template already exists")

    updated_payload = dict(
        **payload.dict(),
        last_modified_by=current_user["user"].username
    )

    template_query.update(
        updated_payload,
        synchronize_session=False
    )

    db.commit()

    updated_template = template_query.first()

    return updated_template
