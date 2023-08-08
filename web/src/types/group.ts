import { HostDataProps } from './host'
import { OrganizationRelationshipProps } from './organization'

export type GroupDataProps = {
  id: string
  name: string
  description?: string
  created_at: string
  created_by: string
  last_modified_at: string
  last_modified_by: string
  organization: OrganizationRelationshipProps
}

export interface GroupRelationshipProps {
  id: string
  name: string
}

export type GroupHostsDataProps = {
  group_host_id: string
  host: HostDataProps
}

export type GroupsHostDataProps = {
  group_host_id: string
  group: GroupDataProps
}
