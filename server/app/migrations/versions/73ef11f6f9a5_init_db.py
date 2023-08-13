"""init db

Revision ID: 73ef11f6f9a5
Revises: 
Create Date: 2023-08-10 00:40:26.425851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73ef11f6f9a5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('towers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.Column('hostname', sa.String(), nullable=False),
    sa.Column('ipv4', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('tower_status', sa.Enum('alive', 'unreachable', name='tower_status'), server_default=sa.text("'alive'"), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('company')
    )
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('tower_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('tower_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('roles', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('user_type', sa.Enum('normal_user', 'system_auditor', 'system_administrator', 'admin', name='user_type'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('tower_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tower_id'], ['towers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('credentials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('credential_type', sa.Enum('machine', 'source_control', name='credential_type'), nullable=False),
    sa.Column('ssh_key', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hosts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('hostname', sa.String(), nullable=False),
    sa.Column('ipv4', sa.String(), nullable=False),
    sa.Column('host_status', sa.Enum('alive', 'successful', 'failed', 'unreachable', name='host_status'), server_default=sa.text("'alive'"), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('inventory_status', sa.Enum('successful', 'disabled', 'error', name='inventory_status'), server_default=sa.text("'disabled'"), nullable=False),
    sa.Column('inventory_file', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('source_control_credential_type', sa.Enum('manual', 'git', name='source_control_credential_type'), nullable=False),
    sa.Column('tool', sa.Enum('ansible', 'jenkins', 'terraform', 'playwright', name='tool'), nullable=False),
    sa.Column('project_status', sa.Enum('pending', 'waiting', 'running', 'successful', 'failed', 'error', 'canceled', 'never_updated', 'ok', 'missing', name='project_status'), server_default=sa.text("'pending'"), nullable=False),
    sa.Column('source_control_url', sa.String(), nullable=True),
    sa.Column('base_path', sa.String(), nullable=True),
    sa.Column('playbook_directory', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schedules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('schedule_type', sa.Enum('template', 'project', 'inventory', name='schedule_type'), nullable=False),
    sa.Column('start_date_time', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('repeat_frequency', sa.Enum('run_once', 'minute', 'hour', 'day', 'week', 'month', 'year', name='repeat_frequency'), nullable=False),
    sa.Column('every', sa.Integer(), nullable=True),
    sa.Column('week_days', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams_organizations',
    sa.Column('team_organization_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('team_id', 'organization_id')
    )
    op.create_table('users_organizations',
    sa.Column('user_organization_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'organization_id')
    )
    op.create_table('users_teams',
    sa.Column('user_team_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'team_id')
    )
    op.create_table('groups_hosts',
    sa.Column('group_host_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('host_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id', 'host_id')
    )
    op.create_table('inventories_groups',
    sa.Column('inventory_group_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('inventory_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('inventory_id', 'group_id')
    )
    op.create_table('inventories_schedules',
    sa.Column('inventory_schedule_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('cron_job_id', sa.String(), nullable=False),
    sa.Column('inventory_id', sa.Integer(), nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedules.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('inventory_id', 'schedule_id'),
    sa.UniqueConstraint('cron_job_id')
    )
    op.create_table('projects_schedules',
    sa.Column('project_schedule_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('cron_job_id', sa.String(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedules.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('project_id', 'schedule_id'),
    sa.UniqueConstraint('cron_job_id')
    )
    op.create_table('teams_credentials',
    sa.Column('team_credential_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('credential_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['credential_id'], ['credentials.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('team_id', 'credential_id')
    )
    op.create_table('teams_groups',
    sa.Column('team_group_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('team_id', 'group_id')
    )
    op.create_table('teams_hosts',
    sa.Column('team_host_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('host_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('team_id', 'host_id')
    )
    op.create_table('teams_inventories',
    sa.Column('team_inventory_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('inventory_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('team_id', 'inventory_id')
    )
    op.create_table('teams_projects',
    sa.Column('team_project_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('team_id', 'project_id')
    )
    op.create_table('templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('launch_type', sa.Enum('run', 'check', name='launch_type'), server_default=sa.text("'run'"), nullable=False),
    sa.Column('playbook_name', sa.String(), nullable=False),
    sa.Column('limit', sa.String(), nullable=True),
    sa.Column('privilege_escalation', sa.Boolean(), server_default='FALSE', nullable=False),
    sa.Column('verbosity', sa.Enum('0', 'v', 'vv', 'vvv', 'vvvv', 'vvvvv', 'vvvvvv', name='verbosity'), server_default=sa.text("'0'"), nullable=False),
    sa.Column('forks', sa.Integer(), server_default=sa.text('5'), nullable=False),
    sa.Column('extra_vars', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('last_modified_by', sa.String(), nullable=False),
    sa.Column('inventory_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('credential_id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['credential_id'], ['credentials.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_credentials',
    sa.Column('user_credential_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('credential_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['credential_id'], ['credentials.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'credential_id')
    )
    op.create_table('users_groups',
    sa.Column('user_group_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'group_id')
    )
    op.create_table('users_hosts',
    sa.Column('user_host_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('host_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'host_id')
    )
    op.create_table('users_inventories',
    sa.Column('user_inventory_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('inventory_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'inventory_id')
    )
    op.create_table('users_projects',
    sa.Column('user_project_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'project_id')
    )
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_status', sa.Enum('pending', 'waiting', 'running', 'successful', 'failed', name='job_status'), server_default=sa.text("'pending'"), nullable=False),
    sa.Column('started_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('finished_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('launched_by', sa.String(), nullable=False),
    sa.Column('output', sa.String(), nullable=False),
    sa.Column('template_id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams_templates',
    sa.Column('team_template_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('template_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('team_id', 'template_id')
    )
    op.create_table('templates_schedules',
    sa.Column('template_schedule_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('cron_job_id', sa.String(), nullable=False),
    sa.Column('template_id', sa.Integer(), nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedules.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('template_id', 'schedule_id'),
    sa.UniqueConstraint('cron_job_id')
    )
    op.create_table('users_templates',
    sa.Column('user_template_id', sa.Integer(), sa.Identity(always=False, start=1, increment=1, minvalue=1, cycle=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('template_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'template_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_templates')
    op.drop_table('templates_schedules')
    op.drop_table('teams_templates')
    op.drop_table('jobs')
    op.drop_table('users_projects')
    op.drop_table('users_inventories')
    op.drop_table('users_hosts')
    op.drop_table('users_groups')
    op.drop_table('users_credentials')
    op.drop_table('templates')
    op.drop_table('teams_projects')
    op.drop_table('teams_inventories')
    op.drop_table('teams_hosts')
    op.drop_table('teams_groups')
    op.drop_table('teams_credentials')
    op.drop_table('projects_schedules')
    op.drop_table('inventories_schedules')
    op.drop_table('inventories_groups')
    op.drop_table('groups_hosts')
    op.drop_table('users_teams')
    op.drop_table('users_organizations')
    op.drop_table('teams_organizations')
    op.drop_table('schedules')
    op.drop_table('projects')
    op.drop_table('inventories')
    op.drop_table('hosts')
    op.drop_table('groups')
    op.drop_table('credentials')
    op.drop_table('users')
    op.drop_table('teams')
    op.drop_table('organizations')
    op.drop_table('towers')
    # ### end Alembic commands ###