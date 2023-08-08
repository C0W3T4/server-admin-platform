import { OrganizationRelationshipProps } from './organization'

export enum HostStatus {
  ALIVE = 'alive',
  SUCCESSFUL = 'successful',
  FAILED = 'failed',
  UNREACHABLE = 'unreachable',
}

export type HostDataProps = {
  id: string
  description?: string
  hostname: string
  ipv4: string
  host_status: HostStatus
  created_at: string
  created_by: string
  last_modified_at: string
  last_modified_by: string
  organization: OrganizationRelationshipProps
}

export interface HostRelationshipProps {
  id: string
  hostname: string
  ipv4: string
  host_status: HostStatus
}
