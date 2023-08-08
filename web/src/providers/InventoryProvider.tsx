import { DescriptionTwoTone, EditTwoTone } from '@mui/icons-material'
import { FaUsers } from 'react-icons/fa'
import { IoMdGitNetwork } from 'react-icons/io'
import { MdOutlineDoneAll, MdSyncDisabled } from 'react-icons/md'
import { TbCalendarTime, TbCirclePlus, TbUsers } from 'react-icons/tb'
import { VscError } from 'react-icons/vsc'
import { MapsProvidersProps } from '../types'
import { InventoryStatus } from '../types/inventory'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'

export const inventoryStatusMap = new Map<InventoryStatus, MapsProvidersProps>([
  [
    InventoryStatus.SUCCESSFUL,
    {
      label: 'enums.inventoryStatus.successful',
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
    InventoryStatus.DISABLED,
    {
      label: 'enums.inventoryStatus.disabled',
      icon: (
        <MdSyncDisabled size={16} color="#9e9e9e" className="icon-container" />
      ),
    },
  ],
  [
    InventoryStatus.ERROR,
    {
      label: 'enums.inventoryStatus.error',
      icon: <VscError size={16} color="#d9534f" className="icon-container" />,
    },
  ],
])

export const inventoryCreateTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.create',
    icon: <TbCirclePlus size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const inventoryEditTabsOptions: TabsOptionsProps[] = [
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
    label: 'tabs.labels.groups',
    icon: <IoMdGitNetwork size={16} color="#ec407a" />,
    disabled: false,
  },
  {
    label: 'tabs.labels.schedules',
    icon: <TbCalendarTime size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const inventoryDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]

export const inventoryListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'inventories.labels.name',
    align: 'left',
  },
  {
    id: 'inventory_file',
    label: 'inventories.labels.inventoryFile',
    align: 'left',
  },
  {
    id: 'inventory_status',
    label: 'inventories.labels.status',
    align: 'left',
  },
]

export const inventoryUsersListTableHeadCells: HeadCell[] = [
  {
    id: 'user_inventory_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'username',
    label: 'inventories.labels.username',
    align: 'left',
  },
  {
    id: 'user_type',
    label: 'inventories.labels.userType',
    align: 'left',
  },
]

export const inventoryTeamsListTableHeadCells: HeadCell[] = [
  {
    id: 'team_inventory_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'inventories.labels.name',
    align: 'left',
  },
  {
    id: 'description',
    label: 'inventories.labels.description',
    align: 'left',
  },
]

export const inventoryGroupsListTableHeadCells: HeadCell[] = [
  {
    id: 'inventory_group_id',
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

export const inventorySchedulesListTableHeadCells: HeadCell[] = [
  {
    id: 'inventory_schedule_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'inventories.labels.name',
    align: 'left',
  },
  {
    id: 'schedule_type',
    label: 'inventories.labels.scheduleType',
    align: 'left',
  },
  {
    id: 'next_date',
    label: 'inventories.labels.nextRun',
    align: 'left',
  },
]
