import { OrganizationRelationshipProps } from './organization'

export enum ScheduleType {
  TEMPLATE = 'template',
  PROJECT = 'project',
  INVENTORY = 'inventory',
}

export enum ScheduleRepeatFrequency {
  RUN_ONCE = 'run_once',
  MINUTE = 'minute',
  HOUR = 'hour',
  DAY = 'day',
  WEEK = 'week',
  MONTH = 'month',
  YEAR = 'year',
}

export type ScheduleWeekdays =
  | 'sun'
  | 'mon'
  | 'tue'
  | 'wed'
  | 'thu'
  | 'fri'
  | 'sat'

export type ScheduleDataProps = {
  id: string
  name: string
  description?: string
  schedule_type: ScheduleType
  start_date_time: Date
  repeat_frequency: ScheduleRepeatFrequency
  every?: number
  week_days?: number[]
  created_at: string
  created_by: string
  last_modified_at: string
  last_modified_by: string
  organization: OrganizationRelationshipProps
}

export interface ScheduleRelationshipProps {
  id: string
  name: string
  schedule_type: ScheduleType
}

export type JobsScheduleInfoDataProps = {
  cron_job_id: string
  frequency: number
  frequency_per_hour: number
  frequency_per_day: number
  frequency_per_year: number
  prev_date: Date
  next_date: Date
}
