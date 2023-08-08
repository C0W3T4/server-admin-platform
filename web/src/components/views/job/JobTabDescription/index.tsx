import { DateRangeTwoTone } from '@mui/icons-material'
import { Grid, Stack, Typography } from '@mui/material'
import { differenceInSeconds } from 'date-fns'
import { FormattedMessage } from 'react-intl'
import useConfig from '../../../../hooks/useConfig'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { gridSpacing } from '../../../../libs/redux/constants'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import { jobStatusMap } from '../../../../providers/JobProvider'
import { DetailsViewProps } from '../../../../types'
import { JobDataProps } from '../../../../types/job'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

const iconSX = {
  width: 16,
  height: 16,
  verticalAlign: 'middle',
  mr: 0.5,
}

const labelSX = {
  flex: '1 1 33.33%',
  textAlign: 'right',
}

const infoSX = {
  flex: '1 1 66.66%',
  textAlign: 'left',
}

export const JobTabDescription = ({
  defaultValues,
  setNewData,
}: DetailsViewProps<JobDataProps>) => {
  const { locale } = useConfig()

  const relaunchJob = async (id: string) => {
    await api
      .put(`api/jobs/${id}/launch`)
      .then((response) => {
        if (response.status === 200) {
          if (setNewData) {
            setNewData(response.data)
          }
          dispatch(
            openSnackbar({
              open: true,
              message: <FormattedMessage id="snackbar.message.success.200" />,
              transition: 'SlideUp',
              variant: 'alert',
              alert: {
                color: 'success',
              },
              close: true,
            }),
          )
        }
      })
      .catch(() => {
        dispatch(
          openSnackbar({
            open: true,
            message: <FormattedMessage id="snackbar.message.error" />,
            transition: 'SlideUp',
            variant: 'alert',
            alert: {
              color: 'error',
            },
            close: true,
          }),
        )
      })
  }

  const handleRelaunchJob = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    id: string,
  ) => relaunchJob(id)

  const syncInventory = async (id: string) => {
    await api
      .put(`api/inventories/${id}/sync`)
      .then((response) => {
        if (response.status === 200) {
          dispatch(
            openSnackbar({
              open: true,
              message: <FormattedMessage id="snackbar.message.success.200" />,
              transition: 'SlideUp',
              variant: 'alert',
              alert: {
                color: 'success',
              },
              close: true,
            }),
          )
        }
      })
      .catch(() => {
        dispatch(
          openSnackbar({
            open: true,
            message: <FormattedMessage id="snackbar.message.error" />,
            transition: 'SlideUp',
            variant: 'alert',
            alert: {
              color: 'error',
            },
            close: true,
          }),
        )
      })
  }

  const handleSyncInventory = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    id: string,
  ) => syncInventory(id)

  const updateRepo = async (id: string) => {
    await api
      .put(`api/projects/${id}/repo`)
      .then((response) => {
        if (response.status === 200) {
          dispatch(
            openSnackbar({
              open: true,
              message: <FormattedMessage id="snackbar.message.success.200" />,
              transition: 'SlideUp',
              variant: 'alert',
              alert: {
                color: 'success',
              },
              close: true,
            }),
          )
        }
      })
      .catch(() => {
        dispatch(
          openSnackbar({
            open: true,
            message: <FormattedMessage id="snackbar.message.error" />,
            transition: 'SlideUp',
            variant: 'alert',
            alert: {
              color: 'error',
            },
            close: true,
          }),
        )
      })
  }

  const handleUpdateRepo = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    id: string,
  ) => updateRepo(id)

  return (
    <SubCard
      title={defaultValues?.template.name}
      secondary={
        <CardHeaderActions
          relaunchJob={{
            jobId: defaultValues!.id,
            handleRelaunchJob,
          }}
          syncInventory={{
            inventoryId: defaultValues!.template.inventory.id,
            handleSyncInventory,
          }}
          updateRepo={{
            projectId: defaultValues!.template.project.id,
            handleUpdateRepo,
          }}
        />
      }
    >
      <Grid container spacing={gridSpacing}>
        <Grid item xs={12}>
          <Grid container spacing={gridSpacing}>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <Stack spacing={2}>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="jobs.labels.name" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.template.name}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="jobs.labels.jobStatus" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {jobStatusMap.get(defaultValues!.job_status)?.icon}
                    <FormattedMessage
                      id={jobStatusMap.get(defaultValues!.job_status)?.label}
                    />
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="jobs.labels.startedAt" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    <DateRangeTwoTone sx={iconSX} color="info" />
                    {new Intl.DateTimeFormat(locale, {
                      dateStyle: 'full',
                      timeStyle: 'medium',
                    }).format(new Date(defaultValues!.started_at))}
                  </Typography>
                </Stack>
                {defaultValues!.finished_at && (
                  <>
                    <Stack
                      direction="row"
                      spacing={2}
                      sx={{ alignItems: 'center' }}
                    >
                      <Typography variant="subtitle1" sx={labelSX}>
                        <FormattedMessage id="jobs.labels.finishedAt" />
                        &#58;
                      </Typography>
                      <Typography variant="body2" sx={infoSX}>
                        <DateRangeTwoTone sx={iconSX} color="info" />
                        {new Intl.DateTimeFormat(locale, {
                          dateStyle: 'full',
                          timeStyle: 'medium',
                        }).format(new Date(defaultValues!.finished_at))}
                      </Typography>
                    </Stack>
                    <Stack
                      direction="row"
                      spacing={2}
                      sx={{ alignItems: 'center' }}
                    >
                      <Typography variant="subtitle1" sx={labelSX}>
                        <FormattedMessage id="jobs.labels.elapsed" />
                        &#58;
                      </Typography>
                      <Typography variant="body2" sx={infoSX}>
                        {differenceInSeconds(
                          new Date(defaultValues!.finished_at),
                          new Date(defaultValues!.started_at),
                          { roundingMethod: 'round' },
                        )}
                        &nbsp;
                        <FormattedMessage id="jobs.labels.seconds" />
                      </Typography>
                    </Stack>
                  </>
                )}
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="jobs.labels.launchedBy" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.launched_by}
                  </Typography>
                </Stack>
              </Stack>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </SubCard>
  )
}
