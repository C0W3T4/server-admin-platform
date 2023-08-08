import { EmailTwoTone } from '@mui/icons-material'
import {
  Button,
  CardActions,
  Divider,
  FormHelperText,
  Grid,
  InputAdornment,
  TextField,
  useTheme,
} from '@mui/material'
import { FieldValues, SubmitHandler, useForm } from 'react-hook-form'
import { FormattedMessage } from 'react-intl'
import { useNavigate } from 'react-router-dom'
import { useLoading } from '../../../../hooks/useLoading'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import { FormProps } from '../../../../types'
import { UserProfile } from '../../../../types/user'
import { AnimateButton } from '../../../AnimateButton'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

export interface IFormInput {
  first_name?: string
  last_name?: string
  email?: string
  username: string
}

export const FormMyAccount = ({
  defaultValues,
  mode,
}: FormProps<UserProfile>) => {
  const { showLoading, hideLoading } = useLoading()

  const navigate = useNavigate()
  const theme = useTheme()

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    defaultValues: {
      first_name: defaultValues?.first_name,
      last_name: defaultValues?.last_name,
      email: defaultValues?.email,
      username: defaultValues?.username,
    },
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()

    if (!formData.email) {
      delete formData.email
    }

    await api
      .request({
        method: 'PUT',
        url: `/api/users/current`,
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
          navigate(-1)
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

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <SubCard
        title={
          mode === 'edit' ? (
            defaultValues?.username
          ) : (
            <FormattedMessage id="users.labels.new" />
          )
        }
        secondary={<CardHeaderActions />}
      >
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="first_name"
              label={<FormattedMessage id="users.labels.firstName" />}
              {...register('first_name')}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="last_name"
              label={<FormattedMessage id="users.labels.lastName" />}
              {...register('last_name')}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="email"
              type="email"
              label={<FormattedMessage id="users.labels.email" />}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <EmailTwoTone />
                  </InputAdornment>
                ),
              }}
              {...register('email')}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="username"
              type="text"
              hidden={true}
              label={<FormattedMessage id="users.labels.username" />}
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
