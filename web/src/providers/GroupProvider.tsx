import { DescriptionTwoTone, EditTwoTone } from '@mui/icons-material'
import { FaUsers } from 'react-icons/fa'
import { TbCirclePlus, TbServer, TbUsers } from 'react-icons/tb'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'

export const groupCreateTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.create',
    icon: <TbCirclePlus size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const groupEditTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.edit',
    icon: <EditTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
  {
    label: 'tabs.labels.users',
    icon: <TbUsers size={16} color="#ec407a" />,
    disabled: false,
  },
  {
    label: 'tabs.labels.teams',
    icon: <FaUsers size={16} color="#ec407a" />,
    disabled: false,
  },
  {
    label: 'tabs.labels.hosts',
    icon: <TbServer size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const groupDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]

export const groupListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'groups.labels.name',
    align: 'left',
  },
  {
    id: 'created_at',
    label: 'groups.labels.createdAt',
    align: 'left',
  },
  {
    id: 'created_by',
    label: 'groups.labels.createdBy',
    align: 'left',
  },
]

export const groupUsersListTableHeadCells: HeadCell[] = [
  {
    id: 'user_group_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'username',
    label: 'groups.labels.username',
    align: 'left',
  },
  {
    id: 'user_type',
    label: 'groups.labels.userType',
    align: 'left',
  },
]

export const groupTeamsListTableHeadCells: HeadCell[] = [
  {
    id: 'team_group_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'groups.labels.name',
    align: 'left',
  },
  {
    id: 'description',
    label: 'groups.labels.description',
    align: 'left',
  },
]

export const groupHostsListTableHeadCells: HeadCell[] = [
  {
    id: 'group_host_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'hostname',
    label: 'groups.labels.hostname',
    align: 'left',
  },
  {
    id: 'ipv4',
    label: 'groups.labels.ipv4',
    align: 'left',
  },
  {
    id: 'host_status',
    label: 'groups.labels.status',
    align: 'left',
  },
]
