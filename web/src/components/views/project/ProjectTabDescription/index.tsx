import { DateRangeTwoTone } from '@mui/icons-material'
import { Grid, Stack, Typography } from '@mui/material'
import { FormattedMessage } from 'react-intl'
import useConfig from '../../../../hooks/useConfig'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { gridSpacing } from '../../../../libs/redux/constants'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import {
  projectStatusMap,
  sourceControlMap,
  toolsMap,
} from '../../../../providers/ProjectProvider'
import { DetailsViewProps } from '../../../../types'
import { ProjectDataProps } from '../../../../types/project'
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

export const ProjectTabDescription = ({
  defaultValues,
  setNewData,
}: DetailsViewProps<ProjectDataProps>) => {
  const { locale } = useConfig()

  const updateRepo = async (id: string) => {
    await api
      .put(`api/projects/${id}/repo`)
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

  const handleUpdateRepo = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    id: string,
  ) => updateRepo(id)

  return (
    <SubCard
      title={defaultValues?.name}
      secondary={
        <CardHeaderActions
          updateRepo={{
            projectId: defaultValues!.id,
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
                    <FormattedMessage id="projects.labels.name" />
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
                      <FormattedMessage id="projects.labels.description" />
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
                    <FormattedMessage id="projects.labels.status" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {projectStatusMap.get(defaultValues!.project_status)?.icon}
                    <FormattedMessage
                      id={
                        projectStatusMap.get(defaultValues!.project_status)
                          ?.label
                      }
                    />
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="projects.labels.sourceControl" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {
                      sourceControlMap.get(
                        defaultValues!.source_control_credential_type,
                      )?.icon
                    }
                    <FormattedMessage
                      id={
                        sourceControlMap.get(
                          defaultValues!.source_control_credential_type,
                        )?.label
                      }
                    />
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="projects.labels.url" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.source_control_url}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="projects.labels.tool" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {toolsMap.get(defaultValues!.tool)?.icon}
                    <FormattedMessage
                      id={toolsMap.get(defaultValues!.tool)?.label}
                    />
                  </Typography>
                </Stack>
                {defaultValues?.base_path && (
                  <Stack
                    direction="row"
                    spacing={2}
                    sx={{ alignItems: 'center' }}
                  >
                    <Typography variant="subtitle1" sx={labelSX}>
                      <FormattedMessage id="projects.labels.basePath" />
                      &#58;
                    </Typography>
                    <Typography variant="body2" sx={infoSX}>
                      {defaultValues.base_path}
                    </Typography>
                  </Stack>
                )}
                {defaultValues?.playbook_directory && (
                  <Stack
                    direction="row"
                    spacing={2}
                    sx={{ alignItems: 'center' }}
                  >
                    <Typography variant="subtitle1" sx={labelSX}>
                      <FormattedMessage id="projects.labels.playbook" />
                      &#58;
                    </Typography>
                    <Typography variant="body2" sx={infoSX}>
                      {defaultValues.playbook_directory}
                    </Typography>
                  </Stack>
                )}
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="projects.labels.organizationName" />
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
                    <FormattedMessage id="projects.labels.createdAt" />
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
                    <FormattedMessage id="projects.labels.lastModifiedAt" />
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
                    <FormattedMessage id="projects.labels.createdBy" />
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
                    <FormattedMessage id="projects.labels.lastModifiedBy" />
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
