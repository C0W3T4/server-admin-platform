import { DateRangeTwoTone } from '@mui/icons-material'
import { Grid, Stack, Typography } from '@mui/material'
import { FormattedMessage } from 'react-intl'
import useConfig from '../../../../hooks/useConfig'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { gridSpacing } from '../../../../libs/redux/constants'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import {
  launchTypeMap,
  privilegeEscalationMap,
  verbosityMap,
} from '../../../../providers/TemplateProvider'
import { DetailsViewProps } from '../../../../types'
import { TemplateDataProps } from '../../../../types/template'
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

export const TemplateTabDescription = ({
  defaultValues,
}: DetailsViewProps<TemplateDataProps>) => {
  const { locale } = useConfig()

  const launchJob = async (row: TemplateDataProps) => {
    await api
      .post(`api/jobs/launch`, {
        template_id: row.id,
        organization_id: row.organization.id,
      })
      .then((response) => {
        if (response.status === 201) {
          dispatch(
            openSnackbar({
              open: true,
              message: <FormattedMessage id="snackbar.message.success.201" />,
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

  const handleLaunchJob = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    row: TemplateDataProps,
  ) => launchJob(row)

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
      title={defaultValues?.name}
      secondary={
        <CardHeaderActions
          launchJob={{
            template: defaultValues!,
            handleLaunchJob,
          }}
          syncInventory={{
            inventoryId: defaultValues!.inventory.id,
            handleSyncInventory,
          }}
          updateRepo={{
            projectId: defaultValues!.project.id,
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
                    <FormattedMessage id="templates.labels.name" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.name}
                  </Typography>
                </Stack>
                {defaultValues?.description && (
                  <Stack
                    direction="row"
                    spacing={2}
                    sx={{ alignItems: 'center' }}
                  >
                    <Typography variant="subtitle1" sx={labelSX}>
                      <FormattedMessage id="templates.labels.description" />
                      &#58;
                    </Typography>
                    <Typography variant="body2" sx={infoSX}>
                      {defaultValues.description}
                    </Typography>
                  </Stack>
                )}
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="templates.labels.launchType" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {launchTypeMap.get(defaultValues!.launch_type)?.icon}
                    <FormattedMessage
                      id={launchTypeMap.get(defaultValues!.launch_type)?.label}
                    />
                  </Typography>
                </Stack>
                {defaultValues?.forks && (
                  <Stack
                    direction="row"
                    spacing={2}
                    sx={{ alignItems: 'center' }}
                  >
                    <Typography variant="subtitle1" sx={labelSX}>
                      <FormattedMessage id="templates.labels.forks" />
                      &#58;
                    </Typography>
                    <Typography variant="body2" sx={infoSX}>
                      {defaultValues.forks}
                    </Typography>
                  </Stack>
                )}
                {defaultValues?.limit && (
                  <Stack
                    direction="row"
                    spacing={2}
                    sx={{ alignItems: 'center' }}
                  >
                    <Typography variant="subtitle1" sx={labelSX}>
                      <FormattedMessage id="templates.labels.limit" />
                      &#58;
                    </Typography>
                    <Typography variant="body2" sx={infoSX}>
                      {defaultValues.limit}
                    </Typography>
                  </Stack>
                )}
                {defaultValues?.privilege_escalation !== null &&
                  defaultValues?.privilege_escalation !== undefined && (
                    <Stack
                      direction="row"
                      spacing={2}
                      sx={{ alignItems: 'center' }}
                    >
                      <Typography variant="subtitle1" sx={labelSX}>
                        <FormattedMessage id="templates.labels.privilegeEscalation" />
                        &#58;
                      </Typography>
                      <Typography variant="body2" sx={infoSX}>
                        {
                          privilegeEscalationMap.get(
                            defaultValues!.privilege_escalation,
                          )?.icon
                        }
                        <FormattedMessage
                          id={
                            privilegeEscalationMap.get(
                              defaultValues!.privilege_escalation,
                            )?.label
                          }
                        />
                      </Typography>
                    </Stack>
                  )}
                {defaultValues?.verbosity && (
                  <Stack
                    direction="row"
                    spacing={2}
                    sx={{ alignItems: 'center' }}
                  >
                    <Typography variant="subtitle1" sx={labelSX}>
                      <FormattedMessage id="templates.labels.verbosity" />
                      &#58;
                    </Typography>
                    <Typography variant="body2" sx={infoSX}>
                      {verbosityMap.get(defaultValues!.verbosity)?.icon}
                      <FormattedMessage
                        id={verbosityMap.get(defaultValues.verbosity)?.label}
                      />
                    </Typography>
                  </Stack>
                )}
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="templates.labels.playbookName" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.playbook_name}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="templates.labels.inventoryName" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.inventory.name}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="templates.labels.projectName" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.project.name}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="templates.labels.credentialName" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.credential.name}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="templates.labels.organizationName" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.organization.name}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="templates.labels.createdAt" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    <DateRangeTwoTone sx={iconSX} color="info" />
                    {new Intl.DateTimeFormat(locale, {
                      dateStyle: 'full',
                      timeStyle: 'medium',
                    }).format(new Date(defaultValues!.created_at))}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="templates.labels.lastModifiedAt" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    <DateRangeTwoTone sx={iconSX} color="info" />
                    {new Intl.DateTimeFormat(locale, {
                      dateStyle: 'full',
                      timeStyle: 'medium',
                    }).format(new Date(defaultValues!.last_modified_at))}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="templates.labels.createdBy" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.created_by}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="templates.labels.lastModifiedBy" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.last_modified_by}
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
