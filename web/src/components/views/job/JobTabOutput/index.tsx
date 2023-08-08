import { Grid, Stack, TextField } from '@mui/material'
import { FormattedMessage } from 'react-intl'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { gridSpacing } from '../../../../libs/redux/constants'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import { DetailsViewProps } from '../../../../types'
import { JobDataProps } from '../../../../types/job'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

export const JobTabOutput = ({
  defaultValues,
  setNewData,
}: DetailsViewProps<JobDataProps>) => {
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
                  <TextField
                    fullWidth
                    id="name"
                    multiline
                    maxRows={25}
                    variant="outlined"
                    autoFocus
                    color="info"
                    inputProps={{ readOnly: true }}
                    value={defaultValues!.output}
                  />
                </Stack>
              </Stack>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </SubCard>
  )
}
