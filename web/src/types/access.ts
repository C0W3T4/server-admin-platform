import { ProjectDataProps } from './project'
import { InventoryDataProps } from './inventory'
import { GroupDataProps } from './group'
import { UserProfile } from './user'
import { TeamDataProps } from './team'
import { CredentialDataProps } from './credential'
import { HostDataProps } from './host'
import { TemplateDataProps } from './template'
import { OrganizationDataProps } from './organization'

export type UsersTeamDataProps = {
  user_team_id: string
  user: UserProfile
}

export type UserTeamsDataProps = {
  user_team_id: string
  team: TeamDataProps
}

export type UsersOrganizationDataProps = {
  user_organization_id: string
  user: UserProfile
}

export type UserOrganizationsDataProps = {
  user_organization_id: string
  organization: OrganizationDataProps
}

export type TeamsOrganizationDataProps = {
  team_organization_id: string
  team: TeamDataProps
}

export type UserCredentialDataProps = {
  user_credential_id: string
  user: UserProfile
  credential: CredentialDataProps
}

export type UsersCredentialDataProps = {
  user_credential_id: string
  user: UserProfile
}

export type UserCredentialsDataProps = {
  user_credential_id: string
  credential: CredentialDataProps
}

export type TeamCredentialDataProps = {
  team_credential_id: string
  team: TeamDataProps
  credential: CredentialDataProps
}

export type TeamsCredentialDataProps = {
  team_credential_id: string
  team: TeamDataProps
}

export type TeamCredentialsDataProps = {
  team_credential_id: string
  credential: CredentialDataProps
}

export type UserGroupDataProps = {
  user_group_id: string
  user: UserProfile
  group: GroupDataProps
}

export type UsersGroupDataProps = {
  user_group_id: string
  user: UserProfile
}

export type UserGroupsDataProps = {
  user_group_id: string
  group: GroupDataProps
}

export type TeamGroupDataProps = {
  team_group_id: string
  team: TeamDataProps
  group: GroupDataProps
}

export type TeamsGroupDataProps = {
  team_group_id: string
  team: TeamDataProps
}

export type TeamGroupsDataProps = {
  team_group_id: string
  group: GroupDataProps
}

export type UserHostDataProps = {
  user_host_id: string
  user: UserProfile
  host: HostDataProps
}

export type UsersHostDataProps = {
  user_host_id: string
  user: UserProfile
}

export type UserHostsDataProps = {
  user_host_id: string
  host: HostDataProps
}

export type TeamHostDataProps = {
  team_host_id: string
  team: TeamDataProps
  host: HostDataProps
}

export type TeamsHostDataProps = {
  team_host_id: string
  team: TeamDataProps
}

export type TeamHostsDataProps = {
  team_host_id: string
  host: HostDataProps
}

export type UsersInventoryDataProps = {
  user_inventory_id: string
  user: UserProfile
}

export type UserInventoriesDataProps = {
  user_inventory_id: string
  inventory: InventoryDataProps
}

export type UserInventoryDataProps = {
  user_inventory_id: string
  user: UserProfile
  inventory: InventoryDataProps
}

export type TeamInventoryDataProps = {
  team_inventory_id: string
  team: TeamDataProps
  inventory: InventoryDataProps
}

export type TeamsInventoryDataProps = {
  team_inventory_id: string
  team: TeamDataProps
}

export type TeamInventoriesDataProps = {
  team_inventory_id: string
  inventory: InventoryDataProps
}

export type UsersProjectDataProps = {
  user_project_id: string
  user: UserProfile
}

export type UserProjectsDataProps = {
  user_project_id: string
  project: ProjectDataProps
}

export type UserProjectDataProps = {
  user_project_id: string
  user: UserProfile
  project: ProjectDataProps
}

export type TeamProjectDataProps = {
  team_project_id: string
  team: TeamDataProps
  project: ProjectDataProps
}

export type TeamsProjectDataProps = {
  team_project_id: string
  team: TeamDataProps
}

export type TeamProjectsDataProps = {
  team_project_id: string
  project: ProjectDataProps
}

export type UserTemplateDataProps = {
  user_template_id: string
  user: UserProfile
  template: TemplateDataProps
}

export type UsersTemplateDataProps = {
  user_template_id: string
  user: UserProfile
}

export type UserTemplatesDataProps = {
  user_template_id: string
  template: TemplateDataProps
}

export type TeamTemplateDataProps = {
  team_template_id: string
  team: TeamDataProps
  template: TemplateDataProps
}

export type TeamsTemplateDataProps = {
  team_template_id: string
  team: TeamDataProps
}

export type TeamTemplatesDataProps = {
  team_template_id: string
  template: TemplateDataProps
}
