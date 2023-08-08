import {
  Button,
  CardActions,
  Divider,
  FormHelperText,
  Grid,
  MenuItem,
  Stack,
  TextField,
  Typography,
  useTheme,
} from '@mui/material'
import { FieldValues, SubmitHandler, useForm } from 'react-hook-form'
import { FormattedMessage } from 'react-intl'
import { useNavigate, useParams } from 'react-router-dom'
import useAuth from '../../../../hooks/useAuth'
import { useAxiosGet } from '../../../../hooks/useAxiosGet'
import { useLoading } from '../../../../hooks/useLoading'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import {
  sourceControlMap,
  toolsMap,
} from '../../../../providers/ProjectProvider'
import { FormProps } from '../../../../types'
import { UserOrganizationsDataProps } from '../../../../types/access'
import {
  CredentialDataProps,
  CredentialType,
} from '../../../../types/credential'
import {
  ProjectDataProps,
  SourceControlCredentialType,
  Tools,
} from '../../../../types/project'
import { AnimateButton } from '../../../AnimateButton'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

export interface IFormInput {
  name: string
  description?: string
  source_control_credential_type: SourceControlCredentialType
  tool: Tools
  source_control_url: string
  base_path?: string
  playbook_directory?: string
  organization_id: string
}

export const FormProject = ({
  defaultValues,
  setNewData,
  mode,
}: FormProps<ProjectDataProps>) => {
  const { showLoading, hideLoading } = useLoading()

  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const theme = useTheme()

  const { data: myOrganizations, error: myOrganizationsError } = useAxiosGet<
    UserOrganizationsDataProps[]
  >(`api/assigns/users-organizations/${user?.id}/organizations`)
  const { data: myCredentials } = useAxiosGet<CredentialDataProps[]>(
    `api/assigns/users-credentials/${user?.id}/credentials`,
  )

  const haveSourceControlCredential = myCredentials?.some(
    (v) => v.credential_type === CredentialType.SOURCE_CONTROL,
  )

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    defaultValues: {
      name: defaultValues?.name,
      description: defaultValues?.description,
      source_control_credential_type:
        defaultValues?.source_control_credential_type,
      tool: defaultValues?.tool,
      source_control_url: defaultValues?.source_control_url,
      base_path: defaultValues?.base_path,
      playbook_directory: defaultValues?.playbook_directory,
      organization_id: defaultValues?.organization.id,
    },
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()
    await api
      .request({
        method: mode === 'create' ? 'POST' : 'PUT',
        url: mode === 'create' ? '/api/projects' : `/api/projects/${id}`,
        data: formData,
      })
      .then((response) => {
        dispatch(
          openSnackbar({
            open: true,
            message:
              response.status === 200 ? (
                <FormattedMessage id="snackbar.message.success.200.updated" />
              ) : (
                <FormattedMessage id="snackbar.message.success.201" />
              ),
            transition: 'SlideUp',
            variant: 'alert',
            alert: {
              color: 'success',
            },
            close: true,
          }),
        )
        setTimeout(() => {
          navigate('../list', { replace: true })
        }, 1)
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
      .finally(() => hideLoading())
  }

  const updateRepo = async (id: string) => {
    showLoading()
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
      .finally(() => hideLoading())
  }

  const handleUpdateRepo = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    id: string,
  ) => updateRepo(id)

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <SubCard
        title={
          mode === 'edit' ? (
            defaultValues?.name
          ) : (
            <FormattedMessage id="projects.labels.new" />
          )
        }
        secondary={
          <CardHeaderActions
            updateRepo={
              mode === 'edit'
                ? {
                    projectId: defaultValues!.id,
                    handleUpdateRepo,
                  }
                : null
            }
          />
        }
      >
        {myOrganizations && haveSourceControlCredential ? (
          <>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="name"
                  label={<FormattedMessage id="projects.labels.name" />}
                  error={errors.name && errors.name?.type === 'required'}
                  helperText={
                    errors.name &&
                    errors.name?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('name', { required: true })}
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="description"
                  label={<FormattedMessage id="projects.labels.description" />}
                  error={
                    errors.description &&
                    errors.description?.type === 'required'
                  }
                  helperText={
                    errors.description &&
                    errors.description?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('description')}
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="tool"
                  select
                  label={<FormattedMessage id="projects.labels.tool" />}
                  defaultValue={
                    defaultValues
                      ? defaultValues.tool
                      : toolsMap.keys().next().value
                  }
                  error={errors.tool && errors.tool?.type === 'required'}
                  helperText={
                    errors.tool &&
                    errors.tool?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('tool', { required: true })}
                >
                  {[...toolsMap.entries()].map(([key, option], index) => (
                    <MenuItem key={index} value={key}>
                      {option.icon}
                      <FormattedMessage id={option.label} />
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="source-control"
                  select
                  label={
                    <FormattedMessage id="projects.labels.sourceControl" />
                  }
                  defaultValue={
                    defaultValues
                      ? defaultValues.source_control_credential_type
                      : sourceControlMap.keys().next().value
                  }
                  error={
                    errors.source_control_credential_type &&
                    errors.source_control_credential_type?.type === 'required'
                  }
                  helperText={
                    errors.source_control_credential_type &&
                    errors.source_control_credential_type?.type ===
                      'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('source_control_credential_type', {
                    required: true,
                  })}
                >
                  {[...sourceControlMap.entries()].map(
                    ([key, option], index) => (
                      <MenuItem key={index} value={key}>
                        {option.icon}
                        <FormattedMessage id={option.label} />
                      </MenuItem>
                    ),
                  )}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="source-control-url"
                  label={<FormattedMessage id="projects.labels.url" />}
                  error={
                    errors.source_control_url &&
                    errors.source_control_url?.type === 'required'
                  }
                  helperText={
                    errors.source_control_url &&
                    errors.source_control_url?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('source_control_url', { required: true })}
                />
              </Grid>
              {/* <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
              <TextField
                fullWidth
                id="base-path"
                label={<FormattedMessage id="projects.labels.basePath" />}
                error={errors.base_path && errors.base_path?.type === 'required'}
                helperText={errors.base_path && errors.base_path?.type === 'required' && <FormHelperText error><FormattedMessage id="input.validation.required" /></FormHelperText>}
                {...register('base_path')}
              />
            </Grid>
            <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
              <TextField
                fullWidth
                id="playbook-directory"
                label={<FormattedMessage id="projects.labels.playbookDirectory" />}
                error={errors.playbook_directory && errors.playbook_directory?.type === 'required'}
                helperText={errors.playbook_directory && errors.playbook_directory?.type === 'required' && <FormHelperText error><FormattedMessage id="input.validation.required" /></FormHelperText>}
                {...register('playbook_directory')}
              />
            </Grid> */}
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  id="organization-id"
                  select
                  label={
                    <FormattedMessage id="projects.labels.selectOrganization" />
                  }
                  fullWidth
                  defaultValue={
                    defaultValues ? defaultValues.organization.id : ''
                  }
                  error={
                    errors.organization_id &&
                    errors.organization_id?.type === 'required'
                  }
                  helperText={
                    errors.organization_id &&
                    errors.organization_id?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('organization_id', { required: true })}
                >
                  {myOrganizations?.map((option) => (
                    <MenuItem
                      key={option.organization.id}
                      value={option.organization.id}
                    >
                      {option.organization.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
            </Grid>
            <Divider sx={{ paddingTop: '16px' }} />
            <CardActions>
              <Grid
                container
                alignItems="center"
                justifyContent="flex-end"
                spacing={2}
              >
                <Grid item>
                  <AnimateButton scale={{ hover: 1.1, tap: 0.9 }}>
                    <Button
                      variant="contained"
                      color="secondary"
                      type="submit"
                      disabled={!isValid}
                      sx={{
                        boxShadow: theme.customShadows.secondary,
                        ':hover': { boxShadow: 'none' },
                      }}
                    >
                      <FormattedMessage id="input.labels.submit" />
                    </Button>
                  </AnimateButton>
                </Grid>
              </Grid>
            </CardActions>
          </>
        ) : (
          (myOrganizationsError?.response?.status === 404 ||
            !haveSourceControlCredential) && (
            <Stack spacing={2}>
              <Stack
                direction="row"
                spacing={2}
                sx={{
                  alignItems: 'center',
                  justifyContent: 'center',
                  textAlign: 'center',
                }}
              >
                <Typography variant="h4">
                  <FormattedMessage id="input.validation.required.needCreate" />
                  &#58;
                  <br />
                  {myOrganizationsError && (
                    <>
                      <br />
                      <FormattedMessage id="projects.labels.organization" />
                    </>
                  )}
                  {!haveSourceControlCredential && (
                    <>
                      <br />
                      <FormattedMessage id="projects.labels.sourceCredential" />
                    </>
                  )}
                </Typography>
              </Stack>
            </Stack>
          )
        )}
      </SubCard>
    </form>
  )
}
