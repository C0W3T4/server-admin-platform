import { DescriptionTwoTone, EditTwoTone } from '@mui/icons-material'
import { FaUsers } from 'react-icons/fa'
import { TbCirclePlus, TbServer, TbUsers } from 'react-icons/tb'
import { VscSourceControl } from 'react-icons/vsc'
import { MapsProvidersProps } from '../types'
import { CredentialType } from '../types/credential'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'

export const credentialTypeMap = new Map<CredentialType, MapsProvidersProps>([
  [
    CredentialType.MACHINE,
    {
      label: 'enums.credentialType.machine',
      icon: <TbServer size={16} color="#29b6f6" className="icon-container" />,
    },
  ],
  [
    CredentialType.SOURCE_CONTROL,
    {
      label: 'enums.credentialType.sourceControl',
      icon: (
        <VscSourceControl
          size={16}
          color="#29b6f6"
          className="icon-container"
        />
      ),
    },
  ],
])

export const credentialCreateTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.create',
    icon: <TbCirclePlus size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const credentialEditTabsOptions: TabsOptionsProps[] = [
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

export const credentialDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]

export const credentialListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'credentials.labels.name',
    align: 'left',
  },
  {
    id: 'username',
    label: 'credentials.labels.username',
    align: 'left',
  },
  {
    id: 'credential_type',
    label: 'credentials.labels.credentialType',
    align: 'left',
  },
]

export const credentialUsersListTableHeadCells: HeadCell[] = [
  {
    id: 'user_credential_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'username',
    label: 'credentials.labels.username',
    align: 'left',
  },
  {
    id: 'user_type',
    label: 'credentials.labels.userType',
    align: 'left',
  },
]

export const credentialTeamsListTableHeadCells: HeadCell[] = [
  {
    id: 'team_credential_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'credentials.labels.name',
    align: 'left',
  },
  {
    id: 'description',
    label: 'credentials.labels.description',
    align: 'left',
  },
]
