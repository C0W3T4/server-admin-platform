import { OrganizationRelationshipProps } from './organization'
import { TemplateDataProps } from './template'

export enum JobStatus {
  PENDING = 'pending',
  WAITING = 'waiting',
  RUNNING = 'running',
  SUCCESSFUL = 'successful',
  FAILED = 'failed',
}

export type JobDataProps = {
  id: string
  job_status: JobStatus
  started_at: string
  finished_at: string
  launched_by: string
  output: string
  template: TemplateDataProps
  organization: OrganizationRelationshipProps
}
