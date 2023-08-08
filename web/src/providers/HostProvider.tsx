import { DescriptionTwoTone, EditTwoTone } from '@mui/icons-material'
import { FaUsers } from 'react-icons/fa'
import { GiLifeBar } from 'react-icons/gi'
import { MdError, MdOutlineDoneAll } from 'react-icons/md'
import { TbCirclePlus, TbPlugConnectedX, TbUsers } from 'react-icons/tb'
import { MapsProvidersProps } from '../types'
import { HostStatus } from '../types/host'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'

export const hostStatusMap = new Map<HostStatus, MapsProvidersProps>([
  [
    HostStatus.ALIVE,
    {
      label: 'enums.hostStatus.alive',
      icon: <GiLifeBar size={16} color="#9e9e9e" className="icon-container" />,
    },
  ],
  [
    HostStatus.SUCCESSFUL,
    {
      label: 'enums.hostStatus.successful',
      icon: (
        <MdOutlineDoneAll
          size={16}
          color="#17c13e"
          className="icon-container"
        />
      ),
    },
  ],
  [
    HostStatus.FAILED,
    {
      label: 'enums.hostStatus.failed',
      icon: <MdError size={16} color="#d9534f" className="icon-container" />,
    },
  ],
  [
    HostStatus.UNREACHABLE,
    {
      label: 'enums.hostStatus.unreachable',
      icon: (
        <TbPlugConnectedX
          size={16}
          color="#d9534f"
          className="icon-container"
        />
      ),
    },
  ],
])

export const hostCreateTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.create',
    icon: <TbCirclePlus size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const hostEditTabsOptions: TabsOptionsProps[] = [
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

export const hostDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]

export const hostListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'hostname',
    label: 'hosts.labels.hostname',
    align: 'left',
  },
  {
    id: 'ipv4',
    label: 'hosts.labels.ipv4',
    align: 'left',
  },
  {
    id: 'host_status',
    label: 'hosts.labels.status',
    align: 'left',
  },
]

export const hostUsersListTableHeadCells: HeadCell[] = [
  {
    id: 'user_host_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'username',
    label: 'hosts.labels.username',
    align: 'left',
  },
  {
    id: 'user_type',
    label: 'hosts.labels.userType',
    align: 'left',
  },
]

export const hostTeamsListTableHeadCells: HeadCell[] = [
  {
    id: 'team_host_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'hosts.labels.name',
    align: 'left',
  },
  {
    id: 'description',
    label: 'hosts.labels.description',
    align: 'left',
  },
]
