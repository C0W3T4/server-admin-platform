export enum TowerStatus {
  ALIVE = 'alive',
  UNREACHABLE = 'unreachable',
}

export type TowerDataProps = {
  id: string
  company: string
  hostname: string
  ipv4: string
  username: string
  port: number
  tower_status: TowerStatus
  created_at: string
  last_modified_at: string
  created_by: string
  last_modified_by: string
}

export type TowerRelationshipProps = {
  id: string
  company: string
}
