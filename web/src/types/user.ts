import {
  OrganizationRelationshipProps,
  OrganizationDataProps,
} from './organization'
import { TeamRelationshipProps } from './team'
import { TowerDataProps, TowerRelationshipProps } from './tower'

export enum UserType {
  NORMAL_USER = 'normal_user',
  SYSTEM_AUDITOR = 'system_auditor',
  SYSTEM_ADMINISTRATOR = 'system_administrator',
  ADMIN = 'admin',
}

export type UserProfile = {
  id: string
  first_name?: string
  last_name?: string
  username: string
  email?: string
  user_type: UserType
  roles?: string[]
  created_at: string
  created_by: string
  last_modified_at: string
  last_modified_by: string
  tower: TowerRelationshipProps
}

export interface UserStateProps {
  user: UserProfile | null | undefined
  error: object | string | null
}

export interface LoginResponseProps {
  user: UserProfile
  teams: TeamRelationshipProps
  organizations: OrganizationRelationshipProps
  access_token: string
  token_type: string
}

export interface RegisterResponseProps {
  tower: TowerDataProps
  user: UserProfile
  organization: OrganizationDataProps
}

export interface UserRelationshipProps {
  id: string
  username: string
}
