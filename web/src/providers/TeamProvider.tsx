import { DescriptionTwoTone, EditTwoTone } from '@mui/icons-material'
import { TbCirclePlus, TbUsers } from 'react-icons/tb'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'

export const teamCreateTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.create',
    icon: <TbCirclePlus size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const teamEditTabsOptions: TabsOptionsProps[] = [
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
]

export const teamDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]

export const teamListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'teams.labels.name',
    align: 'left',
  },
  {
    id: 'created_at',
    label: 'teams.labels.createdAt',
    align: 'left',
  },
  {
    id: 'created_by',
    label: 'teams.labels.createdBy',
    align: 'left',
  },
]

export const teamUsersListTableHeadCells: HeadCell[] = [
  {
    id: 'user_team_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'username',
    label: 'teams.labels.username',
    align: 'left',
  },
  {
    id: 'user_type',
    label: 'teams.labels.userType',
    align: 'left',
  },
]
