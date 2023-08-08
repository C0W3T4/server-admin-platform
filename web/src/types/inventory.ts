import { GroupDataProps } from './group'
import { OrganizationRelationshipProps } from './organization'
import { ScheduleDataProps } from './schedule'

export enum InventoryStatus {
  SUCCESSFUL = 'successful',
  DISABLED = 'disabled',
  ERROR = 'error',
}

export type InventoryDataProps = {
  id: string
  name: string
  description?: string
  inventory_file: string
  inventory_status: InventoryStatus
  created_at: string
  created_by: string
  last_modified_at: string
  last_modified_by: string
  organization: OrganizationRelationshipProps
}

export interface InventoryRelationshipProps {
  id: string
  name: string
  inventory_status: InventoryStatus
}

export type InventoryGroupsDataProps = {
  inventory_group_id: string
  group: GroupDataProps
}

export type InventoriesGroupDataProps = {
  inventory_group_id: string
  inventory: InventoryDataProps
}

export type InventorySchedulesDataProps = {
  inventory_schedule_id: string
  cron_job_id: string
  schedule: ScheduleDataProps
}

export type InventoriesScheduleDataProps = {
  inventory_schedule_id: string
  cron_job_id: string
  inventory: InventoryDataProps
}
