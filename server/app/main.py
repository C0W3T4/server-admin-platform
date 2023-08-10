from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from .routes import group_route, credential_route, host_route, inventory_route, job_route, organization_route, project_route, team_route, user_route, auth_route, template_route, schedule_route, tower_route, user_team_route, user_organization_route, team_organization_route, user_credential_route, team_credential_route, user_inventory_route, team_inventory_route, user_group_route, user_host_route, team_group_route, team_host_route, group_host_route, inventory_group_route, user_project_route, team_project_route, user_template_route, team_template_route, template_schedule_route, project_schedule_route, inventory_schedule_route, dashboard_route

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(dashboard_route.router)
app.include_router(host_route.router)
app.include_router(tower_route.router)
app.include_router(schedule_route.router)
app.include_router(credential_route.router)
app.include_router(job_route.router)
app.include_router(template_route.router)
app.include_router(template_schedule_route.router)
app.include_router(project_schedule_route.router)
app.include_router(inventory_schedule_route.router)
app.include_router(group_route.router)
app.include_router(group_host_route.router)
app.include_router(inventory_route.router)
app.include_router(inventory_group_route.router)
app.include_router(project_route.router)
app.include_router(auth_route.router)
app.include_router(user_route.router)
app.include_router(user_team_route.router)
app.include_router(user_organization_route.router)
app.include_router(user_credential_route.router)
app.include_router(user_inventory_route.router)
app.include_router(user_group_route.router)
app.include_router(user_host_route.router)
app.include_router(user_project_route.router)
app.include_router(user_template_route.router)
app.include_router(team_route.router)
app.include_router(team_organization_route.router)
app.include_router(team_credential_route.router)
app.include_router(team_inventory_route.router)
app.include_router(team_group_route.router)
app.include_router(team_host_route.router)
app.include_router(team_project_route.router)
app.include_router(team_template_route.router)
app.include_router(organization_route.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs/")
