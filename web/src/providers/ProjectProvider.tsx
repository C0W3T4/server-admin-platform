import { DescriptionTwoTone, EditTwoTone, GitHub } from '@mui/icons-material'
import { BsHourglassSplit } from 'react-icons/bs'
import { FaUsers } from 'react-icons/fa'
import { HiOutlineThumbUp } from 'react-icons/hi'
import {
  MdCallMissed,
  MdError,
  MdOutlineDoneAll,
  MdOutlinePending,
  MdUpdateDisabled,
} from 'react-icons/md'
import { SiAnsible } from 'react-icons/si'
import { TbCalendarTime, TbCirclePlus, TbUsers } from 'react-icons/tb'
import { TiCancel } from 'react-icons/ti'
import { VscError, VscVmRunning } from 'react-icons/vsc'
import { MapsProvidersProps } from '../types'
import {
  ProjectStatus,
  SourceControlCredentialType,
  Tools,
} from '../types/project'
import { HeadCell } from '../types/table'
import { TabsOptionsProps } from '../types/tabs'

export const projectStatusMap = new Map<ProjectStatus, MapsProvidersProps>([
  [
    ProjectStatus.PENDING,
    {
      label: 'enums.projectStatus.pending',
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
    ProjectStatus.WAITING,
    {
      label: 'enums.projectStatus.waiting',
      icon: (
        <BsHourglassSplit
          size={16}
          color="#f0ad4e"
          className="icon-container"
        />
      ),
    },
  ],
  [
    ProjectStatus.RUNNING,
    {
      label: 'enums.projectStatus.running',
      icon: (
        <VscVmRunning size={16} color="#8be09f" className="icon-container" />
      ),
    },
  ],
  [
    ProjectStatus.SUCCESSFUL,
    {
      label: 'enums.projectStatus.successful',
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
    ProjectStatus.FAILED,
    {
      label: 'enums.projectStatus.failed',
      icon: <MdError size={16} color="#d9534f" className="icon-container" />,
    },
  ],
  [
    ProjectStatus.ERROR,
    {
      label: 'enums.projectStatus.error',
      icon: <VscError size={16} color="#d9534f" className="icon-container" />,
    },
  ],
  [
    ProjectStatus.CANCELED,
    {
      label: 'enums.projectStatus.canceled',
      icon: <TiCancel size={16} color="#d9534f" className="icon-container" />,
    },
  ],
  [
    ProjectStatus.NEVER_UPDATED,
    {
      label: 'enums.projectStatus.neverUpdated',
      icon: (
        <MdUpdateDisabled
          size={16}
          color="#f0ad4e"
          className="icon-container"
        />
      ),
    },
  ],
  [
    ProjectStatus.OK,
    {
      label: 'enums.projectStatus.ok',
      icon: (
        <HiOutlineThumbUp
          size={16}
          color="#f0ad4e"
          className="icon-container"
        />
      ),
    },
  ],
  [
    ProjectStatus.MISSING,
    {
      label: 'enums.projectStatus.missing',
      icon: (
        <MdCallMissed size={16} color="#d9534f" className="icon-container" />
      ),
    },
  ],
])

export const toolsMap = new Map<Tools, MapsProvidersProps>([
  [
    Tools.ANSIBLE,
    {
      label: 'enums.tools.ansible',
      icon: <SiAnsible size={16} color="#29b6f6" className="icon-container" />,
    },
  ],
  // [
  //   Tools.JENKINS,
  //   {
  //     label: 'enums.tools.jenkins',
  //     icon: <FaJenkins size={16} color="#29b6f6" className="icon-container" />
  //   }
  // ],
  // [
  //   Tools.PLAYWRIGHT,
  //   {
  //     label: 'enums.tools.playwright',
  //     icon: <VscPlayCircle size={16} color="#29b6f6" className="icon-container" />
  //   }
  // ],
  // [
  //   Tools.TERRAFORM,
  //   {
  //     label: 'enums.tools.terraform',
  //     icon: <SiTerraform size={16} color="#29b6f6" className="icon-container" />
  //   }
  // ]
])

export const sourceControlMap = new Map<
  SourceControlCredentialType,
  MapsProvidersProps
>([
  [
    SourceControlCredentialType.GIT,
    {
      label: 'enums.sourceControl.git',
      icon: (
        <GitHub
          sx={{ fontSize: '1.3rem' }}
          color="info"
          className="icon-container"
        />
      ),
    },
  ],
  // [
  //   SourceControlCredentialType.MANUAL,
  //   {
  //     label: 'enums.sourceControl.manual',
  //     icon: <FaProjectDiagram size={16}  color="#29b6f6" className="icon-container" />
  //   }
  // ]
])

export const projectCreateTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.create',
    icon: <TbCirclePlus size={16} color="#ec407a" />,
    disabled: false,
  },
]

export const projectEditTabsOptions: TabsOptionsProps[] = [
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

export const projectDetailsTabsOptions: TabsOptionsProps[] = [
  {
    label: 'tabs.labels.details',
    icon: <DescriptionTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />,
    disabled: false,
  },
]

export const projectListTableHeadCells: HeadCell[] = [
  {
    id: 'id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'projects.labels.name',
    align: 'left',
  },
  {
    id: 'project_status',
    label: 'projects.labels.status',
    align: 'left',
  },
  {
    id: 'tool',
    label: 'projects.labels.tool',
    align: 'left',
  },
  {
    id: 'source_control_credential_type',
    label: 'projects.labels.sourceControl',
    align: 'left',
  },
]

export const projectUsersListTableHeadCells: HeadCell[] = [
  {
    id: 'user_project_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'username',
    label: 'projects.labels.username',
    align: 'left',
  },
  {
    id: 'user_type',
    label: 'projects.labels.userType',
    align: 'left',
  },
]

export const projectTeamsListTableHeadCells: HeadCell[] = [
  {
    id: 'team_project_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'projects.labels.name',
    align: 'left',
  },
  {
    id: 'description',
    label: 'projects.labels.description',
    align: 'left',
  },
]

export const projectSchedulesListTableHeadCells: HeadCell[] = [
  {
    id: 'project_schedule_id',
    label: 'table.labels.id',
    align: 'left',
  },
  {
    id: 'name',
    label: 'projects.labels.name',
    align: 'left',
  },
  {
    id: 'schedule_type',
    label: 'projects.labels.scheduleType',
    align: 'left',
  },
  {
    id: 'next_date',
    label: 'projects.labels.nextRun',
    align: 'left',
  },
]
