import { DescriptionTwoTone } from '@mui/icons-material'
import { BsHourglassSplit } from 'react-icons/bs'
import { MdError, MdOutlineDoneAll, MdOutlinePending } from 'react-icons/md'
import { VscOutput, VscVmRunning } from 'react-icons/vsc'
import { MapsProvidersProps } from '../types'
import { JobStatus } from '../types/job'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'

export const jobStatusMap = new Map<JobStatus, MapsProvidersProps>([
  [
    JobStatus.RUNNING,
    {
      label: 'enums.jobStatus.running',
      icon: (
        <VscVmRunning size={16} color="#8be09f" className="icon-container" />
      ),
    },
  ],
  [
    JobStatus.SUCCESSFUL,
    {
      label: 'enums.jobStatus.successful',
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
    JobStatus.FAILED,
    {
      label: 'enums.jobStatus.failed',
      icon: <MdError size={16} color="#d9534f" className="icon-container" />,
    },
  ],
  [
    JobStatus.PENDING,
    {
      label: 'enums.jobStatus.pending',
      icon: (
        <MdOutlinePending
          size={16}
          color="#f0ad4e"
          className="icon-container"
        />
      ),
    },
  ],
  [
    JobStatus.WAITING,
    {
      label: 'enums.jobStatus.waiting',
      icon: (
        <BsHourglassSplit
          size={16}
          color="#f0ad4e"
          className="icon-container"
        />
      ),
    },
  ],
])

export const jobDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
  {
    label: 'tabs.labels.output',
    icon: <VscOutput size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const jobListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'jobs.labels.name',
    align: 'left',
  },
  {
    id: 'job_status',
    label: 'jobs.labels.jobStatus',
    align: 'left',
  },
  {
    id: 'started_at',
    label: 'jobs.labels.startedAt',
    align: 'left',
  },
  {
    id: 'finished_at',
    label: 'jobs.labels.finishedAt',
    align: 'left',
  },
]
