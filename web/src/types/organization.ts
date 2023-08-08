import { TowerRelationshipProps } from './tower'

export type OrganizationDataProps = {
  id: string
  name: string
  description?: string
  created_at: string
  created_by: string
  last_modified_at: string
  last_modified_by: string
  tower: TowerRelationshipProps
}

export interface OrganizationRelationshipProps {
  id: string
  name: string
  tower_id: string
}
