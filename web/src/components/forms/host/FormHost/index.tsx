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
import { FormProps } from '../../../../types'
import { UserOrganizationsDataProps } from '../../../../types/access'
import { HostDataProps } from '../../../../types/host'
import { AnimateButton } from '../../../AnimateButton'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

export interface IFormInput {
  hostname: string
  description?: string
  ipv4: string
  organization_id: string
}

export const FormHost = ({
  defaultValues,
  setNewData,
  mode,
}: FormProps<HostDataProps>) => {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const theme = useTheme()
  const { showLoading, hideLoading } = useLoading()

  const { data: myOrganizations, error: myOrganizationsError } = useAxiosGet<
    UserOrganizationsDataProps[]
  >(`api/assigns/users-organizations/${user?.id}/organizations`)

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    defaultValues: {
      hostname: defaultValues?.hostname,
      description: defaultValues?.description,
      ipv4: defaultValues?.ipv4,
      organization_id: defaultValues?.organization.id,
    },
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()
    await api
      .request({
        method: mode === 'create' ? 'POST' : 'PUT',
        url: mode === 'create' ? '/api/hosts' : `/api/hosts/${id}`,
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

  const updateHostStatus = async (id: string) => {
    showLoading()
    await api
      .put(`api/hosts/${id}/status`)
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

  const handleUpdateHostStatus = (
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    id: string,
  ) => updateHostStatus(id)

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <SubCard
        title={
          mode === 'edit' ? (
            defaultValues?.hostname
          ) : (
            <FormattedMessage id="hosts.labels.new" />
          )
        }
        secondary={
          <CardHeaderActions
            updateHostStatus={
              mode === 'edit'
                ? {
                    hostId: defaultValues!.id,
                    handleUpdateHostStatus,
                  }
                : null
            }
          />
        }
      >
        {myOrganizations ? (
          <>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="hostname"
                  label={<FormattedMessage id="hosts.labels.hostname" />}
                  error={
                    errors.hostname && errors.hostname?.type === 'required'
                  }
                  helperText={
                    errors.hostname &&
                    errors.hostname?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('hostname', { required: true })}
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="description"
                  multiline
                  rows={1}
                  label={<FormattedMessage id="hosts.labels.description" />}
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
                  id="ipv4"
                  type="text"
                  label={<FormattedMessage id="hosts.labels.ipv4" />}
                  error={
                    errors.ipv4 &&
                    errors.ipv4?.type === 'required' &&
                    errors.ipv4?.type === 'pattern'
                  }
                  helperText={
                    errors.ipv4 ? (
                      <>
                        {errors.ipv4?.type === 'required' && (
                          <FormHelperText error>
                            <FormattedMessage id="input.validation.required" />
                          </FormHelperText>
                        )}
                        {errors.ipv4?.type === 'pattern' && (
                          <FormHelperText error>
                            <FormattedMessage id="input.validation.ipAddress" />
                          </FormHelperText>
                        )}
                      </>
                    ) : null
                  }
                  {...register('ipv4', {
                    required: true,
                    pattern:
                      /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/gi,
                  })}
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  id="organization-id"
                  select
                  label={
                    <FormattedMessage id="hosts.labels.selectOrganization" />
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
          myOrganizationsError?.response?.status === 404 && (
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
                      <FormattedMessage id="hosts.labels.organization" />
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
