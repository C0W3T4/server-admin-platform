import { OrganizationRelationshipProps } from './organization'
import { ScheduleDataProps } from './schedule'

export enum ProjectStatus {
  PENDING = 'pending',
  WAITING = 'waiting',
  RUNNING = 'running',
  SUCCESSFUL = 'successful',
  FAILED = 'failed',
  ERROR = 'error',
  CANCELED = 'canceled',
  NEVER_UPDATED = 'never_updated',
  OK = 'ok',
  MISSING = 'missing',
}

export enum SourceControlCredentialType {
  MANUAL = 'manual',
  GIT = 'git',
}

export enum Tools {
  ANSIBLE = 'ansible',
  JENKINS = 'jenkins',
  TERRAFORM = 'terraform',
  PLAYWRIGHT = 'playwright',
}

export type ProjectDataProps = {
  id: string
  name: string
  description?: string
  source_control_credential_type: SourceControlCredentialType
  tool: Tools
  project_status: ProjectStatus
  source_control_url?: string
  base_path?: string
  playbook_directory?: string
  created_at: string
  created_by: string
  last_modified_at: string
  last_modified_by: string
  organization: OrganizationRelationshipProps
}

export interface ProjectRelationshipProps {
  id: string
  name: string
  project_status: ProjectStatus
}

export type ProjectSchedulesDataProps = {
  project_schedule_id: string
  cron_job_id: string
  schedule: ScheduleDataProps
}

export type ProjectsScheduleDataProps = {
  project_schedule_id: string
  cron_job_id: string
  project: ProjectDataProps
}
