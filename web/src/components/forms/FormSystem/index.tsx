import {
  Button,
  CardActions,
  Divider,
  FormHelperText,
  Grid,
  TextField,
  useTheme,
} from '@mui/material'
import { FieldValues, SubmitHandler, useForm } from 'react-hook-form'
import { FormattedMessage } from 'react-intl'
import { useLoading } from '../../../hooks/useLoading'
import { api } from '../../../libs/axios'
import { dispatch } from '../../../libs/redux'
import { openSnackbar } from '../../../libs/redux/slices/snackbar'
import { FormProps } from '../../../types'
import { TowerDataProps } from '../../../types/tower'
import { AnimateButton } from '../../AnimateButton'
import { CardHeaderActions } from '../../cards/CardHeaderActions'
import SubCard from '../../cards/SubCard'

export interface IFormInput {
  company: string
  hostname: string
  ipv4: string
  username: string
  port: number
}

export const FormSystem = ({
  defaultValues,
  setNewData,
}: FormProps<TowerDataProps>) => {
  const { showLoading, hideLoading } = useLoading()
  const theme = useTheme()

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    defaultValues: {
      company: defaultValues?.company,
      hostname: defaultValues?.hostname,
      ipv4: defaultValues?.ipv4,
      username: defaultValues?.username,
      port: defaultValues?.port,
    },
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()
    await api
      .request({
        method: 'PUT',
        url: `/api/towers/owner`,
        data: formData,
      })
      .then((response) => {
        if (setNewData) {
          setNewData(response.data)
        }
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

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <SubCard
        title={defaultValues?.hostname}
        secondary={<CardHeaderActions />}
      >
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="company"
              label={<FormattedMessage id="settings.labels.company" />}
              error={errors.company && errors.company?.type === 'required'}
              helperText={
                errors.company &&
                errors.company?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required" />
                  </FormHelperText>
                )
              }
              {...register('company', { required: true })}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="hostname"
              label={<FormattedMessage id="settings.labels.hostname" />}
              error={errors.hostname && errors.hostname?.type === 'required'}
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
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="ipv4"
              type="text"
              label={<FormattedMessage id="settings.labels.ipv4" />}
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
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="username"
              type="text"
              hidden={true}
              label={<FormattedMessage id="settings.labels.username" />}
              error={errors.username && errors.username?.type === 'required'}
              helperText={
                errors.username &&
                errors.username?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required" />
                  </FormHelperText>
                )
              }
              {...register('username', { required: true })}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="port"
              type="number"
              label={<FormattedMessage id="settings.labels.port" />}
              error={errors.port && errors.port?.type === 'required'}
              helperText={
                errors.port &&
                errors.port?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required" />
                  </FormHelperText>
                )
              }
              {...register('port', { required: true })}
            />
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
      </SubCard>
    </form>
  )
}
