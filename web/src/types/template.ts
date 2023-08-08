import { CredentialDataProps } from './credential'
import { InventoryDataProps } from './inventory'
import { OrganizationRelationshipProps } from './organization'
import { ProjectDataProps } from './project'
import { ScheduleDataProps } from './schedule'

export enum Verbosity {
  ZERO = '0',
  ONE = 'v',
  TWO = 'vv',
  THREE = 'vvv',
  FOUR = 'vvvv',
  FIVE = 'vvvvv',
  SIX = 'vvvvvv',
}

export enum LaunchType {
  RUN = 'run',
  CHECK = 'check',
}

export type TemplateDataProps = {
  id: string
  name: string
  description?: string
  launch_type: LaunchType
  playbook_name: string
  limit?: string
  privilege_escalation?: boolean
  verbosity?: Verbosity
  forks?: number
  extra_vars?: string
  created_at: string
  created_by: string
  last_modified_at: string
  last_modified_by: string
  inventory: InventoryDataProps
  project: ProjectDataProps
  credential: CredentialDataProps
  organization: OrganizationRelationshipProps
}

export interface TemplateRelationshipProps {
  id: string
  name: string
}

export type TemplateSchedulesDataProps = {
  template_schedule_id: string
  cron_job_id: string
  schedule: ScheduleDataProps
}

export type TemplatesScheduleDataProps = {
  template_schedule_id: string
  cron_job_id: string
  template: TemplateDataProps
}
