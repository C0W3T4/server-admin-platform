import { OrganizationRelationshipProps } from './organization'

export enum CredentialType {
  MACHINE = 'machine',
  SOURCE_CONTROL = 'source_control',
}

export type CredentialDataProps = {
  id: string
  name: string
  description?: string
  username: string
  port: number
  credential_type: CredentialType
  created_at: string
  created_by: string
  last_modified_at: string
  last_modified_by: string
  organization: OrganizationRelationshipProps
}

export interface CredentialRelationshipProps {
  id: string
  name: string
  username: string
}
