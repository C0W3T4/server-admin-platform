import {
  Button,
  CardActions,
  Checkbox,
  Divider,
  FormControlLabel,
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
  launchTypeMap,
  verbosityMap,
} from '../../../../providers/TemplateProvider'
import { FormProps } from '../../../../types'
import { UserOrganizationsDataProps } from '../../../../types/access'
import {
  CredentialDataProps,
  CredentialType,
} from '../../../../types/credential'
import { InventoryDataProps } from '../../../../types/inventory'
import { ProjectDataProps } from '../../../../types/project'
import {
  LaunchType,
  TemplateDataProps,
  Verbosity,
} from '../../../../types/template'
import { AnimateButton } from '../../../AnimateButton'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

export interface IFormInput {
  name: string
  description?: string
  playbook_name: string
  limit?: string
  forks?: number
  extra_vars?: string
  privilege_escalation?: boolean
  verbosity?: Verbosity
  launch_type: LaunchType
  inventory_id: string
  project_id: string
  credential_id: string
  organization_id: string
}

export const FormTemplate = ({
  defaultValues,
  mode,
}: FormProps<TemplateDataProps>) => {
  const { showLoading, hideLoading } = useLoading()

  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const theme = useTheme()

  const { data: myInventories, error: myInventoriesError } = useAxiosGet<
    InventoryDataProps[]
  >(`api/assigns/users-inventories/${user?.id}/inventories`)
  const { data: myProjects, error: myProjectsError } = useAxiosGet<
    ProjectDataProps[]
  >(`api/assigns/users-projects/${user?.id}/projects`)
  const { data: myCredentials, error: myCredentialsError } = useAxiosGet<
    CredentialDataProps[]
  >(`api/assigns/users-credentials/${user?.id}/credentials`)
  const { data: myOrganizations, error: myOrganizationsError } = useAxiosGet<
    UserOrganizationsDataProps[]
  >(`api/assigns/users-organizations/${user?.id}/organizations`)

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    defaultValues: {
      name: defaultValues?.name,
      description: defaultValues?.description,
      playbook_name: defaultValues?.playbook_name,
      limit: defaultValues?.limit,
      forks: defaultValues?.forks,
      extra_vars: defaultValues?.extra_vars,
      privilege_escalation: defaultValues?.privilege_escalation,
      verbosity: defaultValues?.verbosity,
      launch_type: defaultValues?.launch_type,
      inventory_id: defaultValues?.inventory.id,
      project_id: defaultValues?.project.id,
      credential_id: defaultValues?.credential.id,
      organization_id: defaultValues?.organization.id,
    },
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()
    await api
      .request({
        method: mode === 'create' ? 'POST' : 'PUT',
        url: mode === 'create' ? '/api/templates' : `/api/templates/${id}`,
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
    <form onSubmit={handleSubmit(onSubmit)}>
      <SubCard
        title={
          mode === 'edit' ? (
            defaultValues?.name
          ) : (
            <FormattedMessage id="templates.labels.new" />
          )
        }
        secondary={
          <CardHeaderActions
            launchJob={
              mode === 'edit'
                ? { template: defaultValues!, handleLaunchJob }
                : null
            }
            syncInventory={
              mode === 'edit'
                ? {
                    inventoryId: defaultValues!.inventory.id,
                    handleSyncInventory,
                  }
                : null
            }
            updateRepo={
              mode === 'edit'
                ? {
                    projectId: defaultValues!.project.id,
                    handleUpdateRepo,
                  }
                : null
            }
          />
        }
      >
        {myProjects && myInventories && myCredentials && myOrganizations ? (
          <>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="name"
                  label={<FormattedMessage id="templates.labels.name" />}
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
                  multiline
                  rows={1}
                  label={<FormattedMessage id="templates.labels.description" />}
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
                  id="playbook-name"
                  label={
                    <FormattedMessage id="templates.labels.playbookName" />
                  }
                  error={
                    errors.playbook_name &&
                    errors.playbook_name?.type === 'required'
                  }
                  helperText={
                    errors.playbook_name &&
                    errors.playbook_name?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('playbook_name', { required: true })}
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="limit"
                  multiline
                  rows={1}
                  label={<FormattedMessage id="templates.labels.limit" />}
                  {...register('limit')}
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="forks"
                  type="number"
                  defaultValue={5}
                  label={<FormattedMessage id="templates.labels.forks" />}
                  {...register('forks')}
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <FormControlLabel
                  control={
                    <Checkbox
                      id="privilege-escalation"
                      color="primary"
                      defaultChecked={
                        defaultValues
                          ? defaultValues.privilege_escalation
                          : false
                      }
                      {...register('privilege_escalation')}
                    />
                  }
                  label={
                    <FormattedMessage id="templates.labels.privilegeEscalation" />
                  }
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="verbosity"
                  select
                  label={
                    <FormattedMessage id="templates.labels.selectVerbosity" />
                  }
                  defaultValue={
                    defaultValues
                      ? defaultValues.verbosity
                      : verbosityMap.keys().next().value
                  }
                  error={
                    errors.verbosity && errors.verbosity?.type === 'required'
                  }
                  helperText={
                    errors.verbosity &&
                    errors.verbosity?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('verbosity', { required: true })}
                >
                  {[...verbosityMap.entries()].map(([key, option], index) => (
                    <MenuItem key={index} value={key}>
                      <FormattedMessage id={option.label} />
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="launch-type"
                  select
                  label={
                    <FormattedMessage id="templates.labels.selectLaunchType" />
                  }
                  defaultValue={
                    defaultValues
                      ? defaultValues.launch_type
                      : launchTypeMap.keys().next().value
                  }
                  error={
                    errors.launch_type &&
                    errors.launch_type?.type === 'required'
                  }
                  helperText={
                    errors.launch_type &&
                    errors.launch_type?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('launch_type', { required: true })}
                >
                  {[...launchTypeMap.entries()].map(([key, option], index) => (
                    <MenuItem key={index} value={key}>
                      {option.icon}
                      <FormattedMessage id={option.label} />
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  id="inventory-id"
                  select
                  label={
                    <FormattedMessage id="templates.labels.selectInventory" />
                  }
                  fullWidth
                  defaultValue={defaultValues ? defaultValues.inventory.id : ''}
                  error={
                    errors.inventory_id &&
                    errors.inventory_id?.type === 'required'
                  }
                  helperText={
                    errors.inventory_id &&
                    errors.inventory_id?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('inventory_id', { required: true })}
                >
                  {myInventories?.map((option) => (
                    <MenuItem key={option.id} value={option.id}>
                      {option.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  id="project-id"
                  select
                  label={
                    <FormattedMessage id="templates.labels.selectProject" />
                  }
                  fullWidth
                  defaultValue={defaultValues ? defaultValues.project.id : ''}
                  error={
                    errors.project_id && errors.project_id?.type === 'required'
                  }
                  helperText={
                    errors.project_id &&
                    errors.project_id?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('project_id', { required: true })}
                >
                  {myProjects?.map((option) => (
                    <MenuItem key={option.id} value={option.id}>
                      {option.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  id="credential-id"
                  select
                  label={
                    <FormattedMessage id="templates.labels.selectCredential" />
                  }
                  fullWidth
                  defaultValue={
                    defaultValues ? defaultValues.credential.id : ''
                  }
                  error={
                    errors.credential_id &&
                    errors.credential_id?.type === 'required'
                  }
                  helperText={
                    errors.credential_id &&
                    errors.credential_id?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('credential_id', { required: true })}
                >
                  {myCredentials
                    ?.filter(
                      (credential) =>
                        credential.credential_type !==
                        CredentialType.SOURCE_CONTROL,
                    )
                    .map((option) => (
                      <MenuItem key={option.id} value={option.id}>
                        {option.name}
                      </MenuItem>
                    ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  id="organization-id"
                  select
                  label={
                    <FormattedMessage id="templates.labels.selectOrganization" />
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
            myCredentialsError?.response?.status === 404 ||
            myProjectsError?.response?.status === 404 ||
            myInventoriesError?.response?.status === 404) && (
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
                      <FormattedMessage id="templates.labels.organization" />
                    </>
                  )}
                  {myCredentialsError && (
                    <>
                      <br />
                      <FormattedMessage id="templates.labels.credential" />
                    </>
                  )}
                  {myProjectsError && (
                    <>
                      <br />
                      <FormattedMessage id="templates.labels.project" />
                    </>
                  )}
                  {myInventoriesError && (
                    <>
                      <br />
                      <FormattedMessage id="templates.labels.inventory" />
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
