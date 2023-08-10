from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import schedule_model, organization_model, user_model, user_organization_model, user_team_model, user_credential_model, credential_model, user_inventory_model, inventory_model, user_group_model, group_model, user_host_model, host_model, user_project_model, project_model, user_template_model, template_model, job_model
from ..schemas import user_schema, dashboard_schema
from ..database.connection import get_db
from app.utils.get_ids import get_ids_list, get_templates_ids_list_from_response
from ..auth import oauth2

router = APIRouter(
    prefix="/api/dashboards",
    tags=['Dashboards']
)


@router.get("/totals", response_model=dashboard_schema.DashboardTotalsResponse)
async def get_dashboards_totals(
    db: Session = Depends(get_db),
    current_user: user_schema.CurrentUserResponse = Depends(
        oauth2.get_current_user)
):
    users_query = db.query(
        user_model.User
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id
    )
    users = users_query.all()

    user_organizations_query = db.query(
        user_organization_model.UserOrganization
    ).join(
        user_model.User, user_model.User.id == user_organization_model.UserOrganization.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_organization_model.UserOrganization.user_id == current_user["user"].id
    )
    user_organizations = user_organizations_query.all()

    user_teams_query = db.query(
        user_team_model.UserTeam
    ).join(
        user_model.User, user_model.User.id == user_team_model.UserTeam.user_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        user_team_model.UserTeam.user_id == current_user["user"].id
    )
    user_teams = user_teams_query.all()

    user_credentials_query = db.query(
        user_credential_model.UserCredential
    ).join(
        user_model.User, user_model.User.id == user_credential_model.UserCredential.user_id
    ).join(
        credential_model.Credential, credential_model.Credential.id == user_credential_model.UserCredential.credential_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        credential_model.Credential.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_credential_model.UserCredential.user_id == current_user["user"].id
    )
    user_credentials = user_credentials_query.all()

    user_inventories_query = db.query(
        user_inventory_model.UserInventory
    ).join(
        user_model.User, user_model.User.id == user_inventory_model.UserInventory.user_id
    ).join(
        inventory_model.Inventory, inventory_model.Inventory.id == user_inventory_model.UserInventory.inventory_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        inventory_model.Inventory.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_inventory_model.UserInventory.user_id == current_user["user"].id
    )
    user_inventories = user_inventories_query.all()

    user_groups_query = db.query(
        user_group_model.UserGroup
    ).join(
        user_model.User, user_model.User.id == user_group_model.UserGroup.user_id
    ).join(
        group_model.Group, group_model.Group.id == user_group_model.UserGroup.group_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        group_model.Group.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_group_model.UserGroup.user_id == current_user["user"].id
    )
    user_groups = user_groups_query.all()

    user_hosts_query = db.query(
        user_host_model.UserHost
    ).join(
        user_model.User, user_model.User.id == user_host_model.UserHost.user_id
    ).join(
        host_model.Host, host_model.Host.id == user_host_model.UserHost.host_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        host_model.Host.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_host_model.UserHost.user_id == current_user["user"].id
    )
    user_hosts = user_hosts_query.all()

    user_projects_query = db.query(
        user_project_model.UserProject
    ).join(
        user_model.User, user_model.User.id == user_project_model.UserProject.user_id
    ).join(
        project_model.Project, project_model.Project.id == user_project_model.UserProject.project_id
    ).filter(
        user_model.User.tower_id == current_user["user"].tower.id,
        project_model.Project.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        user_project_model.UserProject.user_id == current_user["user"].id
    )
    user_projects = user_projects_query.all()

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
        user_template_model.UserTemplate.user_id == current_user["user"].id
    )
    user_templates = user_templates_query.all()

    schedules_query = db.query(
        schedule_model.Schedule
    ).join(
        organization_model.Organization, organization_model.Organization.id == schedule_model.Schedule.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        schedule_model.Schedule.organization_id.in_(
            get_ids_list(current_user['organizations']))
    )
    schedules = schedules_query.all()

    jobs_query = db.query(
        job_model.Job
    ).join(
        template_model.Template, template_model.Template.id == job_model.Job.template_id
    ).join(
        organization_model.Organization, organization_model.Organization.id == job_model.Job.organization_id
    ).filter(
        organization_model.Organization.tower_id == current_user["user"].tower.id,
        job_model.Job.organization_id.in_(
            get_ids_list(current_user['organizations'])),
        job_model.Job.template_id.in_(
            get_templates_ids_list_from_response(user_templates))
    )
    jobs = jobs_query.all()

    return {
        "total_users": len(users),
        "total_teams": len(user_teams),
        "total_organizations": len(user_organizations),
        "total_credentials": len(user_credentials),
        "total_inventories": len(user_inventories),
        "total_groups": len(user_groups),
        "total_hosts": len(user_hosts),
        "total_projects": len(user_projects),
        "total_templates": len(user_templates),
        "total_schedules": len(schedules),
        "total_jobs": len(jobs)
    }
