import { DescriptionTwoTone, EditTwoTone } from '@mui/icons-material'
import { FaUsers } from 'react-icons/fa'
import { TbCirclePlus, TbUsers } from 'react-icons/tb'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'

export const organizationCreateTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.create',
    icon: <TbCirclePlus size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const organizationEditTabsOptions: TabsOptionsProps[] = [
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
]

export const organizationDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]

export const organizationListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'organizations.labels.name',
    align: 'left',
  },
  {
    id: 'created_at',
    label: 'organizations.labels.createdAt',
    align: 'left',
  },
  {
    id: 'created_by',
    label: 'organizations.labels.createdBy',
    align: 'left',
  },
]

export const organizationUsersListTableHeadCells: HeadCell[] = [
  {
    id: 'user_organization_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'username',
    label: 'organizations.labels.username',
    align: 'left',
  },
  {
    id: 'user_type',
    label: 'organizations.labels.userType',
    align: 'left',
  },
]

export const organizationTeamsListTableHeadCells: HeadCell[] = [
  {
    id: 'team_organization_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'organizations.labels.name',
    align: 'left',
  },
  {
    id: 'description',
    label: 'organizations.labels.description',
    align: 'left',
  },
]
