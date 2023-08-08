import { DescriptionTwoTone, EditTwoTone } from '@mui/icons-material'
import { AiOutlineAudit } from 'react-icons/ai'
import { FaUsers } from 'react-icons/fa'
import { RiAdminLine, RiUserSettingsLine } from 'react-icons/ri'
import { TbBuilding, TbCirclePlus, TbUser } from 'react-icons/tb'
import { MapsProvidersProps } from '../types'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'
import { UserType } from '../types/user'

export const userTypeMap = new Map<UserType, MapsProvidersProps>([
  [
    UserType.NORMAL_USER,
    {
      label: 'enums.userType.normalUser',
      icon: <TbUser size={16} color="#29b6f6" className="icon-container" />,
    },
  ],
  [
    UserType.SYSTEM_AUDITOR,
    {
      label: 'enums.userType.systemAuditor',
      icon: (
        <AiOutlineAudit size={16} color="#29b6f6" className="icon-container" />
      ),
    },
  ],
  [
    UserType.SYSTEM_ADMINISTRATOR,
    {
      label: 'enums.userType.systemAdmin',
      icon: (
        <RiUserSettingsLine
          size={16}
          color="#29b6f6"
          className="icon-container"
        />
      ),
    },
  ],
  [
    UserType.ADMIN,
    {
      label: 'enums.userType.admin',
      icon: (
        <RiAdminLine size={16} color="#29b6f6" className="icon-container" />
      ),
    },
  ],
])

export const userCreateTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.create',
    icon: <TbCirclePlus size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const userEditTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.edit',
    icon: <EditTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
  {
    label: 'tabs.labels.organizations',
    icon: <TbBuilding size={16} color="#ec407a" />,
    disabled: false,
  },
  {
    label: 'tabs.labels.teams',
    icon: <FaUsers size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const userDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]

export const userListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'username',
    label: 'users.labels.username',
    align: 'left',
  },
  {
    id: 'user_type',
    label: 'users.labels.userType',
    align: 'left',
  },
  {
    id: 'created_at',
    label: 'users.labels.createdAt',
    align: 'left',
  },
  {
    id: 'created_by',
    label: 'users.labels.createdBy',
    align: 'left',
  },
]

export const userOrganizationsListTableHeadCells: HeadCell[] = [
  {
    id: 'user_organization_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'users.labels.name',
    align: 'left',
  },
  {
    id: 'description',
    label: 'users.labels.description',
    align: 'left',
  },
]

export const userTeamsListTableHeadCells: HeadCell[] = [
  {
    id: 'user_team_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'users.labels.name',
    align: 'left',
  },
  {
    id: 'description',
    label: 'users.labels.description',
    align: 'left',
  },
]
