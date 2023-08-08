import { DescriptionTwoTone, EditTwoTone } from '@mui/icons-material'
import { AiOutlineCluster } from 'react-icons/ai'
import { TbCirclePlus, TbFolders, TbTemplate } from 'react-icons/tb'
import { MapsProvidersProps } from '../types'
import {
  ScheduleRepeatFrequency,
  ScheduleType,
  ScheduleWeekdays,
} from '../types/schedule'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'

export const weekdays: [
  ScheduleWeekdays,
  ScheduleWeekdays,
  ScheduleWeekdays,
  ScheduleWeekdays,
  ScheduleWeekdays,
  ScheduleWeekdays,
  ScheduleWeekdays,
] = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

export const scheduleTypeMap = new Map<ScheduleType, MapsProvidersProps>([
  [
    ScheduleType.TEMPLATE,
    {
      label: 'enums.scheduleType.template',
      icon: <TbTemplate size={16} color="#29b6f6" className="icon-container" />,
    },
  ],
  [
    ScheduleType.PROJECT,
    {
      label: 'enums.scheduleType.project',
      icon: <TbFolders size={16} color="#29b6f6" className="icon-container" />,
    },
  ],
  [
    ScheduleType.INVENTORY,
    {
      label: 'enums.scheduleType.inventory',
      icon: (
        <AiOutlineCluster
          size={16}
          color="#29b6f6"
          className="icon-container"
        />
      ),
    },
  ],
])

interface MapsScheduleProvidersProps extends MapsProvidersProps {
  numFrequencyLabel: string
}

export const scheduleRepeatFrequencyMap = new Map<
  ScheduleRepeatFrequency,
  MapsScheduleProvidersProps
>([
  [
    ScheduleRepeatFrequency.RUN_ONCE,
    {
      label: 'enums.repeatFrequency.runOnce',
      numFrequencyLabel: 'schedules.labels.runOnce',
    },
  ],
  [
    ScheduleRepeatFrequency.MINUTE,
    {
      label: 'enums.repeatFrequency.minute',
      numFrequencyLabel: 'schedules.labels.minutes',
    },
  ],
  [
    ScheduleRepeatFrequency.HOUR,
    {
      label: 'enums.repeatFrequency.hour',
      numFrequencyLabel: 'schedules.labels.hours',
    },
  ],
  [
    ScheduleRepeatFrequency.DAY,
    {
      label: 'enums.repeatFrequency.day',
      numFrequencyLabel: 'schedules.labels.days',
    },
  ],
  [
    ScheduleRepeatFrequency.MONTH,
    {
      label: 'enums.repeatFrequency.month',
      numFrequencyLabel: 'schedules.labels.months',
    },
  ],
  [
    ScheduleRepeatFrequency.WEEK,
    {
      label: 'enums.repeatFrequency.weekday',
      numFrequencyLabel: 'schedules.labels.weeks',
    },
  ],
  [
    ScheduleRepeatFrequency.YEAR,
    {
      label: 'enums.repeatFrequency.year',
      numFrequencyLabel: 'schedules.labels.years',
    },
  ],
])

export const scheduleCreateTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.create',
    icon: <TbCirclePlus size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const scheduleEditTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.edit',
    icon: <EditTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
  // {
  //   label: 'tabs.labels.templates',
  //   icon: <TbTemplate size={16} color="#ec407a" />,
  //   disabled: false
  // }
]

export const scheduleDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]

export const scheduleListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'schedules.labels.name',
    align: 'left',
  },
  {
    id: 'schedule_type',
    label: 'schedules.labels.scheduleType',
    align: 'left',
  },
]

export const scheduleTemplatesListTableHeadCells: HeadCell[] = [
  {
    id: 'template_schedule_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'schedules.labels.name',
    align: 'left',
  },
  {
    id: 'description',
    label: 'schedules.labels.description',
    align: 'left',
  },
]
