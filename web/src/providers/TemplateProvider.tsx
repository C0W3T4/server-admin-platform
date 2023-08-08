import { DescriptionTwoTone, EditTwoTone } from '@mui/icons-material'
import { FaUsers } from 'react-icons/fa'
import { TbCalendarTime, TbCirclePlus, TbUsers } from 'react-icons/tb'
import { VscDebugRerun, VscRunAll } from 'react-icons/vsc'
import { MapsProvidersProps } from '../types'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'
import { LaunchType, Verbosity } from '../types/template'

export const verbosityMap = new Map<Verbosity, MapsProvidersProps>([
  [
    Verbosity.ZERO,
    {
      label: 'enums.verbosity.zero',
    },
  ],
  [
    Verbosity.ONE,
    {
      label: 'enums.verbosity.one',
    },
  ],
  [
    Verbosity.TWO,
    {
      label: 'enums.verbosity.two',
    },
  ],
  [
    Verbosity.THREE,
    {
      label: 'enums.verbosity.three',
    },
  ],
  [
    Verbosity.FOUR,
    {
      label: 'enums.verbosity.four',
    },
  ],
  [
    Verbosity.FIVE,
    {
      label: 'enums.verbosity.five',
    },
  ],
  [
    Verbosity.SIX,
    {
      label: 'enums.verbosity.six',
    },
  ],
])

export const launchTypeMap = new Map<LaunchType, MapsProvidersProps>([
  [
    LaunchType.RUN,
    {
      label: 'enums.launchType.run',
      icon: <VscRunAll size={16} color="#29b6f6" className="icon-container" />,
    },
  ],
  [
    LaunchType.CHECK,
    {
      label: 'enums.launchType.check',
      icon: (
        <VscDebugRerun size={16} color="#29b6f6" className="icon-container" />
      ),
    },
  ],
])

export const privilegeEscalationMap = new Map<boolean, MapsProvidersProps>([
  [
    true,
    {
      label: 'enums.bool.true',
    },
  ],
  [
    false,
    {
      label: 'enums.bool.false',
    },
  ],
])

export const templateCreateTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.create',
    icon: <TbCirclePlus size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const templateEditTabsOptions: TabsOptionsProps[] = [
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
    label: 'tabs.labels.schedules',
    icon: <TbCalendarTime size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const templateDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]

export const templateListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'templates.labels.name',
    align: 'left',
  },
  {
    id: 'launch_type',
    label: 'templates.labels.launchType',
    align: 'left',
  },
]

export const templateUsersListTableHeadCells: HeadCell[] = [
  {
    id: 'user_template_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'username',
    label: 'templates.labels.username',
    align: 'left',
  },
  {
    id: 'user_type',
    label: 'templates.labels.userType',
    align: 'left',
  },
]

export const templateTeamsListTableHeadCells: HeadCell[] = [
  {
    id: 'team_template_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'templates.labels.name',
    align: 'left',
  },
  {
    id: 'description',
    label: 'templates.labels.description',
    align: 'left',
  },
]

export const templateSchedulesListTableHeadCells: HeadCell[] = [
  {
    id: 'template_schedule_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'templates.labels.name',
    align: 'left',
  },
  {
    id: 'schedule_type',
    label: 'templates.labels.scheduleType',
    align: 'left',
  },
  {
    id: 'next_date',
    label: 'templates.labels.nextRun',
    align: 'left',
  },
]
