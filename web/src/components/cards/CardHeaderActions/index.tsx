import { ArrowBackTwoTone, Sync, SyncAlt, Update } from '@mui/icons-material'
import { IconButton, Tooltip, Zoom } from '@mui/material'
import { TbRocket } from 'react-icons/tb'
import { FormattedMessage } from 'react-intl'
import { useNavigate } from 'react-router-dom'
import { TemplateDataProps } from '../../../types/template'

interface LaunchJobProps {
  template: TemplateDataProps
  handleLaunchJob: (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    row: TemplateDataProps,
  ) => Promise<void>
}

interface RelaunchJobProps {
  jobId: string
  handleRelaunchJob: (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    id: string,
  ) => Promise<void>
}

interface UpdateRepoProps {
  projectId: string
  handleUpdateRepo: (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    id: string,
  ) => Promise<void>
}

interface SyncInventoryProps {
  inventoryId: string
  handleSyncInventory: (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    id: string,
  ) => Promise<void>
}

interface UpdateHostStatusProps {
  hostId: string
  handleUpdateHostStatus: (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    id: string,
  ) => Promise<void>
}

interface CardHeaderActionsProps {
  launchJob?: LaunchJobProps | null
  relaunchJob?: RelaunchJobProps | null
  updateRepo?: UpdateRepoProps | null
  syncInventory?: SyncInventoryProps | null
  updateHostStatus?: UpdateHostStatusProps | null
}

export const CardHeaderActions = ({
  launchJob,
  relaunchJob,
  updateRepo,
  syncInventory,
  updateHostStatus,
}: CardHeaderActionsProps) => {
  const navigate = useNavigate()

  return (
    <>
      {launchJob && (
        <Tooltip
          TransitionComponent={Zoom}
          title={<FormattedMessage id="tooltips.launchJob" />}
        >
          <IconButton
            color="info"
            size="large"
            onClick={(event) =>
              launchJob.handleLaunchJob(event, launchJob.template)
            }
          >
            <TbRocket size={16} />
          </IconButton>
        </Tooltip>
      )}
      {relaunchJob && (
        <Tooltip
          TransitionComponent={Zoom}
          title={<FormattedMessage id="tooltips.relaunchJob" />}
        >
          <IconButton
            color="info"
            size="large"
            onClick={(event) =>
              relaunchJob.handleRelaunchJob(event, relaunchJob.jobId)
            }
          >
            <TbRocket size={16} />
          </IconButton>
        </Tooltip>
      )}
      {updateRepo && (
        <Tooltip
          TransitionComponent={Zoom}
          title={<FormattedMessage id="tooltips.updateProject" />}
        >
          <IconButton
            size="large"
            onClick={(event) =>
              updateRepo.handleUpdateRepo(event, updateRepo.projectId)
            }
          >
            <Update sx={{ fontSize: '1.3rem' }} color="info" />
          </IconButton>
        </Tooltip>
      )}
      {syncInventory && (
        <Tooltip
          TransitionComponent={Zoom}
          title={<FormattedMessage id="tooltips.syncInventory" />}
        >
          <IconButton
            size="large"
            onClick={(event) =>
              syncInventory.handleSyncInventory(
                event,
                syncInventory.inventoryId,
              )
            }
          >
            <Sync sx={{ fontSize: '1.3rem' }} color="info" />
          </IconButton>
        </Tooltip>
      )}
      {updateHostStatus && (
        <Tooltip
          TransitionComponent={Zoom}
          title={<FormattedMessage id="tooltips.updateHostStatus" />}
        >
          <IconButton
            size="large"
            onClick={(event) =>
              updateHostStatus.handleUpdateHostStatus(
                event,
                updateHostStatus.hostId,
              )
            }
          >
            <SyncAlt sx={{ fontSize: '1.3rem' }} color="info" />
          </IconButton>
        </Tooltip>
      )}
      <Tooltip
        TransitionComponent={Zoom}
        title={<FormattedMessage id="tooltips.back" />}
      >
        <IconButton onClick={() => navigate(-1)} size="large">
          <ArrowBackTwoTone sx={{ fontSize: '1.3rem' }} color="secondary" />
        </IconButton>
      </Tooltip>
    </>
  )
}
